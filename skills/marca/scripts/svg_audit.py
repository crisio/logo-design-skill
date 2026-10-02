#!/usr/bin/env python3
"""Audita un SVG de logo según los principios de diseño de logos y las reglas de producción.

Revisa la estructura (viewBox, title, texto/raster/filtros), la disciplina de color, la complejidad frente a la
biblioteca de referencia, los ángulos casi exactos (líneas a 0.3–3° de un ángulo limpio), los detalles diminutos que
desaparecen en tamaño pequeño, el margen y el centrado dentro del viewBox, los trazos que deberían expandirse y los
"falsos huecos" blancos.

Uso:
  python3 scripts/svg_audit.py logo.svg [otro.svg ...]
  python3 scripts/svg_audit.py logo.svg --json            # salida legible por máquina
  python3 scripts/svg_audit.py logo.svg --bg "#0F7C80"    # además reporta el contraste de los colores sobre un fondo

El código de salida es 0 salvo que un archivo no se pueda analizar. Los hallazgos son consejos, no leyes: una decisión
deliberada puede prevalecer sobre una advertencia, pero deberías poder explicar por qué.
"""
import argparse
import json
import math
import os
import re
import sys

sys.dont_write_bytecode = True  # mantiene limpia la carpeta de la skill (sin __pycache__)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import svglib  # noqa: E402

CLEAN_ANGLES = [0, 15, 30, 45, 60, 75, 90, 105, 120, 135, 150, 165, 180]


def load_stats():
    try:
        with open(svglib.STATS_PATH, encoding="utf-8") as fh:
            return json.load(fh)
    except OSError:
        return None


def audit(path, bg=None):
    findings = []  # (nivel, código, mensaje)

    def add(level, code, msg):
        findings.append({"level": level, "code": code, "message": msg})

    raw, root = svglib.load_svg(path)
    counts = svglib.element_counts(root)
    vb = svglib.view_box(root)
    info = {"file": os.path.basename(path), "bytes": os.path.getsize(path)}

    # --- estructura ------------------------------------------------------------------------
    if not root.get("viewBox"):
        add("WARN", "no-viewbox", "Sin viewBox: el logo no escalará de forma predecible. Agrega viewBox=\"0 0 W H\".")
    if vb:
        info["viewBox"] = vb
        w, h = vb[2], vb[3]
        info["aspect"] = round(w / h, 3) if h else None
        info["aspect_class"] = svglib.aspect_class(info["aspect"])
        if any(abs(v - round(v)) > 1e-6 for v in vb):
            add("INFO", "fractional-viewbox", "El viewBox tiene valores fraccionarios; un lienzo con enteros es más fácil de ajustar a una retícula.")
    if counts.get("text", 0) or counts.get("tspan", 0):
        add("FAIL", "live-text", "Contiene <text>: los logos finales deben usar trazados convertidos a contornos (las fuentes cambian de una máquina a otra).")
    if counts.get("image", 0):
        add("FAIL", "raster-image", "Contiene <image> (raster incrustado). El archivo maestro de un logo debe ser completamente vectorial.")
    if counts.get("filter", 0):
        add("WARN", "filter", "Usa filtros (desenfoque/sombra/resplandor). Se ven distinto en cada programa y no se pueden imprimir; usa formas planas.")
    if counts.get("mask", 0):
        add("INFO", "mask", "Usa <mask>. Está bien para explorar; para producción conviértela en trazados (plotters de corte, bordado).")
    if counts.get("foreignObject", 0):
        add("FAIL", "foreign-object", "Contiene <foreignObject> (HTML dentro del SVG). No es portable.")
    if counts.get("style", 0):
        add("INFO", "style-block", "Usa un bloque <style>; los atributos fill en línea son más portables entre programas.")
    if not counts.get("title", 0):
        add("INFO", "no-title", "Sin <title>: agrega uno por accesibilidad (p. ej. <title>Logo de la marca</title>).")
    if re.search(r"\d+\.\d{4,}", raw):
        add("INFO", "precision", "Coordenadas con 4 o más decimales: redondea a 0–2 decimales para reducir el tamaño y dejar ver los desalineamientos.")
    for attr in ("sodipodi", "inkscape:", "sketch:", "data-name", "xmlns:xlink"):
        if attr in raw and attr != "xmlns:xlink":
            add("INFO", "editor-metadata", f"Hay metadatos del editor ('{attr}'); quítalos de los archivos de entrega.")
            break

    # --- color -------------------------------------------------------------------------------
    colors = svglib.collect_colors(root)
    info["colors"] = colors
    grads = counts.get("linearGradient", 0) + counts.get("radialGradient", 0)
    info["gradients"] = grads
    n = len(colors)
    if n > 4:
        add("WARN", "many-colors", f"{n} colores distintos. ~75 % de los logos de referencia usan ≤3; cada color extra le resta memorabilidad y complica la reproducción.")
    elif n == 0:
        add("WARN", "no-paint", "No se encontró ningún relleno ni trazo visible.")
    if grads:
        add("WARN", "gradient", f"{grads} degradado(s). Conserva un archivo maestro en colores planos; los degradados pierden fuerza en impresión y en tamaños pequeños (~19 % de los logos de referencia los usan).")
    opac = re.findall(r'(?:fill-)?opacity\s*[:=]\s*"?\s*(0?\.\d+)', raw)
    if opac:
        add("INFO", "transparency", "Usa transparencia/opacidad. Los efectos de superposición necesitan una alternativa en color sólido para impresión y bordado.")
    # falsos huecos: una forma blanca pintada encima de (dentro de la caja de) una forma de color anterior
    boxes = svglib.painted_shape_boxes(root)
    knock, on_tile = 0, 0
    canvas_area = (vb[2] * vb[3]) if vb else None
    for i, (_, bb_w, fill_w) in enumerate(boxes):
        if not fill_w or fill_w == "url" or svglib.lightness(fill_w) <= 0.97:
            continue
        for _, bb_c, fill_c in boxes[:i]:
            if fill_c and (fill_c == "url" or svglib.lightness(fill_c) <= 0.97):
                if bb_w[0] >= bb_c[0] - 0.5 and bb_w[1] >= bb_c[1] - 0.5 and bb_w[2] <= bb_c[2] + 0.5 and bb_w[3] <= bb_c[3] + 0.5:
                    area_c = (bb_c[2] - bb_c[0]) * (bb_c[3] - bb_c[1])
                    if canvas_area and area_c >= 0.8 * canvas_area:
                        on_tile += 1
                    else:
                        knock += 1
                    break
    if on_tile and not knock:
        add("INFO", "on-tile", "Arte blanco sobre una placa o contenedor que cubre todo el lienzo: está bien para íconos de app y "
            "avatares; asegúrate de que exista una versión sin la placa para otros usos.")
    if knock:
        add("WARN", "white-knockout", f"{knock} forma(s) blanca(s) están pintadas encima de formas de color. Si la idea es que "
            "sean huecos, se verán como manchas blancas sobre fondos de color o fotos y arruinarán las versiones a una tinta: "
            "haz huecos reales (fill-rule=\"evenodd\" o trazados restados). Ignóralo si el blanco es deliberado (p. ej. un "
            "símbolo sobre una placa).")
    all_white = bool(colors) and all(svglib.lightness(c) > 0.9 for c in colors)
    if bg:
        bgc = svglib.normalize_color(bg)
        if bgc and all_white and svglib.lightness(bgc) > 0.6:
            add("INFO", "reversed-file", f"Todo el color es blanco o casi blanco: parece una versión invertida; pruébala con un "
                "--bg oscuro en lugar de " + bgc + ".")
        elif bgc:
            low = [f"{c} ({svglib.contrast_ratio(c, bgc):.1f}:1)" for c in colors if svglib.contrast_ratio(c, bgc) < 3]
            if low:
                add("WARN", "low-contrast", f"Contraste bajo sobre {bgc}: " + ", ".join(low) + " — apunta a ≥3:1 para las partes del logo y a 4.5:1 para texto pequeño.")

    # --- trazos ------------------------------------------------------------------------------
    stroked = 0
    for el in root.iter():
        props = svglib.style_props(el)
        s = props.get("stroke", el.get("stroke"))
        if s and s.strip().lower() not in ("none", "transparent"):
            stroked += 1
    if stroked:
        add("INFO", "strokes", f"{stroked} elemento(s) con trazo. Expande los trazos a contornos rellenos en el archivo maestro para "
            "que el logo escale y se corte de forma predecible (o documenta que es una variante basada en trazos).")

    # --- geometría ---------------------------------------------------------------------------
    geo = svglib.document_geometry(root)
    info["anchors"] = geo["anchors"]
    size = max(vb[2], vb[3]) if vb else None
    stats = load_stats()
    if stats:
        key = "anchors_square" if info.get("aspect_class") == "square" else "anchors_all"
        d = stats[key]
        info["library_anchor_percentiles"] = d
        if geo["anchors"] > d["p95"]:
            add("WARN", "complex", f"{geo['anchors']} puntos de anclaje: más que el 95 % de los logos de referencia comparables "
                f"(mediana {d['median']}). Simplifica: menos puntos, formas unidas, menos detalle.")
        elif geo["anchors"] > d["p75"]:
            add("INFO", "complexity", f"{geo['anchors']} puntos de anclaje (mediana de la biblioteca {d['median']}, p75 {d['p75']}). "
                "Comprueba que cada punto se justifique.")
    # ángulos casi exactos
    if size:
        near = []
        for ang, length, a, b in geo["lines"]:
            if length < size * 0.04:
                continue
            closest = min(CLEAN_ANGLES, key=lambda c: abs(c - ang))
            dev = abs(closest - ang)
            if 0.3 < dev <= 3.0:
                near.append((round(ang, 1), closest % 180, round(length, 1), a))
        if near:
            sample = "; ".join(f"{x[0]}° (→{x[1]}°) largo {x[2]} en ({x[3][0]:.0f},{x[3][1]:.0f})" for x in near[:6])
            add("WARN", "near-miss-angle", f"{len(near)} borde(s) recto(s) a 0.3–3° de un ángulo limpio: se leen como "
                f"errores. Ajústalos: {sample}" + (" …" if len(near) > 6 else "") +
                ". (Es esperable, y está bien, en texto compuesto sobre una curva o en elementos rotados a propósito).")
        # detalles diminutos: los símbolos deben sobrevivir a ~48 px; las composiciones, a ~32 px de alto
        if info.get("aspect_class") in ("wide", "horizontal", "extra-wide"):
            ref, label = vb[3] / 32, "1/32 de la altura de la composición (≈1 px a 32 px de alto)"
        else:
            ref, label = size / 48, "1/48 del lienzo (≈1 px a 48 px)"
        tiny = [bb for bb in geo["subpath_boxes"]
                if max(bb[2] - bb[0], bb[3] - bb[1]) < ref and (bb[2] - bb[0]) * (bb[3] - bb[1]) > 0]
        if tiny:
            ex = "; ".join(f"{bb[2] - bb[0]:.1f}×{bb[3] - bb[1]:.1f} en ({bb[0]:.0f},{bb[1]:.0f})" for bb in tiny[:4])
            add("WARN", "tiny-detail", f"{len(tiny)} subforma(s) más pequeña(s) que {label}: {ex}{' …' if len(tiny) > 4 else ''}. "
                "Desaparecen en tamaño pequeño: agrándalas, únelas o elimínalas, o prepara una versión para tamaños pequeños.")
    # márgenes / centrado
    bb = geo["bbox"]
    if bb and vb:
        x0, y0, w, h = vb
        left, top = bb[0] - x0, bb[1] - y0
        right, bottom = x0 + w - bb[2], y0 + h - bb[3]
        info["content_bbox"] = [round(v, 2) for v in bb]
        info["margins"] = {"left": round(left, 1), "right": round(right, 1), "top": round(top, 1), "bottom": round(bottom, 1)}
        tol = max(w, h) * 0.01
        if min(left, right, top, bottom) < -tol:
            add("WARN", "overflow", "El arte se sale del viewBox y quedará recortado.")
        if abs(left - right) > max(w, h) * 0.03:
            add("INFO", "off-centre-x", f"Los márgenes horizontales difieren (izquierdo {left:.1f}, derecho {right:.1f}). ¿Es un "
                "centrado óptico intencional? Si no, céntralo.")
        if abs(top - bottom) > max(w, h) * 0.03:
            add("INFO", "off-centre-y", f"Los márgenes verticales difieren (superior {top:.1f}, inferior {bottom:.1f}). Recuerda "
                "que el centro óptico queda un poco por encima del centro geométrico.")
        fill_ratio = ((bb[2] - bb[0]) * (bb[3] - bb[1])) / (w * h) if w and h else 0
        info["bbox_fill_ratio"] = round(fill_ratio, 3)
        if info.get("aspect_class") == "square" and fill_ratio < 0.35:
            add("INFO", "small-in-canvas", "El logo ocupa poco de su lienzo cuadrado; ajusta el viewBox o agrándalo.")
    # consejos sobre proporciones
    ac = info.get("aspect_class")
    if ac == "tall":
        add("INFO", "tall", "Las proporciones altas (<0.8:1) resultan incómodas en encabezados e íconos de app; considera un símbolo más cuadrado.")
    if ac == "extra-wide":
        add("INFO", "extra-wide", "Composición extra ancha (>4.5:1): se ve mal al reducirse; prepara una versión apilada y un símbolo independiente.")

    score = 100
    for f in findings:
        score -= {"FAIL": 25, "WARN": 8, "INFO": 1}[f["level"]]
    info["score"] = max(0, score)
    info["findings"] = findings
    return info


def print_report(info):
    print(f"\n=== {info['file']}  ({info['bytes']} bytes)")
    vb = info.get("viewBox")
    if vb:
        print(f"viewBox {vb[0]:g} {vb[1]:g} {vb[2]:g} {vb[3]:g} · proporción {info.get('aspect')} ({info.get('aspect_class')})")
    print(f"colores {len(info.get('colors', []))}: {' '.join(info.get('colors', []))} · degradados {info.get('gradients', 0)} · "
          f"puntos de anclaje {info.get('anchors')}")
    if info.get("margins"):
        m = info["margins"]
        print(f"márgenes izq {m['left']} der {m['right']} sup {m['top']} inf {m['bottom']} · ocupación de la caja {info.get('bbox_fill_ratio')}")
    order = {"FAIL": 0, "WARN": 1, "INFO": 2}
    if not info["findings"]:
        print("✔ no se encontraron problemas")
    for f in sorted(info["findings"], key=lambda f: order[f["level"]]):
        icon = {"FAIL": "✖", "WARN": "▲", "INFO": "·"}[f["level"]]
        print(f"{icon} {f['level']:4s} [{f['code']}] {f['message']}")
    print(f"puntaje de listo para producción: {info['score']}/100 (heurístico)")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("files", nargs="+", help="uno o varios archivos SVG que quieres auditar")
    ap.add_argument("--json", action="store_true", help="salida en JSON, legible por máquina")
    ap.add_argument("--bg", help="color de fondo contra el cual probar el contraste, p. ej. '#ffffff'")
    a = ap.parse_args()
    results, rc = [], 0
    for p in a.files:
        try:
            results.append(audit(p, a.bg))
        except Exception as exc:
            rc = 1
            results.append({"file": p, "error": str(exc)})
    if a.json:
        print(json.dumps(results, indent=1, ensure_ascii=False))
    else:
        for r in results:
            if "error" in r:
                print(f"\n=== {r['file']}\n✖ no se pudo analizar: {r['error']}")
            else:
                print_report(r)
    return rc


if __name__ == "__main__":
    sys.exit(main())
