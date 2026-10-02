#!/usr/bin/env python3
"""Genera una hoja de pruebas en HTML para uno o varios SVG de logo (sin dependencias).

Muestra cada concepto en una escalera de tamaños (de 16 px hacia arriba), una prueba de favicon a nivel de píxel,
sobre fondos claros / oscuros / de color de marca / fotográficos / con patrón, con tratamientos que dejan ver las
debilidades (escala de grises, a una tinta en negro y en blanco, desenfoque de ojos entrecerrados, espejo, rotación
de 180°), en contextos reales (pestaña del navegador, ícono de app, recorte de avatar, encabezado de sitio web,
tarjeta de presentación), lado a lado con otros conceptos y en una "estantería" junto a logos de referencia
(competidores o ejemplos de la biblioteca) para juzgar qué tan distintivo es.

Uso:
  python3 scripts/preview_sheet.py concept-a.svg concept-b.svg -o preview.html
  python3 scripts/preview_sheet.py logo.svg --brand-color "#0F7C80" --name "Puerto" -o preview.html
  python3 scripts/preview_sheet.py logo.svg --refs-industry payments-fintech -o shelf.html
  python3 scripts/preview_sheet.py logo.svg --refs a.svg b.svg c.svg -o shelf.html
  python3 scripts/preview_sheet.py v1.svg v2.svg v3.svg --compare-only -o compare.html

Abre el HTML en un navegador (si eres un agente, usa la herramienta de navegador o de capturas de pantalla) y
obsérvalo de verdad.
"""
import argparse
import html
import json
import os
import random
import sys

sys.dont_write_bytecode = True  # mantiene limpia la carpeta de la skill (sin __pycache__)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import svglib  # noqa: E402

SIZES = [16, 20, 24, 32, 48, 64, 96, 128, 256]

CSS = """
:root{--ink:#1b1b1b;--muted:#6d6d6d;--line:#e4e4e0;--paper:#fafaf8}
*{box-sizing:border-box}body{margin:0;font:14px/1.45 system-ui,-apple-system,Segoe UI,sans-serif;color:var(--ink);background:var(--paper)}
header{padding:20px 24px;border-bottom:1px solid var(--line);background:#fff}h1{margin:0 0 4px;font-size:20px}
h2{font-size:17px;margin:28px 0 10px}h3{font-size:13px;text-transform:uppercase;letter-spacing:.06em;color:var(--muted);margin:18px 0 8px}
.wrap{padding:0 24px 40px;max-width:1400px}.row{display:flex;flex-wrap:wrap;gap:14px;align-items:flex-end}.row>.cell{flex:0 0 auto;max-width:100%}
.cell{display:flex;flex-direction:column;align-items:center;gap:6px}.cap{font-size:11px;color:var(--muted);text-align:center}
.tile{display:flex;align-items:center;justify-content:center;border-radius:10px;border:1px solid var(--line);overflow:hidden}
.checklist{background:#fff;border:1px solid var(--line);border-radius:10px;padding:12px 16px;margin-top:14px;columns:2;font-size:13px}
.checklist li{margin:2px 0}
.concept{border-top:2px solid var(--ink);margin-top:34px}
.pix canvas{image-rendering:pixelated;image-rendering:crisp-edges;border:1px solid var(--line);background:#fff}
.tab{width:260px;height:38px;background:#dfe1e5;border-radius:10px 10px 0 0;display:flex;align-items:center;gap:8px;padding:0 12px;font-size:12px;color:#333}
.tab img{width:16px;height:16px;object-fit:contain}
.phone{width:250px;padding:18px;border-radius:28px;background:linear-gradient(160deg,#3a4a5e,#1d2733);display:grid;grid-template-columns:repeat(4,1fr);gap:14px}
.app{display:flex;flex-direction:column;align-items:center;gap:4px;font-size:9px;color:#fff}
.app .ico{width:46px;height:46px;border-radius:11px;background:rgba(255,255,255,.18)}
.nav{width:520px;max-width:100%;height:64px;background:#fff;border:1px solid var(--line);border-radius:8px;display:flex;align-items:center;padding:0 18px;gap:26px;font-size:13px;color:#444}
.nav .sp{flex:1}.nav .btn{background:#1b1b1b;color:#fff;padding:7px 12px;border-radius:6px}
.card{width:336px;height:192px;border-radius:6px;box-shadow:0 6px 24px rgba(0,0,0,.15);background:#fff;padding:22px;display:flex;flex-direction:column;justify-content:space-between}
.card .t{font-size:11px;color:#444;line-height:1.5}
.avatar{width:96px;height:96px;border-radius:50%;overflow:hidden;display:flex;align-items:center;justify-content:center;border:1px solid var(--line)}
.shelf{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:10px}
.shelf .cell{align-items:stretch}.shelf .tile{height:110px;width:100%;background:#fff}.shelf .me{outline:3px solid #e8505b;outline-offset:2px}
.grey img{filter:grayscale(1)}
img.mono-black{filter:brightness(0)}img.mono-white{filter:brightness(0) invert(1)}
"""

CHECKLIST = """<ul class="checklist">
<li>¿La idea sigue clara a 16–24 px? ¿Qué detalles desaparecen primero?</li>
<li>¿La silueta sobrevive a la prueba de ojos entrecerrados (desenfoque)?</li>
<li>¿La versión a una tinta en negro sigue transmitiendo el concepto?</li>
<li>¿La versión invertida (blanco sobre oscuro) se ve más pesada? (irradiación → adelgázala)</li>
<li>¿Aparece alguna lectura no deseada al reflejarlo o rotarlo 180°?</li>
<li>¿Se sostiene sobre el color de marca, una foto y un patrón?</li>
<li>En las pruebas de favicon e ícono de app, ¿el símbolo tiene un tamaño y un centrado ópticamente correctos?</li>
<li>En la estantería: ¿destaca frente a las referencias o se pierde entre ellas?</li>
<li>Escala de grises: ¿los segmentos de color se siguen distinguiendo por su valor?</li>
<li>¿Lo reconocerías mañana de memoria?</li></ul>"""

PIX_JS = """
document.querySelectorAll('canvas[data-src]').forEach(c=>{
  const img=new Image(); const n=+c.dataset.n, k=+c.dataset.k; c.width=n*k; c.height=n*k;
  img.onload=()=>{const t=document.createElement('canvas'); t.width=n; t.height=n; const x=t.getContext('2d');
    x.fillStyle=c.dataset.bg; x.fillRect(0,0,n,n);
    const r=Math.min(n/img.width,n/img.height)*0.9, w=img.width*r, h=img.height*r; x.drawImage(img,(n-w)/2,(n-h)/2,w,h);
    const g=c.getContext('2d'); g.imageSmoothingEnabled=false; g.drawImage(t,0,0,n*k,n*k);};
  img.src=c.dataset.src;});
"""


def img(uri, h=None, w=None, cls="", style=""):
    dims = ""
    if h:
        dims += f"height:{h}px;"
    if w:
        dims += f"max-width:{w}px;"
    return f'<img src="{uri}" class="{cls}" style="{dims}{style}" alt="">'


def tile(inner, w, h, bg, extra=""):
    return f'<div class="tile" style="width:{w}px;height:{h}px;background:{bg};{extra}">{inner}</div>'


def concept_block(name, uri, aspect, brand, idx):
    square = aspect is None or aspect <= 1.35
    out = [f'<section class="concept"><h2>{html.escape(name)}</h2>']
    # escalera de tamaños
    out.append("<h3>Escalera de tamaños (altura en px)</h3><div class='row'>")
    for s in SIZES:
        out.append(f"<div class='cell'>{tile(img(uri, h=s), max(40, int(s * (aspect or 1)) + 16), s + 16, '#fff')}"
                   f"<div class='cap'>{s}px</div></div>")
    out.append("</div>")
    # prueba de píxeles
    out.append("<h3>Prueba de píxeles: renderizado a 16 / 32 / 48 px y ampliado</h3><div class='row pix'>")
    for n, k in ((16, 8), (32, 4), (48, 3)):
        for bg in ("#ffffff", "#111111"):
            out.append(f"<div class='cell'><canvas data-src='{uri}' data-n='{n}' data-k='{k}' data-bg='{bg}'></canvas>"
                       f"<div class='cap'>{n}px sobre {bg}</div></div>")
    out.append("</div>")
    # fondos
    photo = "radial-gradient(circle at 30% 30%,#e7b889,#8a5a3c 45%,#2d3b2f 80%)"
    pattern = "repeating-linear-gradient(45deg,#e9e4da 0 10px,#d4cbbd 10px 20px)"
    bgs = [("#ffffff", "blanco", ""), ("#f1f1ee", "gris claro", ""), ("#111111", "negro", "mono-white"),
           ("#111111", "negro (colores originales)", ""), (brand, f"color de marca {brand}", ""),
           (brand, "color de marca (en blanco)", "mono-white"), (photo, "tipo foto", ""), (pattern, "patrón", "")]
    out.append("<h3>Fondos</h3><div class='row'>")
    for bg, cap, cls in bgs:
        out.append(f"<div class='cell'>{tile(img(uri, h=72, w=200, cls=cls), 220, 120, bg)}<div class='cap'>{cap}</div></div>")
    out.append("</div>")
    # tratamientos ("@48" en la etiqueta hace que esa muestra se dibuje a 48 px)
    treats = [("original", "", ""), ("escala de grises", "", "filter:grayscale(1)"), ("a una tinta, negro", "mono-black", ""),
              ("a una tinta, blanco", "mono-white", ""), ("ojos entrecerrados (desenfoque 2px)", "", "filter:blur(2px)"),
              ("ojos entrecerrados, pequeño (desenfoque 1px @48)", "", "filter:blur(1px)"),
              ("reflejado", "", "transform:scaleX(-1)"), ("rotado 180°", "", "transform:rotate(180deg)")]
    out.append("<h3>Tratamientos</h3><div class='row'>")
    for cap, cls, st in treats:
        bg = "#111" if cls == "mono-white" else "#fff"
        h = 48 if "@48" in cap else 96
        out.append(f"<div class='cell'>{tile(img(uri, h=h, w=200, cls=cls, style=st), 220, 140, bg)}<div class='cap'>{cap}</div></div>")
    out.append("</div>")
    # contextos
    out.append("<h3>Contextos</h3><div class='row'>")
    out.append(f"<div class='cell'><div class='tab'>{img(uri)}<span>{html.escape(name)} — Inicio</span>"
               f"<span style='margin-left:auto'>✕</span></div><div class='cap'>pestaña del navegador (favicon de 16 px)</div></div>")
    icon = (f"<div class='ico' style='background:{brand};display:flex;align-items:center;justify-content:center'>"
            f"{img(uri, h=28, w=30, cls='mono-white')}</div>")
    apps = "".join("<div class='app'><div class='ico'></div>app</div>" for _ in range(6))
    out.append(f"<div class='cell'><div class='phone'>{apps}<div class='app'>{icon}{html.escape(name[:10])}</div>{apps[:0]}"
               + "".join("<div class='app'><div class='ico'></div>app</div>" for _ in range(5))
               + "</div><div class='cap'>ícono de app (símbolo blanco sobre el color de marca)</div></div>")
    out.append(f"<div class='cell'><div class='avatar' style='background:#fff'>{img(uri, h=58, w=70)}</div>"
               f"<div class='cap'>avatar con recorte circular</div></div>")
    out.append(f"<div class='cell'><div class='nav'>{img(uri, h=30 if not square else 34, w=180)}<span class='sp'></span>"
               f"<span>Producto</span><span>Precios</span><span>Nosotros</span><span class='btn'>Regístrate</span></div>"
               f"<div class='cap'>encabezado de sitio web</div></div>")
    out.append(f"<div class='cell'><div class='card'>{img(uri, h=40, w=160)}<div class='t'><b>Ana Ruiz</b><br>Fundadora<br>"
               f"ana@example.com · +00 000 000 000</div></div><div class='cap'>tarjeta de presentación (3.5 × 2 pulg.)</div></div>")
    out.append("</div></section>")
    return "\n".join(out)


def compare_block(items):
    out = ["<section><h2>Lado a lado</h2>"]
    for h, cls, bg, cap in ((96, "", "#fff", "96 px"), (32, "", "#fff", "32 px"), (64, "mono-black", "#fff", "a una tinta"),
                            (64, "mono-white", "#111", "versión invertida")):
        out.append(f"<h3>{cap}</h3><div class='row'>")
        for name, uri, aspect in items:
            w = max(60, int(h * (aspect or 1)) + 30)
            out.append(f"<div class='cell'>{tile(img(uri, h=h, cls=cls), w, h + 30, bg)}<div class='cap'>{html.escape(name)}</div></div>")
        out.append("</div>")
    out.append("</section>")
    return "\n".join(out)


def shelf_block(items, refs):
    cells = []
    for name, uri, _ in items:
        cells.append((name, uri, True))
    for p in refs:
        cells.append((os.path.basename(p), svglib.svg_data_uri(p), False))
    random.Random(7).shuffle(cells)
    out = ["<section><h2>Prueba de estantería</h2><p class='cap' style='text-align:left'>Tus conceptos, con contorno rojo, "
           "entre logos de referencia a la misma altura. Entrecierra los ojos: ¿destaca o se pierde entre los demás? "
           "La segunda fila repite todo en escala de grises.</p>"]
    for grey in (False, True):
        out.append(f"<div class='shelf{' grey' if grey else ''}' style='margin-bottom:12px'>")
        for name, uri, me in cells:
            out.append(f"<div class='cell'><div class='tile{' me' if me else ''}'>{img(uri, h=56, w=130)}</div>"
                       f"<div class='cap'>{html.escape(name)}</div></div>")
        out.append("</div>")
    out.append("</section>")
    return "\n".join(out)


def refs_for_industry(industry, n):
    with open(svglib.CATALOG_PATH, encoding="utf-8") as fh:
        cat = json.load(fh)
    rows = [r for r in cat if r.get("industry") == industry and r.get("variant") == "main"]
    rows.sort(key=lambda r: (not r.get("exemplary"), r["file"]))
    return [os.path.join(svglib.LIBRARY_SVG_DIR, r["file"]) for r in rows[:n]]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("files", nargs="+", help="SVG del logo que quieres probar (uno o varios)")
    ap.add_argument("-o", "--out", default="logo-preview.html", help="archivo HTML de salida")
    ap.add_argument("--name", help="nombre de la marca (se usa en los contextos simulados)")
    ap.add_argument("--names", nargs="*", help="etiqueta de cada archivo (por defecto: el nombre del archivo)")
    ap.add_argument("--brand-color", help="color de marca para las pruebas de fondos e ícono de app (por defecto: el color más saturado del primer logo; si no hay, gris oscuro)")
    ap.add_argument("--refs", nargs="*", default=[], help="SVG de referencia para la prueba de estantería")
    ap.add_argument("--refs-industry", help="toma de la biblioteca las referencias de la prueba de estantería, filtradas por sector")
    ap.add_argument("--refs-count", type=int, default=11, help="cuántas referencias tomar con --refs-industry")
    ap.add_argument("--compare-only", action="store_true", help="solo la sección de comparación lado a lado")
    a = ap.parse_args()

    items = []
    for i, p in enumerate(a.files):
        _, root = svglib.load_svg(p)
        vb = svglib.view_box(root)
        aspect = (vb[2] / vb[3]) if vb and vb[3] else None
        label = (a.names[i] if a.names and i < len(a.names) else os.path.splitext(os.path.basename(p))[0])
        items.append((label, svglib.svg_data_uri(p), aspect))
    brand_name = a.name or items[0][0]
    color_note = "indicado"
    if not a.brand_color:
        _, r0 = svglib.load_svg(a.files[0])
        cols = [c for c in svglib.collect_colors(r0) if 0.12 < svglib.lightness(c) < 0.9]
        if cols:
            import colorsys
            a.brand_color = max(cols, key=lambda c: colorsys.rgb_to_hls(*[v / 255 for v in svglib.hex_to_rgb(c)])[2])
            color_note = "tomado del logo"
        else:
            a.brand_color, color_note = "#3a3a3a", "no se indicó: gris neutro; usa --brand-color"
    refs = list(a.refs)
    if a.refs_industry:
        refs += refs_for_industry(a.refs_industry, a.refs_count)

    body = [f"<header><h1>Hoja de pruebas del logo — {html.escape(brand_name)}</h1>"
            f"<div class='cap' style='text-align:left'>{len(items)} archivo(s) · color de marca {a.brand_color} ({color_note}). "
            f"Revísala con ojo crítico; corrige lo que falle y vuelve a generarla.</div>{CHECKLIST}</header><div class='wrap'>"]
    if len(items) > 1 or a.compare_only:
        body.append(compare_block(items))
    if not a.compare_only:
        for i, (label, uri, aspect) in enumerate(items):
            body.append(concept_block(label, uri, aspect, a.brand_color, i))
    if refs:
        body.append(shelf_block(items, refs))
    body.append("</div>")
    doc = (f"<!doctype html><html lang='es'><head><meta charset='utf-8'><title>Pruebas del logo — {html.escape(brand_name)}</title>"
           f"<meta name='viewport' content='width=device-width,initial-scale=1'><style>{CSS}</style></head>"
           f"<body>{''.join(body)}<script>{PIX_JS}</script></body></html>")
    with open(a.out, "w", encoding="utf-8") as fh:
        fh.write(doc)
    print(f"se generó {a.out}  ({len(items)} logo(s), {len(refs)} referencia(s)); ábrelo en un navegador")


if __name__ == "__main__":
    main()
