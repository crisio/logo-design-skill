#!/usr/bin/env python3
"""Prueba rápida de todos los scripts de la skill, tal como los ejecuta un agente (la usa la CI en Windows, macOS y Linux).

  python tools/smoke_test.py            # todas las pruebas; las de PNG corren si hay un renderizador disponible

Cada script corre en un subproceso con la codificación de consola predeterminada de la plataforma (cp1252 en
Windows), así se detectan fallos como UnicodeEncodeError con los símbolos de los reportes. Solo usa la
biblioteca estándar.
"""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zlib

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILL = os.path.join(ROOT, "skills", "marca")
SCRIPTS = os.path.join(SKILL, "scripts")
LIB = os.path.join(SKILL, "assets", "library", "svg")

SYMBOL = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256"><title>Símbolo de prueba</title>
<circle cx="128" cy="128" r="96" fill="#0F7C80"/>
<path d="M80 150 L176 146 L176 170 L80 174 Z" fill="#FFFFFF"/></svg>
"""
LOCKUP = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 256"><title>Composición de prueba</title>
<circle cx="128" cy="128" r="96" fill="#0F7C80"/>
<rect x="280" y="100" width="560" height="56" rx="8" fill="#161616"/></svg>
"""

failures = []


def run(name, args, expect=(), cwd=None):
    """Ejecuta un script; falla si sale con código distinto de cero, hay un traceback o falta un texto o archivo esperado."""
    env = {k: v for k, v in os.environ.items() if k not in ("PYTHONIOENCODING", "PYTHONUTF8")}
    p = subprocess.run([sys.executable] + args, cwd=cwd or SKILL, env=env, capture_output=True)
    out = (p.stdout + p.stderr).decode("utf-8", "replace")
    problems = []
    if p.returncode != 0:
        problems.append(f"código de salida {p.returncode}")
    if "Traceback (most recent call last)" in out:
        problems.append("traceback")
    for e in expect:
        if os.path.isabs(e):
            if not os.path.exists(e):
                problems.append(f"falta el archivo {e}")
        elif e not in out:
            problems.append(f"la salida no contiene {e!r}")
    status = "ok   " if not problems else "FALLA"
    print(f"[{status}] {name}")
    if problems:
        failures.append(name)
        print("        " + "; ".join(problems))
        print("        " + out.strip().replace("\n", "\n        ")[-2500:])
    return out


def png_ojos(path, lado=160):
    """PNG RGBA de prueba: un cuerpo verde redondo con dos ojos ovalados oscuros."""
    filas = []
    for y in range(lado):
        fila = bytearray([0])
        for x in range(lado):
            cx, cy = x - lado / 2 + 0.5, y - lado / 2 + 0.5
            ojo = any(((x - ex) / 8) ** 2 + ((y - lado * 0.4) / 15) ** 2 <= 1 for ex in (lado * 0.4, lado * 0.6))
            if ojo:
                fila += bytes((20, 24, 24, 255))
            elif cx * cx + cy * cy <= (lado * 0.4) ** 2:
                fila += bytes((27, 158, 115, 255))
            else:
                fila += bytes((0, 0, 0, 0))
        filas.append(bytes(fila))

    def bloque(tipo, cuerpo):
        return (len(cuerpo).to_bytes(4, "big") + tipo + cuerpo
                + (zlib.crc32(tipo + cuerpo) & 0xFFFFFFFF).to_bytes(4, "big"))
    ihdr = lado.to_bytes(4, "big") * 2 + bytes((8, 6, 0, 0, 0))
    with open(path, "wb") as fh:
        fh.write(b"\x89PNG\r\n\x1a\n" + bloque(b"IHDR", ihdr) + bloque(b"IDAT", zlib.compress(b"".join(filas)))
                 + bloque(b"IEND", b""))


def png_rgba(path, lado=64):
    """Escribe un PNG RGBA de prueba: fondo transparente y un círculo opaco en el centro."""
    filas = []
    for y in range(lado):
        fila = bytearray([0])
        for x in range(lado):
            dentro = (x - lado / 2 + 0.5) ** 2 + (y - lado / 2 + 0.5) ** 2 <= (lado * 0.3) ** 2
            fila += bytes((122, 50, 104, 255)) if dentro else bytes((0, 0, 0, 0))
        filas.append(bytes(fila))

    def bloque(tipo, cuerpo):
        return (len(cuerpo).to_bytes(4, "big") + tipo + cuerpo
                + (zlib.crc32(tipo + cuerpo) & 0xFFFFFFFF).to_bytes(4, "big"))
    ihdr = lado.to_bytes(4, "big") * 2 + bytes((8, 6, 0, 0, 0))
    with open(path, "wb") as fh:
        fh.write(b"\x89PNG\r\n\x1a\n" + bloque(b"IHDR", ihdr) + bloque(b"IDAT", zlib.compress(b"".join(filas)))
                 + bloque(b"IEND", b""))


def main():
    tmp = tempfile.mkdtemp(prefix="marca-prueba-")
    try:
        sym, lock = os.path.join(tmp, "a-symbol.svg"), os.path.join(tmp, "a-lockup.svg")
        for path, body in ((sym, SYMBOL), (lock, LOCKUP)):
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(body)
        lib = sorted(f for f in os.listdir(LIB) if f.endswith(".svg"))[:3]
        S = lambda f: os.path.join(SCRIPTS, f)

        # revisión del frontmatter y de los manifiestos
        text = open(os.path.join(SKILL, "SKILL.md"), encoding="utf-8").read()
        m = re.match(r"---\nname: (.+)\ndescription: (.+?)\n", text)
        ok = bool(m) and m.group(1).strip() == "marca" and len(m.group(2)) <= 1024
        versions = set()
        for f in ("plugin.json", "marketplace.json"):
            data = json.load(open(os.path.join(ROOT, ".claude-plugin", f), encoding="utf-8"))
            versions.add(data.get("version") or data["plugins"][0]["version"])
            if "plugins" in data:
                versions.update(p["version"] for p in data["plugins"])
        ok = ok and len(versions) == 1
        print(f"[{'ok   ' if ok else 'FALLA'}] frontmatter de SKILL.md y versiones de los manifiestos "
              f"({', '.join(sorted(versions))})")
        if not ok:
            failures.append("frontmatter/manifiestos")

        run("build_catalog --check", [S("build_catalog.py"), "--check"], ["0 faltantes"])
        run("svg_audit (ejemplos + biblioteca)", [S("svg_audit.py"), sym, lock] + [os.path.join(LIB, f) for f in lib],
            ["puntaje de listo para producción"])
        run("svg_audit --json", [S("svg_audit.py"), "--json", sym])
        run("search_library con valor aproximado", [S("search_library.py"), "--industry", "finance", "--limit", "3"],
            ["usando 'finance-banking'"])
        run("search_library --summary", [S("search_library.py"), "--technique", "negative-space", "--summary"],
            ["logos coinciden"])
        out = run("search_library --format json", [S("search_library.py"), "--type", "letterform", "--format", "json",
                                                    "--limit", "2"])
        try:
            json.loads(out[out.index("["):])
        except ValueError:
            failures.append("salida json de search_library")
            print("[FALLA] la salida json de search_library no es JSON válido")
        run("search_library --list-values", [S("search_library.py"), "--list-values"], ["mark_type:"])
        run("concept_sheet", [S("concept_sheet.py"), sym, sym, "--lockups", lock, lock, "--names", "A", "B",
                              "--notes", "Uno.", "Dos.", "--recommend", "1", "-o", os.path.join(tmp, "concepts.png")],
            [os.path.join(tmp, "concepts.svg")])
        run("preview_sheet", [S("preview_sheet.py"), sym, lock, "--refs-industry", "finance-banking",
                              "-o", os.path.join(tmp, "preview.html")], [os.path.join(tmp, "preview.html")])
        run("presentation_board --list-mockups", [S("presentation_board.py"), "--list-mockups"], ["payment-card"])
        spec = {"brand": "Humo", "tagline": "Prueba", "brief": "Un brief de prueba.", "adjectives": ["sereno"],
                "industry": "finance", "brand_color": "#0F7C80", "final": True, "greyscale": False,
                "concepts": [{"name": "Prueba", "symbol": sym, "lockup": lock, "idea": "Una idea.",
                              "rationale": ["Uno", "Dos"]}]}
        spec_path = os.path.join(tmp, "spec.json")
        with open(spec_path, "w", encoding="utf-8") as fh:
            json.dump(spec, fh)
        run("presentation_board", [S("presentation_board.py"), spec_path, "-o", os.path.join(tmp, "board.html")],
            [os.path.join(tmp, "board.html")])
        run("export_variants (SVG)", [S("export_variants.py"), sym, "--out-dir", os.path.join(tmp, "export"),
                                      "--mono", "#0F7C80", "--icon-bg", "#0F7C80"])
        avatar = os.path.join(tmp, "personaje.png")
        png_rgba(avatar)
        run("check_alpha (PNG transparente)", [S("check_alpha.py"), avatar], ["canal alfa real", "APROBADO"])
        run("check_alpha --json y --preview", [S("check_alpha.py"), avatar, "--json", "--preview",
                                                os.path.join(tmp, "prueba.html"), "--color", "#7A3268"],
            ['"aprobado": true', os.path.join(tmp, "prueba.html")])
        con_ojos = os.path.join(tmp, "con-ojos.png")
        png_ojos(con_ojos)
        run("eye_highlight", [S("eye_highlight.py"), con_ojos, os.path.join(tmp, "con-brillo.png")],
            ["brillo agregado", os.path.join(tmp, "con-brillo.png")])
        kot_dir = os.path.join(tmp, "kot")
        run("kot_build --sin-animacion", [S("kot_build.py"), "--nombre", "Prueba", "--personaje", con_ojos,
                                          "--color", "#1B9E73", "--fondo", "#E9F6F1", "--salida", kot_dir,
                                          "--familia", os.path.join(tmp, "kots"), "--sin-animacion"],
            [os.path.join(kot_dir, "kot.json"), os.path.join(kot_dir, "kot.png"), os.path.join(kot_dir, "kot.html"),
             os.path.join(kot_dir, "kot-avatar.js"), os.path.join(tmp, "kots", "familia.html")])
        run("check_alpha --opacar", [S("check_alpha.py"), avatar, "--opacar", os.path.join(tmp, "limpio.png")],
            [os.path.join(tmp, "limpio.png")])
        which = run("render_png --which", [S("render_png.py"), "--which"])
        if "renderizadores disponibles: ninguno" not in which and "renderizadores disponibles:" in which:
            png = os.path.join(tmp, "a.png")
            run("render_png (PNG)", [S("render_png.py"), sym, "-o", png, "--size", "64"], [png])
            run("export_variants --web-icons", [S("export_variants.py"), sym, "--out-dir", os.path.join(tmp, "web"),
                                               "--icon-bg", "#0F7C80", "--web-icons"],
                [os.path.join(tmp, "web", "favicon.ico")])
        else:
            print("[omite] pruebas de PNG (no hay renderizador en esta máquina)")
        run("package_skill", [os.path.join(ROOT, "tools", "package_skill.py")],
            [os.path.join(ROOT, "dist", "marca.zip"), os.path.join(ROOT, "dist", "marca-lite.zip")],
            cwd=ROOT)

        caches = [d for d, _, _ in os.walk(SKILL) if os.path.basename(d) == "__pycache__"]
        print(f"[{'ok   ' if not caches else 'FALLA'}] no se escribió __pycache__ en la carpeta de la skill")
        if caches:
            failures.append("__pycache__ en la carpeta de la skill: " + ", ".join(caches))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    print()
    if failures:
        print(f"{len(failures)} prueba(s) fallaron: {', '.join(failures)}")
        sys.exit(1)
    print("todas las pruebas pasaron")


if __name__ == "__main__":
    sys.dont_write_bytecode = True
    main()
