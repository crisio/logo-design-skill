#!/usr/bin/env python3
"""Arma el kit de un Kot: la mascota de peluche animada de un agente, a partir de su personaje 3D (PNG transparente).

Pasos:
  1. Limpia el PNG: alfa 255 en el cuerpo (como check_alpha.py --opacar) y el brillo de la familia en los ojos (como
     eye_highlight.py), salvo que ya lo tenga.
  2. Detecta los ojos y el color del párpado, y guarda kot.json (ojos, caja del personaje, colores).
  3. Tamaños: kot-1024.png, kot-512.png, kot-256.png y la foto para Telegram (kot-telegram-1024.png, con fondo).
  4. Animación grabada de 3 s en loop: kot-animado.webp (con transparencia, para web) y kot-sticker.webm (sticker
     animado de Telegram: VP9 con transparencia, 512 px, 3 s, ≤ 256 KB). Los cuadros salen del mismo componente
     <kot-avatar> que se usa en vivo, capturados con Chrome.
  5. Web: kot-avatar.js (componente sin dependencias) y kot.html (demo en vivo), y una hoja de cuadros para revisar.
  6. Familia (opcional): agrega el Kot a familia.json y regenera familia.html con todos los Kots en vivo.

Necesita: Python 3.8+ (sin dependencias). Para tamaños y animaciones usa, si están instalados, ffmpeg, img2webp
(libwebp) y Chrome/Chromium; si faltan, lo dice y arma el resto.

Uso:
  python3 scripts/kot_build.py --nombre Hilo --personaje hilo-personaje.png --color "#1B9E73" --fondo "#E9F6F1" \\
      --salida marcas/tracking-gc/kot --familia marcas/kots
  python3 scripts/kot_build.py … --sin-animacion        # solo datos, tamaños y web
"""
import argparse
import datetime
import html
import json
import os
import pathlib
import re
import shutil
import signal
import subprocess
import sys
import struct
import tempfile
import urllib.parse
import zlib

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import check_alpha as ca  # noqa: E402
import eye_highlight as eh  # noqa: E402

COMPONENTE = os.path.join(os.path.dirname(AQUI), "assets", "kots", "kot-avatar.js")
CICLO_MS, FPS = 3000, 24
CUADROS = CICLO_MS * FPS // 1000          # 72
LIMITE_STICKER = 256 * 1024


def aviso(msg):
    print(f"· {msg}")


def ejecutar(cmd, timeout=300, **kw):
    """Corre un programa externo con límite de tiempo; si se pasa, devuelve un resultado fallido en vez de colgarse."""
    try:
        return subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout, **kw)
    except subprocess.TimeoutExpired:
        aviso(f"{os.path.basename(cmd[0])} tardó más de {timeout} s y se detuvo")
        return subprocess.CompletedProcess(cmd, 124, b"", b"timeout")


def normalizar_color(valor, nombre):
    """Acepta #RGB o #RRGGBB (con o sin #) y devuelve #RRGGBB; si no, termina con un mensaje claro."""
    m = re.fullmatch(r"#?([0-9A-Fa-f]{3}|[0-9A-Fa-f]{6})", (valor or "").strip())
    if not m:
        raise SystemExit(f"--{nombre} tiene que ser un color HEX como #1B9E73 (recibí «{valor}»)")
    h = m.group(1)
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return "#" + h.upper()


def color_hex(rgb):
    return "#{:02X}{:02X}{:02X}".format(*[max(0, min(255, round(c))) for c in rgb])


def tiene_brillo(ancho, datos, ojo):
    """True si dentro del óvalo del ojo ya hay píxeles casi blancos (un brillo previo)."""
    x0, y0, x1, y1 = ojo["caja"]
    cx, cy = (x0 + x1 + 1) / 2, (y0 + y1 + 1) / 2
    rx, ry = (x1 - x0 + 1) / 2, (y1 - y0 + 1) / 2
    dentro = claros = 0
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            if ((x + 0.5 - cx) / rx) ** 2 + ((y + 0.5 - cy) / ry) ** 2 > 1:
                continue
            dentro += 1
            k = 4 * (y * ancho + x)
            if datos[k] + datos[k + 1] + datos[k + 2] > 600:
                claros += 1
    return dentro > 0 and claros / dentro > 0.01


def color_parpado(ancho, alto, datos, ojo):
    """Promedio del fieltro justo encima del ojo (anillo superior), que es de donde baja el párpado."""
    x0, y0, x1, y1 = ojo["caja"]
    cx, cy = (x0 + x1 + 1) / 2, (y0 + y1 + 1) / 2
    rx, ry = (x1 - x0 + 1) / 2, (y1 - y0 + 1) / 2
    suma, n = [0, 0, 0], 0
    for y in range(max(0, int(cy - ry * 1.7)), int(cy)):
        for x in range(max(0, int(cx - rx * 1.7)), min(ancho, int(cx + rx * 1.7) + 1)):
            d = ((x + 0.5 - cx) / rx) ** 2 + ((y + 0.5 - cy) / ry) ** 2
            if not (1.35 ** 2 <= d <= 1.7 ** 2):
                continue
            k = 4 * (y * ancho + x)
            if datos[k + 3] < 250:
                continue
            for c in range(3):
                suma[c] += datos[k + c]
            n += 1
    return color_hex([s / n for s in suma]) if n else "#808080"


def muestra_fieltro(ancho, alto, datos, ojo, lado_preferido):
    """Desplazamiento (dx, dy) en píxeles hacia un parche de fieltro limpio para tapar el ojo al parpadear.

    Prueba primero a los costados (misma altura: la luz coincide), después arriba y abajo. El parche, del tamaño del
    ojo ampliado, tiene que ser todo opaco, sin píxeles oscuros de ojo y de un color parecido al fieltro que rodea al ojo."""
    x0, y0, x1, y1 = ojo["caja"]
    cx, cy = (x0 + x1 + 1) / 2, (y0 + y1 + 1) / 2
    rx, ry = (x1 - x0 + 1) / 2 * 1.5, (y1 - y0 + 1) / 2 * 1.35
    ref = [int(color_parpado(ancho, alto, datos, ojo)[i:i + 2], 16) for i in (1, 3, 5)]
    candidatos = []
    for f in (1.8, 2.1, 2.5, 3.2, 4.0):
        horiz = [(-lado_preferido * f * rx, 0), (lado_preferido * f * rx, 0)]
        diag = [(lado_preferido * f * rx * 0.8, f * ry * 0.6), (lado_preferido * f * rx * 0.8, -f * ry * 0.6)]
        candidatos += horiz + diag + [(0, -f * ry), (0, f * ry)]
    mejor, mejor_d = None, 1e9
    for dx, dy in candidatos:
        sx, sy = cx + dx, cy + dy
        if sx - rx < 0 or sy - ry < 0 or sx + rx >= ancho or sy + ry >= alto:
            continue
        ok, suma, n = True, [0, 0, 0], 0
        paso = max(1, int(min(rx, ry) / 8))
        for y in range(int(sy - ry), int(sy + ry) + 1, paso):
            for x in range(int(sx - rx), int(sx + rx) + 1, paso):
                if ((x + 0.5 - sx) / rx) ** 2 + ((y + 0.5 - sy) / ry) ** 2 > 1:
                    continue
                k = 4 * (y * ancho + x)
                r_, g_, b_, a_ = datos[k], datos[k + 1], datos[k + 2], datos[k + 3]
                if a_ < 250 or max(r_, g_, b_) <= 75:
                    ok = False
                    break
                suma[0] += r_; suma[1] += g_; suma[2] += b_; n += 1
            if not ok:
                break
        if not ok or not n:
            continue
        prom = [s / n for s in suma]
        d = sum((p - q) ** 2 for p, q in zip(prom, ref)) ** 0.5 + abs(dy) / max(ry, 1) * 6  # preferir la misma altura
        if d < mejor_d:
            mejor, mejor_d = (dx, dy), d
    return mejor


def validar_ojos(ancho, alto, datos, ojos):
    """Evita ojos falsos (sombras de un fieltro oscuro): pequeños, parecidos entre sí, a la misma altura y arriba."""
    alfa = bytes(datos[3::4])
    filas = [y for y in range(0, alto, 4) if max(alfa[y * ancho:(y + 1) * ancho]) > ca.UMBRAL_OPACO]
    alto_pj = (filas[-1] - filas[0]) if filas else alto
    medidas = []
    for o in ojos:
        x0, y0, x1, y1 = o["caja"]
        medidas.append((x1 - x0 + 1, y1 - y0 + 1, (y0 + y1) / 2))
    (w1, h1, c1), (w2, h2, c2) = medidas
    problemas = []
    if max(w1, w2) > 0.12 * ancho or max(h1, h2) > 0.2 * alto:
        problemas.append("son demasiado grandes para ser ojos")
    if max(w1 * h1, w2 * h2) > 2.2 * min(w1 * h1, w2 * h2):
        problemas.append("tienen tamaños muy distintos")
    if abs(c1 - c2) > 0.12 * alto_pj:
        problemas.append("están a alturas muy distintas")
    if problemas:
        raise SystemExit("lo que detecté como ojos no parece ojos (" + ", ".join(problemas) + "). Pasa cuando las sombras "
                         "del cuerpo son tan oscuras como los ojos: genera una variante con ojos más marcados o un fieltro "
                         "más claro.")


def preparar_png(ruta, sin_brillo=False):
    ancho, alto, prof, tipo, px, _, _ = ca.leer_png(ruta)
    if tipo != 6 or prof != 8:
        raise SystemExit("el personaje tiene que ser un PNG RGBA de 8 bits (como los que entrega check_alpha.py)")
    datos = bytearray(px)
    if ancho != alto:
        # El Kot siempre es cuadrado: se centra en un lienzo transparente para no deformarlo después
        lado = max(ancho, alto)
        cuadrado = bytearray(lado * lado * 4)
        ox, oy = (lado - ancho) // 2, (lado - alto) // 2
        for y in range(alto):
            ini = ((y + oy) * lado + ox) * 4
            cuadrado[ini:ini + ancho * 4] = datos[y * ancho * 4:(y + 1) * ancho * 4]
        aviso(f"el personaje medía {ancho}×{alto}: se centró en un cuadrado de {lado}×{lado}")
        datos, ancho, alto = cuadrado, lado, lado
    tabla = bytes(255 if v >= 240 else v for v in range(256))
    datos[3::4] = bytes(datos[3::4]).translate(tabla)
    try:
        ojos = eh.ojos(ancho, alto, datos)
    except SystemExit:
        raise SystemExit("no encontré los dos ojos del personaje (dos óvalos oscuros pequeños). Revisa que el personaje "
                         "tenga ojos lisos y oscuros sobre un fieltro más claro, o genera otra variante.")
    validar_ojos(ancho, alto, datos, ojos)
    con_brillo = [tiene_brillo(ancho, datos, o) for o in ojos]
    brillo_previo = all(con_brillo)
    parpados = [color_parpado(ancho, alto, datos, o) for o in ojos]
    # Parche de fieltro para el parpadeo: el ojo de la izquierda mira primero a su izquierda y el otro a su derecha
    muestras = [muestra_fieltro(ancho, alto, datos, o, -1 if i == 0 else 1) for i, o in enumerate(ojos)]
    if not sin_brillo and not brillo_previo:
        for o, ya in zip(ojos, con_brillo):
            if ya:
                continue
            x0, y0, x1, y1 = o["caja"]
            w, h = x1 - x0 + 1, y1 - y0 + 1
            eh.pintar(ancho, datos, o, x0 + 0.38 * w, y0 + 0.27 * h, 0.17 * w, 0.88)
            eh.pintar(ancho, datos, o, x0 + 0.62 * w, y0 + 0.64 * h, 0.08 * w, 0.5)
        aviso("brillo de la familia agregado a los ojos")
    elif brillo_previo:
        aviso("los ojos ya tenían brillo: no se agregó otro")
    # Caja del personaje
    alfa = bytes(datos[3::4])
    x0, y0, x1, y1 = ancho, alto, -1, -1
    for y in range(alto):
        fila = alfa[y * ancho:(y + 1) * ancho]
        if max(fila) > ca.UMBRAL_OPACO:
            iz = next(i for i, v in enumerate(fila) if v > ca.UMBRAL_OPACO)
            de = ancho - 1 - next(i for i, v in enumerate(reversed(fila)) if v > ca.UMBRAL_OPACO)
            x0, x1, y0, y1 = min(x0, iz), max(x1, de), min(y0, y), y
    ojos_json = []
    for o, color, m in zip(ojos, parpados, muestras):
        ox0, oy0, ox1, oy1 = o["caja"]
        ojo = {"cx": round((ox0 + ox1 + 1) / 2 / ancho, 5), "cy": round((oy0 + oy1 + 1) / 2 / alto, 5),
               "rx": round((ox1 - ox0 + 1) / 2 / ancho, 5), "ry": round((oy1 - oy0 + 1) / 2 / alto, 5),
               "parpado": color}
        if m:
            ojo["muestra"] = [round(m[0] / ancho, 5), round(m[1] / alto, 5)]
        else:
            aviso("no encontré fieltro limpio junto a un ojo: ese ojo parpadea con un párpado de color plano")
        ojos_json.append(ojo)
    caja = [round(x0 / ancho, 5), round(y0 / alto, 5), round((x1 + 1) / ancho, 5), round((y1 + 1) / alto, 5)]
    return ancho, alto, datos, ojos_json, caja


def ffmpeg():
    return shutil.which("ffmpeg")


def redimensionar(origen, destino, lado):
    r = ejecutar([ffmpeg(), "-y", "-v", "error", "-i", origen, "-vf", f"scale={lado}:{lado}:flags=lanczos",
                  "-frames:v", "1", destino])
    return r.returncode == 0


def foto_telegram(origen, destino, fondo, lado=1024):
    """Personaje centrado sobre el fondo suave de la paleta (Telegram no respeta la transparencia)."""
    k = round(lado * 0.9)
    filtro = (f"color=c=0x{fondo.lstrip('#')}:s={lado}x{lado}[f];[0:v]scale={k}:{k}:flags=lanczos[k];"
              f"[f][k]overlay=(W-w)/2:(H-h)/2+{round(lado * 0.02)}:format=auto")
    r = ejecutar([ffmpeg(), "-y", "-v", "error", "-i", origen, "-filter_complex", filtro, "-frames:v", "1", destino])
    return r.returncode == 0


def atributo_kot(datos_kot):
    return html.escape(json.dumps({"ojos": datos_kot["ojos"], "caja": datos_kot["caja"]}, ensure_ascii=False), quote=True)


def hoja_cuadros(ruta, src, datos_kot, indices, lado, columnas, sombra):
    filas = (len(indices) + columnas - 1) // columnas
    celdas = "".join(
        f'<kot-avatar src="{html.escape(src)}" kot="{atributo_kot(datos_kot)}" tiempo="{round(i * 1000 / FPS, 3)}"'
        f'{" sombra" if sombra else ""} style="width:{lado}px;height:{lado}px"></kot-avatar>' for i in indices)
    doc = (f'<!doctype html><html><head><meta charset="utf-8"><style>html,body{{margin:0;background:transparent}}'
           f'body{{width:{columnas * lado}px;height:{filas * lado}px;display:grid;'
           f'grid-template-columns:repeat({columnas},{lado}px);grid-auto-rows:{lado}px}}'
           f'kot-avatar{{display:block}}</style></head><body>{celdas}'
           f'<script src="kot-avatar.js"></script></body></html>')
    with open(ruta, "w", encoding="utf-8") as fh:
        fh.write(doc)
    return columnas * lado, filas * lado


def capturar(html_ruta, png_ruta, ancho, alto):
    r = ejecutar([sys.executable, os.path.join(AQUI, "render_png.py"), html_ruta, "-o", png_ruta,
                  "--width", str(ancho), "--height", str(alto)],
                 env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"))
    return r.returncode == 0 and os.path.exists(png_ruta)


def patron(carpeta, nombre):
    """Ruta de patrón para ffmpeg (c%03d.png): los % literales de la carpeta se escriben %%."""
    return os.path.join(carpeta.replace("%", "%%"), nombre)


def tiene_vp9():
    r = ejecutar([ffmpeg(), "-hide_banner", "-encoders"], timeout=30)
    return b"libvpx-vp9" in (r.stdout or b"")


GENERADOS = ("kot-1024.png", "kot-512.png", "kot-256.png", "kot-telegram-1024.png", "kot-animado.webp",
             "kot-sticker.webm", "kot-sticker-excede.webm", "kot-cuadros.png")


def limpiar_generados(salida):
    """Borra lo que dejó una corrida anterior para no mezclar archivos de dos personajes."""
    for viejo in GENERADOS:
        ruta = os.path.join(salida, viejo)
        if os.path.exists(ruta):
            os.remove(ruta)


def animar(salida, datos_kot, lado, sombra, lado_webp=320):
    if not ffmpeg():
        aviso("sin ffmpeg: no se generó la animación (instálalo y vuelve a correr)")
        return {}
    tmp = tempfile.mkdtemp(prefix="kot-")
    try:
        shutil.copy(os.path.join(salida, "kot-avatar.js"), tmp)
        fuente = os.path.join(salida, "kot-1024.png")
        if not os.path.exists(fuente):
            fuente = os.path.join(salida, "kot.png")
        shutil.copy(fuente, os.path.join(tmp, "kot.png"))
        cuadros_dir = os.path.join(tmp, "cuadros")
        os.makedirs(cuadros_dir)
        columnas, por_hoja = 6, 36
        for h in range(0, CUADROS, por_hoja):
            indices = list(range(h, min(CUADROS, h + por_hoja)))
            hoja_html = os.path.join(tmp, f"hoja-{h // por_hoja}.html")
            hoja_png = os.path.join(tmp, f"hoja-{h // por_hoja}.png")
            ancho, alto = hoja_cuadros(hoja_html, "kot.png", datos_kot, indices, lado, columnas, sombra)
            if not capturar(hoja_html, hoja_png, ancho, alto):
                aviso("no se pudo capturar la animación con Chrome: se omitió")
                return {}
            for j, i in enumerate(indices):
                x, y = (j % columnas) * lado, (j // columnas) * lado
                ejecutar([ffmpeg(), "-y", "-v", "error", "-i", hoja_png, "-vf", f"crop={lado}:{lado}:{x}:{y}",
                          "-frames:v", "1", os.path.join(cuadros_dir, f"c{i:03d}.png")])
            if h <= 50 < h + por_hoja:   # la hoja que incluye el parpadeo (cierre total en el cuadro 50)
                shutil.copy(hoja_png, os.path.join(salida, "kot-cuadros.png"))
        cuadros = [os.path.join(cuadros_dir, f"c{i:03d}.png") for i in range(CUADROS)]
        if not all(os.path.exists(c) for c in cuadros):
            aviso("faltaron cuadros de la animación: se omitió")
            return {}
        hecho = {}
        img2webp = shutil.which("img2webp")
        if img2webp:
            webp = os.path.join(salida, "kot-animado.webp")
            web_dir = os.path.join(tmp, "web")
            os.makedirs(web_dir)
            lado_web = min(lado, lado_webp)
            ejecutar([ffmpeg(), "-y", "-v", "error", "-i", patron(cuadros_dir, "c%03d.png"),
                      "-vf", f"scale={lado_web}:{lado_web}:flags=lanczos", patron(web_dir, "w%03d.png")])
            cuadros_web = [os.path.join(web_dir, f"w{i + 1:03d}.png") for i in range(CUADROS)]
            if not all(os.path.exists(c) for c in cuadros_web):
                cuadros_web = cuadros
            # Duración por cuadro que suma exactamente 3000 ms (alterna 42 y 41 ms)
            args = [img2webp, "-loop", "0", "-lossy", "-q", "75", "-m", "4"]
            for i, c in enumerate(cuadros_web):
                args += ["-d", str(round((i + 1) * 1000 / FPS) - round(i * 1000 / FPS)), c]
            r = ejecutar(args + ["-o", webp])
            if r.returncode == 0:
                hecho["webp"] = webp
        else:
            aviso("sin img2webp (libwebp): no se generó kot-animado.webp")
        sticker = os.path.join(salida, "kot-sticker.webm")
        if not tiene_vp9():
            aviso("ffmpeg no tiene el códec libvpx-vp9: no se generó el sticker de Telegram")
            return hecho
        for crf in (34, 40, 46, 52, 58, 63):
            r = ejecutar([ffmpeg(), "-y", "-v", "error", "-framerate", str(FPS), "-i", patron(cuadros_dir, "c%03d.png"),
                          "-vf", "scale=512:512:flags=lanczos", "-c:v", "libvpx-vp9", "-pix_fmt", "yuva420p", "-b:v", "0",
                          "-crf", str(crf), "-deadline", "good", "-an", "-t", "3", sticker])
            if r.returncode != 0:
                aviso("ffmpeg no pudo generar el sticker: " + (r.stderr or b"").decode("utf-8", "replace").strip()[-200:])
                break
            if os.path.getsize(sticker) <= LIMITE_STICKER:
                hecho["sticker"] = sticker
                hecho["sticker_crf"] = crf
                break
        else:
            os.replace(sticker, os.path.join(salida, "kot-sticker-excede.webm"))
            hecho["excede"] = True
            aviso("el sticker quedó por encima de 256 KB incluso con la compresión máxima: se guardó como "
                  "kot-sticker-excede.webm y no sirve para Telegram")
        return hecho
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def demo_html(salida, datos_kot, animado, tamanos):
    n = html.escape(datos_kot["nombre"])
    grande = "kot-1024.png" if tamanos else "kot.png"
    chico = "kot-256.png" if tamanos else "kot.png"
    fondo = datos_kot["fondo"]
    kot = atributo_kot(datos_kot)
    extra = ""
    if animado.get("webp") or animado.get("sticker"):
        extra = '<section><h2>Animación grabada</h2><div class="fila">'
        if animado.get("webp"):
            extra += '<figure><img src="kot-animado.webp" width="200" height="200" alt=""><figcaption>kot-animado.webp</figcaption></figure>'
        if animado.get("sticker"):
            extra += ('<figure><video src="kot-sticker.webm" width="200" height="200" autoplay loop muted playsinline></video>'
                      '<figcaption>kot-sticker.webm (Telegram)</figcaption></figure>')
        extra += "</div></section>"
    doc = f"""<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Kot · {n}</title><style>
:root{{--fondo:{fondo}}}body{{margin:0;font:15px/1.5 system-ui,-apple-system,"Segoe UI",sans-serif;color:#1d2027;background:#fff}}
main{{max-width:960px;margin:0 auto;padding:28px 20px 60px}}h1{{font-size:26px;margin:0 0 4px}}h2{{font-size:16px;margin:28px 0 10px}}
.escena{{background:var(--fondo);border-radius:20px;display:grid;place-items:center;padding:24px}}
.fila{{display:flex;gap:18px;flex-wrap:wrap;align-items:center}}.osc{{background:#17212B;border-radius:14px;padding:14px}}
.cla{{background:#fff;border:1px solid #e3e6eb;border-radius:14px;padding:14px}}figure{{margin:0;text-align:center}}
figcaption{{font-size:12px;color:#777}}pre{{background:#f4f6f9;border-radius:10px;padding:12px;overflow:auto;font-size:13px}}
kot-avatar[circulo]{{--kot-fondo:var(--fondo)}}</style></head><body><main>
<h1>Kot · {n}</h1><p>Pasa el mouse y toca al Kot. Si tienes «reducir movimiento» activado, se queda quieto.</p>
<div class="escena"><kot-avatar src="{grande}" kot="{kot}" alt="{n}" sombra style="width:min(360px,70vw)"></kot-avatar></div>
<section><h2>Como avatar</h2><div class="fila"><div class="cla fila"><kot-avatar src="{chico}" kot="{kot}" circulo style="width:96px"></kot-avatar>
<kot-avatar src="{chico}" kot="{kot}" circulo style="width:40px"></kot-avatar></div><div class="osc fila">
<kot-avatar src="{chico}" kot="{kot}" circulo style="width:96px"></kot-avatar><kot-avatar src="{chico}" kot="{kot}" circulo style="width:40px"></kot-avatar></div></div></section>
{extra}
<section><h2>Úsalo en una página</h2><pre>&lt;script src="kot-avatar.js" defer&gt;&lt;/script&gt;
&lt;kot-avatar src="{"kot-512.png" if tamanos else "kot.png"}" alt="{n}" kot='{html.escape(json.dumps({"ojos": datos_kot["ojos"], "caja": datos_kot["caja"]}, ensure_ascii=False))}' style="width:160px"&gt;&lt;/kot-avatar&gt;</pre></section>
</main><script src="kot-avatar.js"></script></body></html>"""
    with open(os.path.join(salida, "kot.html"), "w", encoding="utf-8") as fh:
        fh.write(doc)


def leeme(salida, datos_kot, animado, tamanos, telegram):
    n = datos_kot["nombre"]
    lineas = [f"# Kot · {n}", "",
              f"La mascota de peluche de {n}, lista para web, Telegram y presentaciones. La generó `kot_build.py`.", "",
              "| Archivo | Para qué |", "|---|---|",
              f"| `kot.png` | Original, {datos_kot['ancho']} px, fondo transparente, con el brillo de la familia en los ojos |"]
    if tamanos:
        lineas.append("| `kot-1024.png` · `kot-512.png` · `kot-256.png` | Tamaños con fondo transparente |")
    if telegram:
        lineas.append("| `kot-telegram-1024.png` | Foto del bot de Telegram (con fondo: Telegram no respeta la transparencia) |")
    lineas += [
              "| `kot.json` | Datos del Kot: ojos, color del párpado, caja, colores |",
              "| `kot-avatar.js` | Componente web sin dependencias: flota, respira, parpadea y reacciona al cursor |",
              "| `kot.html` | Demo en vivo (ábrela en el navegador) |"]
    if animado.get("webp"):
        lineas.append("| `kot-animado.webp` | Animación de 3 s en loop con transparencia, para web (320 px) |")
    if animado.get("sticker"):
        lineas.append("| `kot-sticker.webm` | Sticker animado de Telegram (VP9 con transparencia, 512 px, 3 s, ≤ 256 KB) |")
    if animado.get("excede"):
        lineas.append("| `kot-sticker-excede.webm` | Sticker que pasó de 256 KB: no sirve para Telegram (simplifica el personaje) |")
    if animado.get("cuadros"):
        lineas.append("| `kot-cuadros.png` | Hoja de 36 cuadros de la animación (incluye el parpadeo), para revisarla |")
    imagen_web = "kot-512.png" if tamanos else "kot.png"
    lineas += ["", "## En una página web", "", "```html", '<script src="kot-avatar.js" defer></script>',
               f"<kot-avatar src=\"{imagen_web}\" alt=\"{n}\" kot='{json.dumps({'ojos': datos_kot['ojos'], 'caja': datos_kot['caja']}, ensure_ascii=False)}' style=\"width:160px\"></kot-avatar>",
               "```", "",
               "Atributos opcionales: `sombra` (sombra suave), `circulo` (recorte circular con fondo `--kot-fondo`), "
               "`quieto` (sin animación), `alt` (nombre para lectores de pantalla). Respeta «reducir movimiento»."]
    if telegram or animado.get("sticker"):
        lineas += ["", "## En Telegram", ""]
        if telegram:
            lineas.append("- **Foto del bot:** @BotFather → `/mybots` → el bot → Edit Bot → Edit Botpic → `kot-telegram-1024.png`.")
        if animado.get("sticker"):
            lineas.append("- **Sticker animado:** en @Stickers → `/newvideo` → sube `kot-sticker.webm` y elige un emoji. "
                          "Después el bot puede mandar el sticker.")
    with open(os.path.join(salida, "LEEME.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(lineas) + "\n")


def familia(dir_familia, salida, datos_kot):
    os.makedirs(dir_familia, exist_ok=True)
    reg_ruta = os.path.join(dir_familia, "familia.json")
    reg = []
    if os.path.exists(reg_ruta):
        try:
            with open(reg_ruta, encoding="utf-8-sig") as fh:
                reg = json.load(fh)
        except (OSError, ValueError):
            reg = None
        if not isinstance(reg, list):
            raise SystemExit(f"{reg_ruta} no es válido: corrígelo o bórralo y vuelve a correr (el kit del Kot ya se generó)")
    try:
        carpeta = os.path.relpath(os.path.abspath(salida), os.path.abspath(dir_familia))
    except ValueError:   # Windows: discos distintos
        carpeta = os.path.abspath(salida)
    carpeta = carpeta.replace(os.sep, "/")
    validos = [k for k in reg if isinstance(k, dict) and isinstance(k.get("nombre"), str) and k.get("carpeta")]
    if len(validos) != len(reg):
        aviso(f"se ignoraron {len(reg) - len(validos)} entradas inválidas de familia.json")
    reg = [k for k in validos if k["nombre"] != datos_kot["nombre"]]
    reg.append({"nombre": datos_kot["nombre"], "carpeta": carpeta, "color": datos_kot["color"], "fondo": datos_kot["fondo"]})
    reg.sort(key=lambda k: k["nombre"].lower())
    try:
        with open(reg_ruta + ".tmp", "w", encoding="utf-8") as fh:
            json.dump(reg, fh, ensure_ascii=False, indent=2)
        os.replace(reg_ruta + ".tmp", reg_ruta)
    finally:
        if os.path.exists(reg_ruta + ".tmp"):
            os.remove(reg_ruta + ".tmp")
    shutil.copy(COMPONENTE, os.path.join(dir_familia, "kot-avatar.js"))
    tarjetas = ""
    for k in reg:
        carpeta_k = str(k.get("carpeta", "")).replace("\\", "/")
        absoluta = os.path.isabs(carpeta_k) or re.match(r"^[A-Za-z]:/", carpeta_k)
        base = carpeta_k if absoluta else os.path.join(dir_familia, *carpeta_k.split("/"))
        ruta_json = os.path.join(base, "kot.json")
        if not os.path.exists(ruta_json):
            aviso(f"el Kot «{k.get('nombre')}» de familia.json no tiene kot.json en {carpeta_k}: no aparece en familia.html")
            continue
        try:
            with open(ruta_json, encoding="utf-8-sig") as fh:
                d = json.load(fh)
            atributo_kot(d)
        except (OSError, ValueError, KeyError, TypeError):
            aviso(f"el kot.json de «{k['nombre']}» está dañado: no aparece en familia.html")
            continue
        archivo = "kot-512.png" if os.path.exists(os.path.join(os.path.dirname(ruta_json), "kot-512.png")) else "kot.png"
        if absoluta:
            img = html.escape(pathlib.Path(base, archivo).as_uri(), quote=True)
        else:
            img = html.escape(urllib.parse.quote(carpeta_k + "/" + archivo), quote=True)
        fondo_k = html.escape(str(k.get("fondo") or d.get("fondo") or "#F4F6F9"), quote=True)
        tarjetas += (f'<figure style="background:{fondo_k}"><kot-avatar src="{img}" kot="{atributo_kot(d)}" '
                     f'alt="{html.escape(k["nombre"], quote=True)}" sombra '
                     f'style="width:200px"></kot-avatar><figcaption>{html.escape(k["nombre"])}</figcaption></figure>')
    doc = f"""<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Familia de Kots</title><style>body{{margin:0;font:15px system-ui,-apple-system,"Segoe UI",sans-serif;color:#1d2027}}
main{{max-width:1100px;margin:0 auto;padding:28px 20px}}h1{{font-size:26px;margin:0 0 18px}}
.g{{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:18px}}
figure{{margin:0;border-radius:20px;padding:18px;display:grid;justify-items:center;gap:8px}}figcaption{{font-weight:600}}</style></head>
<body><main><h1>Familia de Kots</h1><div class="g">{tarjetas}</div></main><script src="kot-avatar.js"></script></body></html>"""
    with open(os.path.join(dir_familia, "familia.html"), "w", encoding="utf-8") as fh:
        fh.write(doc)
    return len(reg)


def main():
    ap = argparse.ArgumentParser(description="Arma el kit de un Kot (mascota de peluche animada) a partir de su personaje 3D.")
    ap.add_argument("--nombre", required=True, help="nombre del agente, p. ej. Hilo")
    ap.add_argument("--personaje", required=True, help="PNG transparente del personaje (RGBA de 8 bits)")
    ap.add_argument("--color", required=True, help="color principal de la marca en HEX")
    ap.add_argument("--fondo", required=True, help="color suave de la paleta para fondos (foto de Telegram, demo)")
    ap.add_argument("--salida", required=True, help="carpeta del kit, p. ej. <marca>/kot")
    ap.add_argument("--familia", help="carpeta de la familia: agrega el Kot a familia.json y regenera familia.html")
    ap.add_argument("--sin-brillo", action="store_true", help="no agregar el brillo de la familia a los ojos")
    ap.add_argument("--sin-animacion", action="store_true", help="no generar kot-animado.webp ni kot-sticker.webm")
    ap.add_argument("--sombra", action="store_true", help="incluir la sombra suave en la animación grabada")
    ap.add_argument("--tamano", type=int, default=512, help="lado de los cuadros de la animación y del sticker (por defecto 512)")
    ap.add_argument("--lado-webp", type=int, default=320, help="lado del WebP animado para web (por defecto 320)")
    a = ap.parse_args()
    # Un SIGTERM (p. ej. un límite de tiempo externo) sale por SystemExit para que se borren los temporales
    signal.signal(signal.SIGTERM, lambda *_: sys.exit(143))
    a.color = normalizar_color(a.color, "color")
    a.fondo = normalizar_color(a.fondo, "fondo")
    if not os.path.isfile(a.personaje):
        raise SystemExit(f"no existe el archivo del personaje: {a.personaje}")
    try:
        revision = ca.revisar(a.personaje)
        if not revision.get("aprobado"):
            raise SystemExit("el personaje no pasa check_alpha.py (fondo no transparente o sin canal alfa): corrígelo primero")
        ancho, alto, datos, ojos_json, caja = preparar_png(a.personaje, a.sin_brillo)
    except (OSError, ValueError, zlib.error, struct.error, IndexError) as e:
        raise SystemExit(f"no pude leer el personaje como PNG (¿archivo dañado?): {e}")
    os.makedirs(a.salida, exist_ok=True)
    limpiar_generados(a.salida)
    kot_png = os.path.join(a.salida, "kot.png")
    eh.guardar(kot_png, ancho, alto, datos)
    datos_kot = {"nombre": a.nombre, "version": 1, "color": a.color, "fondo": a.fondo,
                 "imagen": "kot.png", "ancho": ancho, "alto": alto, "caja": caja, "ojos": ojos_json,
                 "ciclo_ms": CICLO_MS, "fps": FPS, "creado": datetime.date.today().isoformat()}
    with open(os.path.join(a.salida, "kot.json"), "w", encoding="utf-8") as fh:
        json.dump(datos_kot, fh, ensure_ascii=False, indent=2)
    print(f"se generó {kot_png} y kot.json ({len(ojos_json)} ojos)")
    shutil.copy(COMPONENTE, os.path.join(a.salida, "kot-avatar.js"))

    tamanos = telegram = False
    if ffmpeg():
        tamanos = all(redimensionar(kot_png, os.path.join(a.salida, f"kot-{lado}.png"), lado) for lado in (1024, 512, 256))
        telegram = foto_telegram(kot_png, os.path.join(a.salida, "kot-telegram-1024.png"), a.fondo)
        if tamanos and telegram:
            print("se generaron los tamaños y la foto para Telegram")
        else:
            aviso("ffmpeg no pudo generar " + ("los tamaños" if not tamanos else "la foto para Telegram"))
    else:
        aviso("sin ffmpeg: no se generaron kot-1024/512/256.png ni la foto de Telegram")

    animado = {} if a.sin_animacion else animar(a.salida, datos_kot, a.tamano, a.sombra, a.lado_webp)
    if animado.get("webp"):
        print(f"se generó kot-animado.webp ({os.path.getsize(animado['webp']) // 1024} KB)")
    if animado.get("sticker"):
        print(f"se generó kot-sticker.webm ({os.path.getsize(animado['sticker']) // 1024} KB, crf {animado['sticker_crf']})")
    animado["cuadros"] = os.path.exists(os.path.join(a.salida, "kot-cuadros.png"))
    demo_html(a.salida, datos_kot, animado, tamanos)
    leeme(a.salida, datos_kot, animado, tamanos, telegram)
    print("se generaron kot.html, kot-avatar.js y LEEME.md")
    if a.familia:
        n = familia(a.familia, a.salida, datos_kot)
        print(f"familia actualizada: {n} Kots en {os.path.join(a.familia, 'familia.html')}")


if __name__ == "__main__":
    main()
