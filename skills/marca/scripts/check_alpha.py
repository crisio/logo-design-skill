#!/usr/bin/env python3
"""Revisa que un PNG (por ejemplo, el avatar 3D de un personaje) tenga el fondo transparente de verdad.

Los generadores de imágenes a veces entregan un PNG sin canal alfa, con el fondo blanco o con un tablero de ajedrez
pintado que solo *parece* transparente. Este script lee el PNG sin dependencias y revisa:
  · que tenga canal alfa real (o transparencia por paleta);
  · que el borde sea transparente, es decir, que el fondo no esté pintado;
  · que no haya un tablero de ajedrez falso;
  · que sea cuadrado, que el personaje tenga margen, que esté centrado y que quepa en el círculo de un avatar.
Con --preview genera una hoja HTML para mirarlo sobre fondo claro, oscuro, de color y recortado en círculo
(captúrala con render_png.py para verla como imagen).

Uso:
  python3 scripts/check_alpha.py avatar.png
  python3 scripts/check_alpha.py avatar.png --preview avatar-prueba.html --color "#7A3268"
  python3 scripts/check_alpha.py avatar.png --json
  python3 scripts/check_alpha.py avatar.png --opacar avatar-limpio.png   # corrige un cuerpo con alfa 240–254
Sale con código 1 si falla una revisión obligatoria (canal alfa real y borde transparente).
"""
import argparse
import base64
import html
import json
import math
import os
import struct
import sys
import zlib

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import svglib  # noqa: E402,F401  (salida UTF-8 en las consolas de Windows)

FIRMA_PNG = b"\x89PNG\r\n\x1a\n"
CANALES = {0: 1, 2: 3, 3: 1, 4: 2, 6: 4}
UMBRAL_OPACO = 24        # alfa mayor que esto cuenta como «hay personaje»
UMBRAL_TRANSPARENTE = 8  # alfa menor o igual que esto cuenta como transparente


def leer_png(ruta):
    """Devuelve (ancho, alto, profundidad, tipo_color, datos_sin_filtro, paleta, trns)."""
    with open(ruta, "rb") as fh:
        datos = fh.read()
    if datos[:8] != FIRMA_PNG:
        raise ValueError("no es un archivo PNG")
    pos, idat, ihdr, plte, trns = 8, [], None, None, None
    while pos + 8 <= len(datos):
        (largo,) = struct.unpack(">I", datos[pos:pos + 4])
        tipo = datos[pos + 4:pos + 8]
        cuerpo = datos[pos + 8:pos + 8 + largo]
        pos += 12 + largo
        if tipo == b"IHDR":
            ihdr = struct.unpack(">IIBBBBB", cuerpo)
        elif tipo == b"PLTE":
            plte = cuerpo
        elif tipo == b"tRNS":
            trns = cuerpo
        elif tipo == b"IDAT":
            idat.append(cuerpo)
        elif tipo == b"IEND":
            break
    if not ihdr:
        raise ValueError("el PNG no tiene encabezado IHDR")
    ancho, alto, prof, tipo_color, _, _, entrelazado = ihdr
    if entrelazado:
        raise ValueError("PNG entrelazado (Adam7): expórtalo sin entrelazado y vuelve a revisarlo")
    if tipo_color not in CANALES:
        raise ValueError(f"tipo de color {tipo_color} no soportado")
    if prof not in (8, 16) or (tipo_color == 3 and prof != 8):
        raise ValueError(f"profundidad de {prof} bits no soportada para este tipo de PNG")
    bpp = CANALES[tipo_color] * prof // 8
    crudo = zlib.decompress(b"".join(idat))
    fila = ancho * bpp
    salida = bytearray(alto * fila)
    previa = bytearray(fila)
    i = 0
    for y in range(alto):
        filtro = crudo[i]
        i += 1
        linea = bytearray(crudo[i:i + fila])
        i += fila
        if filtro == 1:
            for x in range(bpp, fila):
                linea[x] = (linea[x] + linea[x - bpp]) & 255
        elif filtro == 2:
            for x in range(fila):
                linea[x] = (linea[x] + previa[x]) & 255
        elif filtro == 3:
            for x in range(fila):
                izq = linea[x - bpp] if x >= bpp else 0
                linea[x] = (linea[x] + ((izq + previa[x]) >> 1)) & 255
        elif filtro == 4:
            for x in range(fila):
                a = linea[x - bpp] if x >= bpp else 0
                b = previa[x]
                c = previa[x - bpp] if x >= bpp else 0
                p = a + b - c
                pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
                linea[x] = (linea[x] + (a if pa <= pb and pa <= pc else (b if pb <= pc else c))) & 255
        elif filtro != 0:
            raise ValueError(f"filtro de fila desconocido: {filtro}")
        salida[y * fila:(y + 1) * fila] = linea
        previa = linea
    return ancho, alto, prof, tipo_color, bytes(salida), plte, trns


def canal_alfa(ancho, alto, prof, tipo_color, px, trns):
    """Devuelve (tiene_alfa, bytes con un alfa de 0–255 por píxel)."""
    n = ancho * alto
    paso = 2 if prof == 16 else 1
    if tipo_color == 6:
        return True, px[3 * paso::4 * paso]
    if tipo_color == 4:
        return True, px[paso::2 * paso]
    if tipo_color == 3:
        tabla = bytes((trns[i] if trns and i < len(trns) else 255) for i in range(256))
        return bool(trns), px.translate(tabla)
    if trns:  # gris o RGB con un color declarado transparente
        canales = CANALES[tipo_color]
        clave = tuple(struct.unpack(">" + "H" * canales, trns[:2 * canales]))
        alfa = bytearray(n)
        for k in range(n):
            base = k * canales * paso
            valor = tuple(px[base + c * paso] if paso == 1 else (px[base + c * paso] << 8 | px[base + c * paso + 1])
                          for c in range(canales))
            alfa[k] = 0 if valor == clave else 255
        return True, bytes(alfa)
    return False, b"\xff" * n


def color(ancho, prof, tipo_color, px, plte, x, y):
    paso = 2 if prof == 16 else 1
    canales = CANALES[tipo_color]
    base = (y * ancho + x) * canales * paso
    if tipo_color == 3:
        i = px[base] * 3
        return tuple(plte[i:i + 3]) if plte else (0, 0, 0)
    if tipo_color in (0, 4):
        v = px[base]
        return (v, v, v)
    return (px[base], px[base + paso], px[base + 2 * paso])


def revisar(ruta):
    ancho, alto, prof, tipo_color, px, plte, trns = leer_png(ruta)
    tiene_alfa, alfa = canal_alfa(ancho, alto, prof, tipo_color, px, trns)
    lado = min(ancho, alto)
    r = {"archivo": os.path.basename(ruta), "ancho": ancho, "alto": alto, "canal_alfa": tiene_alfa}

    opaco = bytes(1 if v > UMBRAL_OPACO else 0 for v in range(256))
    transp = bytes(1 if v <= UMBRAL_TRANSPARENTE else 0 for v in range(256))

    # Borde: una franja del 2 % alrededor de toda la imagen
    b = max(1, round(lado * 0.02))
    total_borde = trans_borde = 0
    for y in range(alto):
        fila = alfa[y * ancho:(y + 1) * ancho]
        tramo = fila if (y < b or y >= alto - b) else fila[:b] + fila[-b:]
        total_borde += len(tramo)
        trans_borde += tramo.translate(transp).count(1)
    r["borde_transparente"] = round(trans_borde / total_borde, 4) if total_borde else 0

    # Tablero de ajedrez pintado: el borde es opaco y casi todo son dos grises claros que se alternan
    r["tablero_falso"] = False
    if r["borde_transparente"] < 0.5:
        muestras = []
        paso = max(1, lado // 200)
        for x in range(0, ancho, paso):
            for y in (0, b // 2, alto - 1 - b // 2, alto - 1):
                muestras.append(color(ancho, prof, tipo_color, px, plte, x, y))
        neutros = [round(sum(c) / 3 / 8) for c in muestras if max(c) - min(c) < 14 and sum(c) / 3 > 150]
        if len(neutros) > 0.85 * len(muestras):
            frecuencias = sorted((neutros.count(v) for v in set(neutros)), reverse=True)
            if len(frecuencias) >= 2 and frecuencias[1] > 0.2 * len(neutros):
                r["tablero_falso"] = True

    # Caja del personaje, margen y centrado
    x0, y0, x1, y1 = ancho, alto, -1, -1
    for y in range(alto):
        fila = alfa[y * ancho:(y + 1) * ancho].translate(opaco)
        izq = fila.find(1)
        if izq >= 0:
            der = fila.rfind(1)
            x0, x1 = min(x0, izq), max(x1, der)
            y0 = min(y0, y)
            y1 = y
    if x1 < 0:
        r["vacio"] = True
    else:
        r["vacio"] = False
        r["caja"] = [x0, y0, x1, y1]
        r["margen"] = round(min(x0, y0, ancho - 1 - x1, alto - 1 - y1) / lado, 4)
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        r["descentrado"] = round(max(abs(cx - ancho / 2), abs(cy - alto / 2)) / lado, 4)
        # Avatar circular: cuánto del personaje queda fuera del círculo inscrito (radio al 46 % del lado)
        radio = lado * 0.46
        ccx, ccy = ancho / 2, alto / 2
        fuera = total = 0
        for y in range(y0, y1 + 1):
            fila = alfa[y * ancho:(y + 1) * ancho].translate(opaco)
            total += fila.count(1)
            dy = abs(y + 0.5 - ccy)
            if dy >= radio:
                fuera += fila.count(1)
                continue
            dx = math.sqrt(radio * radio - dy * dy)
            a, z = max(0, int(ccx - dx)), min(ancho, int(ccx + dx) + 1)
            fuera += fila[:a].count(1) + fila[z:].count(1)
        r["fuera_del_circulo"] = round(fuera / total, 4) if total else 0
    muestra = alfa[::max(1, len(alfa) // 200000)]
    opacos = sum(1 for v in muestra if v > UMBRAL_OPACO)
    r["casi_opaco"] = round(sum(1 for v in muestra if 240 <= v < 255) / opacos, 4) if opacos else 0
    parcial = sum(1 for v in alfa[::max(1, len(alfa) // 200000)] if 0 < v < 255)
    r["semitransparente"] = round(parcial / len(alfa[::max(1, len(alfa) // 200000)]), 4)

    obligatorio = r["canal_alfa"] and r["borde_transparente"] >= 0.97 and not r["tablero_falso"] and not r["vacio"]
    r["aprobado"] = bool(obligatorio)
    return r


def reporte(r):
    ok, av = "✓", "⚠"
    lineas = [f"=== {r['archivo']}  ({r['ancho']}×{r['alto']})"]
    lineas.append(f"{ok if r['canal_alfa'] else '✗'} canal alfa real" if r["canal_alfa"]
                  else "✗ sin canal alfa: el fondo no puede ser transparente; pide salida con transparencia o quita el fondo")
    pct = round(r["borde_transparente"] * 100)
    if r["tablero_falso"]:
        lineas.append("✗ tablero de ajedrez pintado: el fondo parece transparente pero es parte de la imagen")
    elif r["borde_transparente"] >= 0.97:
        lineas.append(f"{ok} borde transparente ({pct} %)")
    else:
        lineas.append(f"✗ el borde no es transparente ({pct} %): el fondo está pintado")
    if r["vacio"]:
        lineas.append("✗ la imagen está vacía: no hay nada opaco")
    else:
        lineas.append(f"{ok if r['ancho'] == r['alto'] else av} formato "
                      + ("cuadrado" if r["ancho"] == r["alto"] else "no cuadrado: recórtalo a 1:1"))
        m = round(r["margen"] * 100, 1)
        lineas.append(f"{ok if r['margen'] >= 0.06 else av} margen alrededor del personaje: {m} %"
                      + ("" if r["margen"] >= 0.06 else " (deja al menos 6 % para usarlo como avatar)"))
        d = round(r["descentrado"] * 100, 1)
        lineas.append(f"{ok if r['descentrado'] <= 0.05 else av} centrado (desvío {d} %)")
        f = round(r["fuera_del_circulo"] * 100, 1)
        lineas.append(f"{ok if r['fuera_del_circulo'] <= 0.005 else av} cabe en un avatar circular"
                      + ("" if r["fuera_del_circulo"] <= 0.005 else f": {f} % del personaje queda fuera del círculo"))
    if r.get("casi_opaco", 0) > 0.2:
        lineas.append(f"{av} el personaje no es 100 % opaco: {round(r['casi_opaco'] * 100)} % de sus píxeles tiene alfa entre "
                      "240 y 254 (deja pasar un poco el fondo); corrígelo con --opacar salida.png")
    lineas.append(f"· sombras o bordes suaves con transparencia parcial: {round(r['semitransparente'] * 100, 1)} % de la imagen")
    lineas.append("resultado: " + ("APROBADO, el fondo es transparente de verdad" if r["aprobado"]
                                   else "NO APROBADO, corrige lo marcado con ✗"))
    return "\n".join(lineas)


def opacar(ruta, salida, umbral=240):
    """Guarda una copia RGBA de 8 bits con alfa 255 donde el alfa era ≥ umbral (bordes suaves intactos)."""
    ancho, alto, prof, tipo_color, px, _, _ = leer_png(ruta)
    if tipo_color != 6 or prof != 8:
        raise ValueError("--opacar solo acepta PNG RGBA de 8 bits")
    datos = bytearray(px)
    tabla = bytes(255 if v >= umbral else v for v in range(256))
    datos[3::4] = bytes(datos[3::4]).translate(tabla)
    fila = ancho * 4
    crudo = b"".join(b"\x00" + bytes(datos[y * fila:(y + 1) * fila]) for y in range(alto))

    def bloque(tipo, cuerpo):
        return struct.pack(">I", len(cuerpo)) + tipo + cuerpo + struct.pack(">I", zlib.crc32(tipo + cuerpo) & 0xFFFFFFFF)
    with open(salida, "wb") as fh:
        fh.write(FIRMA_PNG + bloque(b"IHDR", struct.pack(">IIBBBBB", ancho, alto, 8, 6, 0, 0, 0))
                 + bloque(b"IDAT", zlib.compress(crudo, 9)) + bloque(b"IEND", b""))


def hoja_prueba(ruta_png, salida, color_marca):
    with open(ruta_png, "rb") as fh:
        uri = "data:image/png;base64," + base64.b64encode(fh.read()).decode("ascii")
    nombre = html.escape(os.path.basename(ruta_png))
    fondos = [("Blanco", "#FFFFFF"), ("Gris claro", "#F4F6F9"), ("Modo oscuro (Telegram)", "#17212B")]
    if color_marca:
        fondos.append(("Color de marca", color_marca))
    tarjetas = "".join(f'<figure style="background:{c}"><img src="{uri}" alt=""><figcaption>{html.escape(n)}</figcaption></figure>'
                       for n, c in fondos)
    circulos = "".join(f'<div class="c" style="background:{c}"><img src="{uri}" style="width:{s}px;height:{s}px"></div>'
                       for c in ("#FFFFFF", "#17212B") for s in (40, 96))
    doc = f"""<!doctype html><html lang="es"><meta charset="utf-8"><title>Prueba de transparencia · {nombre}</title>
<style>body{{margin:0;padding:24px;font:14px system-ui,-apple-system,"Segoe UI",sans-serif;background:#fff;color:#1d2027}}
h1{{font-size:18px;margin:0 0 16px}}.g{{display:grid;grid-template-columns:repeat(4,1fr);gap:16px}}
figure{{margin:0;border-radius:12px;padding:12px;border:1px solid #dfe4ec}}figure img{{width:100%;display:block}}
figcaption{{font-size:12px;opacity:.7;margin-top:6px;color:#888}}
.t{{background-color:#fff;background-image:linear-gradient(45deg,#ccc 25%,transparent 25%),linear-gradient(-45deg,#ccc 25%,transparent 25%),linear-gradient(45deg,transparent 75%,#ccc 75%),linear-gradient(-45deg,transparent 75%,#ccc 75%);background-size:20px 20px;background-position:0 0,0 10px,10px -10px,-10px 0}}
.fila{{display:flex;gap:20px;align-items:center;margin-top:20px}}.c{{padding:14px;border-radius:12px;border:1px solid #dfe4ec}}
.c img{{border-radius:50%;object-fit:cover;display:block}}</style>
<h1>Prueba de transparencia · {nombre}</h1>
<div class="g">{tarjetas}</div>
<div class="fila"><figure class="t" style="width:220px"><img src="{uri}" alt=""><figcaption>Sobre tablero: lo transparente deja ver los cuadros</figcaption></figure>{circulos}</div>
</html>"""
    with open(salida, "w", encoding="utf-8") as fh:
        fh.write(doc)


def main():
    ap = argparse.ArgumentParser(description="Revisa que un PNG tenga el fondo transparente de verdad (avatares y personajes).")
    ap.add_argument("png", nargs="+", help="archivos PNG a revisar")
    ap.add_argument("--json", action="store_true", help="salida en JSON")
    ap.add_argument("--preview", help="genera una hoja HTML de prueba (solo con un archivo)")
    ap.add_argument("--color", help="color de marca en HEX para la hoja de prueba, p. ej. #7A3268")
    ap.add_argument("--opacar", metavar="SALIDA", help="guarda una copia con alfa 255 en los píxeles casi opacos "
                    "(alfa ≥ 240); los bordes suaves no cambian (solo con un archivo)")
    a = ap.parse_args()
    resultados, fallo = [], False
    for ruta in a.png:
        try:
            r = revisar(ruta)
        except (OSError, ValueError, zlib.error) as e:
            r = {"archivo": os.path.basename(ruta), "error": str(e), "aprobado": False}
        resultados.append(r)
        fallo = fallo or not r.get("aprobado")
        if not a.json:
            print(f"=== {r['archivo']}\n✗ no se pudo leer: {r['error']}" if "error" in r else reporte(r))
    if a.json:
        print(json.dumps(resultados, ensure_ascii=False, indent=2))
    if a.opacar:
        opacar(a.png[0], a.opacar)
        if not a.json:
            print(f"se generó {a.opacar} con el personaje 100 % opaco")
    if a.preview:
        hoja_prueba(a.opacar or a.png[0], a.preview, a.color)
        if not a.json:
            print(f"se generó {a.preview}: captúrala con render_png.py para mirarla")
    sys.exit(1 if fallo else 0)


if __name__ == "__main__":
    main()
