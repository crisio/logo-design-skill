# Kots: las mascotas de peluche animadas de los agentes

Un **Kot** es la mascota de peluche de un agente: su personaje 3D (ver `personaje-3d.md`) convertido en un kit vivo
para web, Telegram y presentaciones. Los Kots de una empresa forman una **familia**: el mismo fieltro, la misma luz,
los mismos ojos con el mismo brillo y la misma forma de moverse; cambian la forma y el color de cada agente.

## Contenido
1. Qué incluye un Kot
2. Cómo crear un Kot nuevo
3. Cómo se mueve un Kot
4. Cómo usarlo
5. Revisión antes de entregar
6. Límites y honestidad

---

## 1. Qué incluye un Kot

`scripts/kot_build.py` arma esta carpeta (normalmente `<carpeta-de-la-marca>/kot/`):

| Archivo | Para qué |
|---|---|
| `kot.png` | Original, 2048 px, fondo transparente, cuerpo 100 % opaco y el brillo de la familia en los ojos |
| `kot-1024.png` · `kot-512.png` · `kot-256.png` | Tamaños con fondo transparente |
| `kot-telegram-1024.png` | Foto de perfil del bot, sobre el fondo suave de la paleta (Telegram no respeta la transparencia) |
| `kot.json` | Datos: ojos (posición, tamaño, color del párpado y parche de fieltro para parpadear), caja del personaje, colores |
| `kot-avatar.js` | Componente web `<kot-avatar>`, sin dependencias y sin internet |
| `kot.html` | Demo en vivo del Kot, como avatar en fondo claro y oscuro, y la animación grabada |
| `kot-animado.webp` | Animación de 3 s en loop con transparencia, 320 px, para web |
| `kot-sticker.webm` | Sticker animado de Telegram: VP9 con transparencia, 512 px, 3 s, ≤ 256 KB |
| `kot-cuadros.png` | Hoja con 36 cuadros de la animación (incluye el parpadeo), para revisarla |
| `LEEME.md` | Cómo usar cada archivo |

Con `--familia <carpeta>` también actualiza `familia.json` y `familia.html`, que muestra a todos los Kots en vivo.

## 2. Cómo crear un Kot nuevo

1. **Logo aprobado.** El Kot nace del logo del agente: su silueta, letra o símbolo.
2. **Personaje 3D** con `personaje-3d.md`. Usa el prompt de la familia y genera los **ojos lisos**: dos ojos pequeños,
   ovalados y verticales, color tinta oscuro, sin boca. Usa fieltro, sin sombra proyectada y con fondo transparente.
   Genera 2–4 variantes y elige la mejor con la revisión de esa guía.
3. **Revisa** el PNG elegido con `check_alpha.py`. Tiene que decir **APROBADO**.
4. **Arma el Kot:**
   ```bash
   python3 scripts/kot_build.py --nombre <Nombre> --personaje <personaje.png> \
       --color "#HEX-de-la-marca" --fondo "#HEX-suave-de-la-paleta" \
       --salida <carpeta-de-la-marca>/kot --familia <carpeta-de-los-kots>
   ```
   Los colores van en HEX (`#1B9E73` o `#EEE`). Si el personaje no es cuadrado, lo centra en un cuadrado transparente.
   El script corrige el alfa del cuerpo y agrega el brillo de los ojos, salvo que ya lo tenga (lo detecta ojo por ojo).
   Si lo que detecta como ojos no parece ojos (pasa con fieltros muy oscuros), se detiene y lo dice. Busca
   el fieltro para el parpadeo, genera los tamaños, la foto de Telegram, la animación y el sticker, y actualiza la
   familia. Tarda unos 30 segundos.
5. **Mira** `kot-cuadros.png` y abre `kot.html` en el navegador: revisa sobre todo el parpadeo (§5).
6. **Entrega** el kit con su `LEEME.md` y la ruta. Si es parte de una familia, comparte también `familia.html`.

Para tamaños y animaciones el script usa **ffmpeg**, **img2webp** (libwebp) y **Chrome**, si están instalados. Si falta
alguno, lo dice y arma el resto. Con `--sin-animacion` solo genera los datos, los tamaños y la web.

## 3. Cómo se mueve un Kot

El mismo movimiento sirve en vivo (`kot-avatar.js`) y en la animación grabada. Los cuadros de la animación se
capturan del propio componente, así que todo coincide.

- **Ciclo de 3 s en loop perfecto:** flota (sube y baja un 2 %), respira (se estira y se ensancha muy poco) y se mece
  (±1°). Todo pivota desde la base del personaje.
- **Parpadeo:** el ojo se aplasta hasta quedar como una línea y vuelve (170 ms). Mientras parpadea, un parche de
  **fieltro real** tomado junto al ojo, a la misma altura para que la luz coincida, tapa el ojo original. En vivo
  parpadea cada 2.5–6 s, a veces dos veces seguidas. En la animación grabada, una vez por ciclo: empieza a los 2.0 s y
  el cierre total cae justo en un cuadro (el 50, a 2.08 s), así que la animación sí muestra el ojo como línea.
- **En vivo, además:** voltea un poco hacia el cursor, se aplasta al pasar el mouse y da un saltito al tocarlo.
- **Respeta «reducir movimiento»:** se queda quieto. También se pausa cuando no está en pantalla.

## 4. Cómo usarlo

**En una página web** (los portales internos funcionan sin internet):
```html
<script src="kot-avatar.js" defer></script>
<kot-avatar src="kot-512.png" kot='<ojos y caja de kot.json>' style="width:160px"></kot-avatar>
```
Atributos: `alt` (nombre para lectores de pantalla; sin `alt` el Kot es decorativo), `sombra` (sombra suave bajo el Kot), `circulo` (recorte circular con fondo en `--kot-fondo`), `quieto`
(sin animación), `tiempo` y `parpadeo` (pose fija, para capturas). El `LEEME.md` de cada Kot trae el fragmento ya
llenado. El Kot siempre se dibuja en un cuadrado centrado, aunque la caja del elemento no sea cuadrada. En una fila flex
de chat con texto largo, ponle `flex:none` para que no se encoja.

**Sin JavaScript** (correos, presentaciones, documentos): `kot-animado.webp` o `kot-512.png`.

**En Telegram:**
- Foto del bot: @BotFather → `/mybots` → el bot → Edit Bot → Edit Botpic → `kot-telegram-1024.png`.
- Sticker animado: @Stickers → `/newvideo` → sube `kot-sticker.webm` y elige un emoji. Así el agente puede mandar
  su sticker en el grupo.

## 5. Revisión antes de entregar

- [ ] `check_alpha.py` APROBADO para el personaje.
- [ ] El script encontró fieltro para **los dos ojos**. Si avisa que un ojo parpadea con «párpado de color plano», mira
      ese parpadeo: si se nota el parche, genera otra variante del personaje con más fieltro alrededor de los ojos.
- [ ] En `kot-cuadros.png`, los cuadros del parpadeo (2.0–2.2 s): el ojo se vuelve una línea, sin parches visibles.
- [ ] La animación no corta el personaje: flota dentro del cuadro y cabe en el círculo del avatar.
- [ ] El sticker pesa ≤ 256 KB, dura 3 s y mide 512 px.
- [ ] `kot.html` se ve bien en fondo claro y oscuro, y como avatar de 40 px.
- [ ] En una familia, el Kot nuevo comparte fieltro, luz, ojos y brillo con los demás, y su color no repite el de otro.

## 6. Límites y honestidad

- El Kot se anima en 2D a partir del render: no gira en 3D ni mueve los ojos hacia el cursor. Un Kot 3D en tiempo
  real necesita un modelo 3D con los ojos separados del cuerpo (como los de los «dots» de OpenAI) y es otro proyecto.
- El parpadeo depende de encontrar fieltro limpio junto a los ojos. Si los ojos tocan el borde del personaje, el
  parche puede notarse: dilo y propone otra variante.
- Si no puedes generar la animación (sin ffmpeg, img2webp o Chrome), dilo y entrega el resto del kit. No digas que
  existe una animación que no generaste.
