#!/usr/bin/env python3
"""Agrega un brillo a los ojos de un personaje 3D (PNG RGBA) sin tocar nada más de la imagen.

Detecta los ojos (las dos manchas más oscuras y neutras del personaje), pinta dentro de cada uno un reflejo blanco
suave arriba a la izquierda y un puntito más chico abajo a la derecha, y guarda un PNG nuevo. El original no se
modifica. Los reflejos se recortan a la forma del ojo, así que nunca se salen al fieltro.

Uso:
  python3 scripts/eye_highlight.py personaje.png personaje-brillo.png
  python3 scripts/eye_highlight.py personaje.png personaje-brillo.png --recortes ojos.png   # además, un acercamiento antes/después
"""
import argparse
import math
import os
import struct
import sys
import zlib
from collections import deque

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check_alpha as ca  # noqa: E402  (lector de PNG sin dependencias)


def ojos(ancho, alto, px):
    """Devuelve las cajas (x0, y0, x1, y1) y los píxeles de los dos ojos."""
    marca = bytearray(ancho * alto)
    for i in range(ancho * alto):
        r, g, b, a = px[4 * i:4 * i + 4]
        if a >= 200 and max(r, g, b) <= 75 and max(r, g, b) - min(r, g, b) <= 45:
            marca[i] = 1
    visto = bytearray(ancho * alto)
    grupos = []
    for i in range(ancho * alto):
        if marca[i] and not visto[i]:
            cola, pix = deque([i]), []
            visto[i] = 1
            while cola:
                k = cola.popleft()
                pix.append(k)
                x, y = k % ancho, k // ancho
                for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                    if 0 <= nx < ancho and 0 <= ny < alto:
                        j = ny * ancho + nx
                        if marca[j] and not visto[j]:
                            visto[j] = 1
                            cola.append(j)
            if len(pix) > max(20, int(150 * ancho * alto / 2048 ** 2)):   # mínimo proporcional al tamaño
                xs = [k % ancho for k in pix]
                ys = [k // ancho for k in pix]
                grupos.append({"caja": (min(xs), min(ys), max(xs), max(ys)), "pix": set(pix), "n": len(pix)})
    # Candidatos: manchas más altas que anchas. De ellas se elige el par que de verdad parece un par de ojos
    # (pequeñas, de tamaño parecido, a la misma altura y separadas); así las sombras grandes del cuerpo no ganan.
    grupos = [g for g in grupos if (g["caja"][3] - g["caja"][1]) >= 0.9 * (g["caja"][2] - g["caja"][0])]
    grupos.sort(key=lambda g: g["n"], reverse=True)
    if len(grupos) < 2:
        raise SystemExit("no encontré dos ojos oscuros en la imagen")
    mejor, puntaje = None, -1.0
    cand = grupos[:10]
    for i in range(len(cand)):
        for j in range(i + 1, len(cand)):
            a, b = cand[i], cand[j]
            (ax0, ay0, ax1, ay1), (bx0, by0, bx1, by1) = a["caja"], b["caja"]
            wa, ha, wb, hb = ax1 - ax0 + 1, ay1 - ay0 + 1, bx1 - bx0 + 1, by1 - by0 + 1
            if max(wa, wb) > 0.12 * ancho or max(ha, hb) > 0.2 * alto:
                continue
            if max(wa * ha, wb * hb) > 2.2 * min(wa * ha, wb * hb):
                continue
            cya, cyb = (ay0 + ay1) / 2, (by0 + by1) / 2
            if abs(cya - cyb) > 0.08 * alto:
                continue
            separacion = abs((ax0 + ax1) / 2 - (bx0 + bx1) / 2)
            if separacion < 1.2 * (wa + wb) / 2 or separacion > 0.45 * ancho:
                continue
            p = (a["n"] + b["n"]) * (1 - 0.5 * min(cya, cyb) / alto)   # más grandes y más arriba, mejor
            if p > puntaje:
                mejor, puntaje = (a, b), p
    par = list(mejor) if mejor else grupos[:2]
    return sorted(par, key=lambda g: g["caja"][0])


def pintar(ancho, px, ojo, cx, cy, radio, opacidad):
    datos = px
    borde = max(1.5, radio * 0.45)
    x0, y0 = int(cx - radio - borde), int(cy - radio - borde)
    x1, y1 = int(cx + radio + borde) + 1, int(cy + radio + borde) + 1
    for y in range(y0, y1):
        for x in range(x0, x1):
            k = y * ancho + x
            # Solo dentro del óvalo del ojo (la elipse de su caja, un poco adentro): así no salen puntitos del fieltro
            ex0, ey0, ex1, ey1 = ojo["caja"]
            ecx, ecy = (ex0 + ex1 + 1) / 2, (ey0 + ey1 + 1) / 2
            erx, ery = (ex1 - ex0 + 1) / 2 - 2, (ey1 - ey0 + 1) / 2 - 2
            if ((x + 0.5 - ecx) / erx) ** 2 + ((y + 0.5 - ecy) / ery) ** 2 > 1:
                continue
            d = math.hypot(x + 0.5 - cx, y + 0.5 - cy)
            if d >= radio + borde:
                continue
            t = 1.0 if d <= radio - borde else max(0.0, (radio + borde - d) / (2 * borde))
            t = t * t * (3 - 2 * t) * opacidad
            for c in range(3):
                datos[4 * k + c] = round(datos[4 * k + c] * (1 - t) + 255 * t)


def guardar(ruta, ancho, alto, datos):
    fila = ancho * 4
    crudo = b"".join(b"\x00" + bytes(datos[y * fila:(y + 1) * fila]) for y in range(alto))

    def bloque(tipo, cuerpo):
        return struct.pack(">I", len(cuerpo)) + tipo + cuerpo + struct.pack(">I", zlib.crc32(tipo + cuerpo) & 0xFFFFFFFF)
    with open(ruta, "wb") as fh:
        fh.write(ca.FIRMA_PNG + bloque(b"IHDR", struct.pack(">IIBBBBB", ancho, alto, 8, 6, 0, 0, 0))
                 + bloque(b"IDAT", zlib.compress(crudo, 6)) + bloque(b"IEND", b""))


def main():
    ap = argparse.ArgumentParser(description="Agrega un brillo a los ojos de un personaje 3D (PNG RGBA de 8 bits).")
    ap.add_argument("entrada")
    ap.add_argument("salida")
    ap.add_argument("--recortes", help="guarda un HTML con el acercamiento de los ojos, antes y después")
    a = ap.parse_args()
    ancho, alto, prof, tipo, px, _, _ = ca.leer_png(a.entrada)
    if tipo != 6 or prof != 8:
        raise SystemExit("se necesita un PNG RGBA de 8 bits")
    datos = bytearray(px)
    encontrados = ojos(ancho, alto, datos)
    for ojo in encontrados:
        x0, y0, x1, y1 = ojo["caja"]
        w, h = x1 - x0 + 1, y1 - y0 + 1
        # Reflejo principal arriba a la izquierda y un puntito abajo a la derecha, proporcionales al ojo
        pintar(ancho, datos, ojo, x0 + 0.38 * w, y0 + 0.27 * h, 0.17 * w, 0.88)
        pintar(ancho, datos, ojo, x0 + 0.62 * w, y0 + 0.64 * h, 0.08 * w, 0.5)
        print(f"ojo en ({x0},{y0})–({x1},{y1}), {w}×{h} px: brillo agregado")
    guardar(a.salida, ancho, alto, datos)
    print(f"se generó {a.salida}")
    if a.recortes:
        xs = [c for o in encontrados for c in (o["caja"][0], o["caja"][2])]
        ys = [c for o in encontrados for c in (o["caja"][1], o["caja"][3])]
        m = 60
        vx, vy = min(xs) - m, min(ys) - m
        vw, vh = max(xs) - min(xs) + 2 * m, max(ys) - min(ys) + 2 * m
        escala = 520 / vw
        def recorte(src):
            return (f'<div style="width:520px;height:{vh*escala:.0f}px;overflow:hidden;position:relative;border-radius:12px">'
                    f'<img src="{src}" style="position:absolute;left:{-vx*escala:.1f}px;top:{-vy*escala:.1f}px;'
                    f'width:{ancho*escala:.0f}px;height:{alto*escala:.0f}px"></div>')
        with open(a.recortes, "w", encoding="utf-8") as fh:
            fh.write('<!doctype html><meta charset="utf-8"><body style="margin:0;padding:16px;background:#fff;'
                     'font:14px system-ui;display:flex;gap:16px">'
                     f'<div>Antes{recorte(os.path.relpath(a.entrada, os.path.dirname(os.path.abspath(a.recortes))))}</div>'
                     f'<div>Después{recorte(os.path.relpath(a.salida, os.path.dirname(os.path.abspath(a.recortes))))}</div></body>')


if __name__ == "__main__":
    main()
