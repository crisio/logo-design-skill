#!/usr/bin/env python3
"""Exporta las variantes de entrega estándar de un logo a partir de un solo SVG maestro (sin dependencias obligatorias).

Variantes SVG (junto al maestro, o en --out-dir):
  <nombre>-black.svg        a una tinta en negro (todos los colores -> #000000; los degradados se aplanan)
  <nombre>-white.svg        a una tinta en blanco, para fondos oscuros
  <nombre>-mono-<hex>.svg   a una tinta en un color de marca (--mono se puede repetir)
  <nombre>-square.svg       símbolo centrado en un lienzo de 256×256 con margen (avatar / maestro para redes sociales)
  <nombre>-favicon.svg      versión cuadrada ajustada para pestañas del navegador (sirve como favicon.svg)
  <nombre>-app-icon.svg     símbolo en blanco (o --icon-fg) sobre un fondo cuadrado redondeado (--icon-bg)

Rasterizado (requiere alguno de los renderizadores de render_png.py: cairosvg, rsvg-convert, inkscape,
Chrome/Chromium o Quick Look de macOS):
  --png 32 512 1024         PNG de cada variante SVG generada (fondo transparente)
  --web-icons               favicon.ico (16/32/48), favicon-16/32/48.png, apple-touch-icon.png (180),
                            icon-192.png, icon-512.png, maskable-512.png, además de site.webmanifest y
                            head-snippet.html: el set completo de íconos web/PWA

Uso:
  python3 scripts/export_variants.py brand-symbol.svg --mono "#0F7C80" --icon-bg "#0F7C80" --title "Logo de Puerto"
  python3 scripts/export_variants.py brand-horizontal.svg --only black white mono --mono "#0F7C80"
  python3 scripts/export_variants.py brand-symbol.svg --web-icons --icon-bg "#0F7C80" --out-dir dist/web
  python3 scripts/export_variants.py brand-symbol.svg --favicon-source brand-symbol-small.svg --web-icons

Notas:
- La conversión a una tinta reemplaza todos los colores de fill/stroke/stop. Las formas blancas usadas como
  falsos recortes se vuelven manchas: corrige el maestro con huecos reales (fill-rule="evenodd") o usa --keep-white.
- Los símbolos en versión invertida (en blanco) se ven más pesados (irradiación); para usos críticos, adelgaza
  a mano la geometría blanca.
- Los tamaños pequeños merecen un dibujo simplificado: pásalo con --favicon-source (se usa para el favicon,
  el ícono de app y los íconos web).
- Centrado óptico: --optical-offset -0.02 sube los símbolos de square/app-icon/favicon un 2 % del lienzo.
"""
import argparse
import json
import os
import re
import sys
import tempfile

sys.dont_write_bytecode = True  # mantiene limpia la carpeta de la skill (sin __pycache__)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import svglib  # noqa: E402
import render_png  # noqa: E402

PAINT_ATTR = re.compile(r'\b(fill|stroke|stop-color)\s*=\s*"([^"]*)"')
PAINT_CSS = re.compile(r'\b(fill|stroke|stop-color)\s*:\s*([^;"}]+)')


def recolor(raw, color, keep_white=False):
    def swap(value):
        v = value.strip()
        low = v.lower()
        if low in ("none", "transparent") or low.startswith("url("):
            return v
        norm = svglib.normalize_color(v) or (low if low == "currentcolor" else None)
        if norm is None:
            return v
        if keep_white and norm == "#ffffff":
            return v
        return color

    raw = PAINT_ATTR.sub(lambda m: f'{m.group(1)}="{swap(m.group(2))}"', raw)
    raw = PAINT_CSS.sub(lambda m: f"{m.group(1)}:{swap(m.group(2))}", raw)
    # Las formas sin color son negras por defecto; se da un fill a la raíz para que sigan el nuevo color.
    raw = re.sub(r"<svg\b(?![^>]*\bfill=)", f'<svg fill="{color}"', raw, count=1)
    return raw


def set_title(raw, title):
    if not title:
        return raw
    raw = re.sub(r"<title>.*?</title>", "", raw, flags=re.S)
    return re.sub(r"(<svg\b[^>]*>)", lambda m: m.group(1) + f"<title>{title}</title>", raw, count=1)


def inner_markup(raw):
    m = re.search(r"<svg\b[^>]*>(.*)</svg>", raw, re.S)
    body = m.group(1) if m else raw
    return re.sub(r"<title>.*?</title>", "", body, flags=re.S)


def square_wrap(raw, root, padding=0.1, bg=None, radius=0.0, fg=None, symbol_scale=None, offset=0.0, title=None):
    """Centra la caja delimitadora real del dibujo en un lienzo de 256×256 (opcionalmente sobre un fondo redondeado)."""
    vb = svglib.view_box(root)
    geo = svglib.document_geometry(root)
    bb = geo["bbox"] or (vb[0], vb[1], vb[0] + vb[2], vb[1] + vb[3])
    w, h = bb[2] - bb[0], bb[3] - bb[1]
    side = max(w, h)
    canvas = 256.0
    target = symbol_scale if symbol_scale else (1 - 2 * padding)
    s = round(canvas * target / side, 3)
    tx = round((canvas - w * s) / 2 - bb[0] * s, 2)
    ty = round((canvas - h * s) / 2 - bb[1] * s + offset * canvas, 2)
    src = recolor(raw, fg) if fg else raw
    body = inner_markup(src)
    root_tag = re.search(r"<svg\b[^>]*>", src)
    carried = ""
    if root_tag:
        for attr in ("fill", "stroke", "fill-rule", "clip-rule", "stroke-width", "stroke-linecap", "stroke-linejoin", "style"):
            m = re.search(r'\s%s\s*=\s*"([^"]*)"' % re.escape(attr), root_tag.group(0))
            if m:
                carried += f' {attr}="{m.group(1)}"'
    tile = f'<rect width="256" height="256" rx="{canvas * radius:g}" fill="{bg}"/>' if bg else ""
    t = f"<title>{title}</title>" if title else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256">{t}'
            f'{tile}<g transform="translate({tx:g} {ty:g}) scale({s:g})"{carried}>{body}</g></svg>')


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("master")
    ap.add_argument("--out-dir")
    ap.add_argument("--name", help="nombre base de los archivos de salida (por defecto: el nombre del archivo maestro)")
    ap.add_argument("--title", help="<title> accesible para cada archivo de salida, p. ej. 'Logo de Puerto'")
    ap.add_argument("--mono", action="append", default=[], help="versión(es) adicional(es) a una tinta, p. ej. '#0F7C80'")
    ap.add_argument("--icon-bg", default="#111111", help="color de fondo de app-icon / apple-touch / maskable")
    ap.add_argument("--icon-fg", default="#ffffff", help="color del símbolo sobre el fondo ('keep' = colores originales)")
    ap.add_argument("--icon-scale", type=float, default=0.62, help="tamaño del símbolo sobre el fondo de app-icon (lo típico: 0.55–0.7)")
    ap.add_argument("--optical-offset", type=float, default=0.0, help="ajuste vertical de las salidas cuadradas (fracción; negativo = hacia arriba)")
    ap.add_argument("--favicon-source", help="dibujo simplificado para tamaños pequeños, usado para favicon/app-icon/íconos web")
    ap.add_argument("--keep-white", action="store_true", help="deja intacto el blanco puro en las versiones a una tinta")
    ap.add_argument("--only", nargs="*", help="subconjunto: black white mono square favicon app-icon")
    ap.add_argument("--png", nargs="*", type=int, default=[], help="tamaños PNG para cada variante SVG generada")
    ap.add_argument("--web-icons", action="store_true", help="favicon.ico + set de íconos PNG + webmanifest + fragmento para el <head>")
    a = ap.parse_args()

    raw, root = svglib.load_svg(a.master)
    small_raw, small_root = svglib.load_svg(a.favicon_source) if a.favicon_source else (raw, root)
    out_dir = a.out_dir or os.path.dirname(os.path.abspath(a.master))
    os.makedirs(out_dir, exist_ok=True)
    base = a.name or os.path.splitext(os.path.basename(a.master))[0]
    want = set(a.only) if a.only else {"black", "white", "mono", "square", "favicon", "app-icon"}
    fg = None if a.icon_fg == "keep" else a.icon_fg
    written = []

    def write(suffix, content):
        p = os.path.join(out_dir, f"{base}-{suffix}.svg")
        with open(p, "w", encoding="utf-8") as fh:
            fh.write(content)
        written.append(p)
        return p

    if "black" in want:
        write("black", set_title(recolor(raw, "#000000", a.keep_white), a.title))
    if "white" in want:
        write("white", set_title(recolor(raw, "#ffffff"), a.title))
    if "mono" in want:
        for c in a.mono:
            hx = svglib.normalize_color(c)
            if not hx:
                print("se omitió un color no válido:", c)
                continue
            write(f"mono-{hx[1:]}", set_title(recolor(raw, hx, a.keep_white), a.title))
    if "square" in want:
        write("square", square_wrap(raw, root, padding=0.08, offset=a.optical_offset, title=a.title))
    if "favicon" in want:
        write("favicon", square_wrap(small_raw, small_root, padding=0.02, offset=a.optical_offset, title=a.title))
    if "app-icon" in want:
        write("app-icon", square_wrap(small_raw, small_root, bg=a.icon_bg, radius=0.225, fg=fg,
                                      symbol_scale=a.icon_scale, offset=a.optical_offset, title=a.title))

    colors = svglib.collect_colors(root)
    if any(svglib.lightness(c) > 0.97 for c in colors) and len(colors) > 1:
        print("nota: el maestro tiene partes en blanco; revisa que las versiones a una tinta no tengan manchas (falsos recortes).")

    raster = []
    if a.png:
        for p in list(written):
            for size in a.png:
                txt = open(p, encoding="utf-8").read()
                vb = re.search(r'viewBox\s*=\s*"[\d.\-]+[ ,]+[\d.\-]+[ ,]+([\d.]+)[ ,]+([\d.]+)"', txt)
                ratio = float(vb.group(1)) / float(vb.group(2)) if vb else 1.0
                w, h = (size, max(1, round(size / ratio))) if ratio >= 1 else (max(1, round(size * ratio)), size)
                png = p[:-4] + f"-{size}.png"
                if render_png.render(p, png, w, h):
                    raster.append(png)
                else:
                    print("se omitió la exportación a PNG: no hay renderizador (consulta: python3 scripts/render_png.py --which)")
                    break

    if a.web_icons:
        with tempfile.TemporaryDirectory() as tmp:
            fav_svg = os.path.join(tmp, "fav.svg")
            with open(fav_svg, "w", encoding="utf-8") as fh:
                fh.write(square_wrap(small_raw, small_root, padding=0.02, offset=a.optical_offset, title=a.title))
            tile_svg = os.path.join(tmp, "tile.svg")
            with open(tile_svg, "w", encoding="utf-8") as fh:
                fh.write(square_wrap(small_raw, small_root, bg=a.icon_bg, radius=0.0, fg=fg,
                                     symbol_scale=a.icon_scale, offset=a.optical_offset))
            mask_svg = os.path.join(tmp, "mask.svg")  # maskable: mantiene el símbolo dentro de la zona segura del 80 %
            with open(mask_svg, "w", encoding="utf-8") as fh:
                fh.write(square_wrap(small_raw, small_root, bg=a.icon_bg, radius=0.0, fg=fg,
                                     symbol_scale=min(a.icon_scale, 0.5), offset=a.optical_offset))
            jobs = [(fav_svg, "favicon-16.png", 16), (fav_svg, "favicon-32.png", 32), (fav_svg, "favicon-48.png", 48),
                    (tile_svg, "apple-touch-icon.png", 180), (tile_svg, "icon-192.png", 192),
                    (tile_svg, "icon-512.png", 512), (mask_svg, "maskable-512.png", 512)]
            ok = True
            for src, fname, size in jobs:
                dst = os.path.join(out_dir, fname)
                if render_png.render(src, dst, size, size):
                    raster.append(dst)
                else:
                    ok = False
                    print(f"se omitieron los íconos web: no se pudo renderizar {fname} (consulta: python3 scripts/render_png.py --which)")
                    break
            if ok:
                ico = os.path.join(out_dir, "favicon.ico")
                render_png.write_ico([os.path.join(out_dir, f"favicon-{s}.png") for s in (16, 32, 48)], ico)
                raster.append(ico)
                fav_copy = os.path.join(out_dir, "favicon.svg")
                with open(fav_svg, encoding="utf-8") as src, open(fav_copy, "w", encoding="utf-8") as dst:
                    dst.write(src.read())
                raster.append(fav_copy)
                manifest = {"name": a.title or base, "icons": [
                    {"src": "/icon-192.png", "sizes": "192x192", "type": "image/png"},
                    {"src": "/icon-512.png", "sizes": "512x512", "type": "image/png"},
                    {"src": "/maskable-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"}],
                    "theme_color": a.icon_bg, "background_color": a.icon_bg, "display": "standalone"}
                with open(os.path.join(out_dir, "site.webmanifest"), "w", encoding="utf-8") as fh:
                    json.dump(manifest, fh, indent=2)
                with open(os.path.join(out_dir, "head-snippet.html"), "w", encoding="utf-8") as fh:
                    fh.write('<link rel="icon" href="/favicon.ico" sizes="48x48">\n'
                             '<link rel="icon" href="/favicon.svg" type="image/svg+xml">\n'
                             '<link rel="apple-touch-icon" href="/apple-touch-icon.png">\n'
                             '<link rel="manifest" href="/site.webmanifest">\n'
                             f'<meta name="theme-color" content="{a.icon_bg}">\n')
                raster += [os.path.join(out_dir, "site.webmanifest"), os.path.join(out_dir, "head-snippet.html")]

    for p in written + raster:
        print("se generó", p)


if __name__ == "__main__":
    main()
