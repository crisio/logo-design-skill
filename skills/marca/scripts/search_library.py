#!/usr/bin/env python3
"""Busca en la biblioteca de referencia incluida, con más de 1400 logos SVG reales.

Úsalo para estudiar cómo resuelven un problema los logos existentes (una técnica, un tema, un tipo de logo), para ver
qué aspecto tiene ya un sector (y así poder evitarlo) y para sacar unos cuantos archivos que puedas leer como ejemplos
de SVG. Los logos son marcas registradas de sus propietarios: estúdialos, nunca los copies.

Ejemplos:
  python3 scripts/search_library.py --technique negative-space --exemplary
  python3 scripts/search_library.py --type letterform --geometry circle --max-colors 1 --limit 12
  python3 scripts/search_library.py --subject "bird" --format paths
  python3 scripts/search_library.py --industry payments-fintech --summary
  python3 scripts/search_library.py --query cloud --type pictorial --format json
  python3 scripts/search_library.py --list-values          # muestra todos los valores permitidos de los filtros

Los filtros se combinan con Y (AND). Los filtros de varios valores (--technique, --geometry) aceptan una lista separada
por comas y exigen que se cumplan todos.
"""
import argparse
import json
import os
import sys
from collections import Counter

sys.dont_write_bytecode = True  # mantiene limpia la carpeta de la skill (sin __pycache__)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import svglib  # noqa: E402


def load_catalog():
    if not os.path.exists(svglib.CATALOG_PATH):
        sys.exit("no se encontró catalog.json; ejecuta primero scripts/build_catalog.py")
    with open(svglib.CATALOG_PATH, encoding="utf-8") as fh:
        return json.load(fh)


def matches(r, a):
    if a.type and r.get("mark_type") != a.type:
        return False
    if a.symbol_type and r.get("symbol_type") != a.symbol_type:
        return False
    if a.technique and not all(t in r.get("techniques", []) for t in a.technique.split(",")):
        return False
    if a.geometry and not all(g in r.get("geometry", []) for g in a.geometry.split(",")):
        return False
    if a.industry and r.get("industry") != a.industry:
        return False
    if a.color and a.color not in (r.get("color_families", []) + [r.get("primary_family")]):
        return False
    if a.primary_color and r.get("primary_family") != a.primary_color:
        return False
    if a.max_colors is not None and r.get("n_colors", 99) > a.max_colors:
        return False
    if a.min_colors is not None and r.get("n_colors", 0) < a.min_colors:
        return False
    if a.aspect and r.get("aspect_class") != a.aspect:
        return False
    if a.variant and r.get("variant") != a.variant:
        return False
    if a.type_style and r.get("type_style") != a.type_style:
        return False
    if a.case and r.get("case") != a.case:
        return False
    if a.mood and a.mood.lower() not in [m.lower() for m in r.get("mood", [])]:
        return False
    if a.exemplary and not r.get("exemplary"):
        return False
    if a.no_gradient and r.get("gradients"):
        return False
    if a.subject and a.subject.lower() not in (r.get("subject") or "").lower():
        return False
    if a.query:
        hay = " ".join([r.get("file", ""), r.get("subject") or "", r.get("note") or "", " ".join(r.get("mood", []))]).lower()
        if not all(w in hay for w in a.query.lower().split()):
            return False
    return True


def summary(rows, total):
    n = len(rows)
    print(f"{n} logos coinciden (de {total}).\n")
    if not n:
        return

    def block(title, counter, k=10):
        print(title)
        for key, cnt in counter.most_common(k):
            print(f"  {str(key):24s} {cnt:4d}  {cnt / n * 100:5.1f}%")
        print()
    block("Tipos de logo", Counter(r.get("mark_type") for r in rows))
    block("Tipo de símbolo (imagotipos)", Counter(r.get("symbol_type") for r in rows if r.get("symbol_type")))
    block("Familia de color principal", Counter(r.get("primary_family") for r in rows))
    block("Técnicas", Counter(t for r in rows for t in r.get("techniques", [])), 12)
    block("Geometría", Counter(g for r in rows for g in r.get("geometry", [])))
    block("Estilo tipográfico (cuando hay texto)", Counter(r.get("type_style") for r in rows if r.get("type_style")))
    cols = Counter(r.get("n_colors") for r in rows)
    few = sum(v for k, v in cols.items() if k is not None and k <= 2)
    print(f"Cantidad de colores: el {few / n * 100:.0f} % usa 1-2 colores; hay degradados en el "
          f"{sum(1 for r in rows if r.get('gradients')) / n * 100:.0f} %.")
    ex = [r["file"] for r in rows if r.get("exemplary")][:12]
    if ex:
        print("Archivos ejemplares:", ", ".join(ex))
    print("\nCómo leerlo: los tipos, colores y técnicas más frecuentes son las convenciones del sector. "
          "Repetirlos comunica pertenencia; apartarse de ellos crea diferenciación.")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--type", help="tipo de logo: wordmark|lettermark|letterform|pictorial|abstract|mascot|emblem|combination")
    ap.add_argument("--symbol-type", help="tipo de símbolo dentro de los imagotipos (combination)")
    ap.add_argument("--technique", help="p. ej. negative-space, geometric-construction, letter-substitution (coma = Y)")
    ap.add_argument("--geometry", help="p. ej. circle, hexagon, triangle, organic (coma = Y)")
    ap.add_argument("--industry", help="sector, p. ej. developer-tools, payments-fintech, database-data")
    ap.add_argument("--color", help="familia de color presente en cualquier parte: red|orange|yellow|green|cyan|blue|purple|pink|black|white|gray")
    ap.add_argument("--primary-color", help="familia dominante: un matiz, 'multi' o 'mono'")
    ap.add_argument("--max-colors", type=int)
    ap.add_argument("--min-colors", type=int)
    ap.add_argument("--aspect", help="proporción: square|wide|horizontal|extra-wide|tall")
    ap.add_argument("--variant", help="main|icon (icon = símbolo independiente de una marca que también tiene composición)")
    ap.add_argument("--type-style", help="estilo tipográfico: geometric-sans|grotesque-sans|humanist-sans|rounded-sans|serif|slab|script|display-custom|monospace")
    ap.add_argument("--case", help="uso de mayúsculas: lowercase|uppercase|titlecase|mixed")
    ap.add_argument("--mood", help="un solo adjetivo de tono (en inglés), p. ej. friendly, technical, playful")
    ap.add_argument("--subject", help="fragmento del tema visual (en inglés), p. ej. bird, shield, cloud, letter a")
    ap.add_argument("--query", help="palabras libres que se buscan en el nombre de archivo, el tema, la nota y el tono (en inglés)")
    ap.add_argument("--exemplary", action="store_true", help="solo ejemplos didácticos sólidos")
    ap.add_argument("--no-gradient", action="store_true")
    ap.add_argument("--limit", type=int, default=25)
    ap.add_argument("--format", choices=("table", "paths", "json"), default="table")
    ap.add_argument("--summary", action="store_true", help="vista agregada: convenciones del conjunto que coincide")
    ap.add_argument("--list-values", action="store_true", help="muestra los valores permitidos de cada filtro")
    a = ap.parse_args()

    cat = load_catalog()
    if a.list_values:
        for key in ("mark_type", "symbol_type", "industry", "primary_family", "aspect_class", "type_style", "case"):
            print(f"{key}: {', '.join(sorted({str(r.get(key)) for r in cat if r.get(key)}))}")
        for key in ("techniques", "geometry"):
            vals = Counter(v for r in cat for v in r.get(key, []))
            print(f"{key}: {', '.join(f'{k}({c})' for k, c in vals.most_common())}")
        moods = Counter(m.lower() for r in cat for m in r.get("mood", []))
        print("mood (los 40 más frecuentes):", ", ".join(k for k, _ in moods.most_common(40)))
        return

    # tolera valores de filtro casi exactos: "security" -> "security-identity", "fintech" -> "payments-fintech"
    for attr, field in (("industry", "industry"), ("type", "mark_type"), ("symbol_type", "symbol_type"),
                        ("type_style", "type_style"), ("aspect", "aspect_class"), ("primary_color", "primary_family")):
        val = getattr(a, attr)
        if not val:
            continue
        known = sorted({str(r.get(field)) for r in cat if r.get(field)})
        if val in known:
            continue
        close = [k for k in known if val.lower() in k.lower() or k.lower() in val.lower()]
        if len(close) == 1:
            print(f"(--{attr.replace('_', '-')} '{val}' → usando '{close[0]}')")
            setattr(a, attr, close[0])
        else:
            hint = ", ".join(close) if close else ", ".join(known)
            sys.exit(f"valor desconocido para --{attr.replace('_', '-')}: '{val}'. ¿Quisiste decir alguno de estos? {hint}")
    for attr, field in (("technique", "techniques"), ("geometry", "geometry")):
        val = getattr(a, attr)
        if not val:
            continue
        known = sorted({v for r in cat for v in r.get(field, [])})
        fixed = []
        for part in val.split(","):
            if part in known:
                fixed.append(part)
                continue
            close = [k for k in known if part.lower() in k.lower()]
            if len(close) == 1:
                print(f"(--{attr} '{part}' → usando '{close[0]}')")
                fixed.append(close[0])
            else:
                sys.exit(f"valor desconocido para --{attr}: '{part}'. ¿Quisiste decir alguno de estos? {', '.join(close) if close else ', '.join(known)}")
        setattr(a, attr, ",".join(fixed))

    rows = [r for r in cat if matches(r, a)]
    rows.sort(key=lambda r: (not r.get("exemplary"), r.get("anchors", 0)))
    if a.summary:
        summary(rows, len(cat))
        return
    shown = rows[: a.limit]
    if a.format == "json":
        print(json.dumps(shown, ensure_ascii=False, indent=1))
    elif a.format == "paths":
        for r in shown:
            print(os.path.join(svglib.LIBRARY_SVG_DIR, r["file"]))
    else:
        print(f"{len(rows)} coinciden, se muestran {len(shown)}  (★ = ejemplar; archivos en {svglib.LIBRARY_SVG_DIR})")
        for r in shown:
            star = "★" if r.get("exemplary") else " "
            kind = r.get("mark_type") or "?"
            if r.get("symbol_type"):
                kind += "/" + r["symbol_type"]
            print(f"{star} {r['file']:34s} {kind:22s} {r.get('n_colors', 0):2d}c  {(r.get('subject') or '')[:48]}")
            if r.get("note") and r.get("exemplary"):
                print(f"      ↳ {r['note']}")


if __name__ == "__main__":
    main()
