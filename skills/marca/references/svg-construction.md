# Construir logos en SVG

Cómo convertir un concepto en código SVG limpio y listo para producción, escrito a mano (como una IA que escribe
marcado): geométrico, minimalista y fácil de usar para imprentas, desarrolladores y editores vectoriales.

## Contenido
1. Convenciones de archivo
2. Estrategia de construcción: piensa en primitivas
3. Trazados: escribir geometría limpia
4. Espacio negativo y formas compuestas
5. Trazos vs. rellenos
6. Tipografía en SVG
7. Color, degradados, variantes
8. Recetas de construcción comunes
9. Qué evitar en un archivo maestro
10. Contornos y uniones booleanas
11. Validación

---

## 1. Convenciones de archivo

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256"
     role="img" aria-labelledby="title">
  <title id="title">Logo de Puerto</title>
  <path fill="#0F7C80" d="…"/>
</svg>
```
- **Primero el viewBox**: trabaja en un lienzo limpio de números enteros. 256 × 256 (o 512 × 512) para símbolos;
  para composiciones (lockups), mantén la altura en 256 y deja que el ancho se ajuste (p. ej., `0 0 960 256`). La
  biblioteca incluida usa la misma convención (ancho de 256 o 512 en ~99 % de los archivos).
- **Margen interno**: deja un margen constante dentro del viewBox (≈ 4–8 % del tamaño en los símbolos) o recorta al
  ras y deja que la regla del área de protección se encargue del espaciado; sé consistente en todo el conjunto.
- **Coordenadas enteras o con 1–2 decimales**. El exceso de precisión (`127.99999`) infla los archivos y oculta
  desalineaciones.
- **Incluye `<title>`** por accesibilidad; usa IDs con significado (`symbol`, `wordmark`).
- **Agrupa con lógica**: `<g id="symbol">`, `<g id="wordmark">`, para poder recomponer las composiciones.
- Un archivo por variante (ver §7), con nombres predecibles: `brand-logo-horizontal-color.svg`,
  `brand-symbol-black.svg`.

## 2. Estrategia de construcción: piensa en primitivas

Antes de escribir los datos del trazado, describe la construcción con palabras:
- *"Círculo r=96 centrado en (128,128); quita una cuña de 45° en la parte superior derecha; un círculo más pequeño
  r=28 se ubica en el hueco como 'punto'."*
- *"Letra M hecha con tres barras de 40 unidades de ancho en una retícula de 256; el vértice central sube hasta
  y=96; las astas exteriores se extienden 4 unidades por debajo de la línea base como compensación óptica
  (overshoot) del vértice en punta."*

Luego elige el elemento más simple que exprese cada parte:
- `<circle>`, `<ellipse>`, `<rect rx>` para primitivas (fáciles de leer y de ajustar).
- `<path>` para todo lo demás, y para la silueta final fusionada.
- `<polygon>` para formas de bordes rectos.

Elige una **unidad** (p. ej., 8 o 16 en un lienzo de 256) y ajusta las medidas clave a múltiplos de ella; el logo se
sentirá sistemático y reticularlo después será trivial. Lleva una lista de los radios y ángulos que usas, y
reutilízalos.

## 3. Trazados: escribir geometría limpia

- **Comandos**: `M` mover, `L`/`H`/`V` líneas, `A` arco elíptico (perfecto para segmentos de círculo), `C` Bézier
  cúbica, `Q` cuadrática, `Z` cerrar. Mayúscula = absoluto (prefiérelo mientras diseñas), minúscula = relativo.
- **Arcos para geometría circular**: `A r r 0 largeArc sweep x y`. Las curvas basadas en círculos mantienen los
  radios consistentes y son fáciles de verificar. Ejemplo, un remate semicircular: `M 64 128 A 64 64 0 0 1 192 128`.
- **Béziers para curvas orgánicas**: coloca los puntos de anclaje en los extremos de la curva (arriba, abajo,
  izquierda, derecha), con los manejadores horizontales o verticales en esos puntos; así obtienes curvas suaves y
  predecibles con pocos puntos. Un cuarto de círculo como cúbica usa manejadores de longitud ≈ 0.5523 × radio.
- **Pocos puntos de anclaje**. Cada punto extra es una oportunidad para una ondulación. Si una curva necesita muchos
  puntos, divídela en arcos.
- **Ángulos**: calcula los extremos de las diagonales a partir de ángulos exactos. Para 30°/60°, los desplazamientos
  usan sen/cos (0.5, 0.866); para 45°, desplazamientos iguales en x e y. Evita ángulos casi exactos como 44° o 2°
  fuera de la vertical (el script de auditoría los marca).
- **Esquinas suaves (contra el efecto hueso)**: en lugar de un simple arco unido a un lado recto, extiende los
  manejadores de la curva para que la curvatura aumente de forma gradual. Una buena esquina squircle de tamaño `s`
  empieza ~1.3 × s antes de la esquina, con manejadores de ~0.6 × s.
- **Formas cerradas**: termina siempre con `Z` los trazados que llevan relleno.

## 4. Espacio negativo y formas compuestas

- Pon el contorno exterior y los huecos en **un solo trazado** y usa `fill-rule="evenodd"`: los huecos aparecen donde
  los subtrazados se superponen un número impar de veces. O bien dibuja los huecos en sentido contrario y usa la regla
  predeterminada `nonzero`.
  ```svg
  <path fill-rule="evenodd" d="M128 16 A112 112 0 1 1 127.9 16 Z  M128 80 A48 48 0 1 0 128.1 80 Z"/>
  ```
- Para una figura oculta entre dos formas, diseña **primero la forma negativa** (la flecha, la letra) y luego
  construye las formas positivas a su alrededor; así garantizas que la forma negativa quede limpia.
- Evita `<mask>` y `<clipPath>` en el archivo maestro salvo que sean imprescindibles: algunas herramientas y el
  software de bordado o de corte los manejan mal. En los archivos finales, integra la geometría en los trazados. (En
  la exploración, las máscaras están bien para ir rápido.)
- Donde dos formas rellenas del mismo color se tocan, fusiónalas en un solo trazado para que no quede una costura
  finísima al renderizar o cortar.

## 5. Trazos vs. rellenos

- Explora con trazos (`stroke-width`, `stroke-linecap="round"`, `stroke-linejoin="round"`): son rápidos.
- En el archivo maestro, **convierte los trazos en contornos rellenos** para que el logo escale de forma proporcional
  en todas partes y sobreviva a las herramientas que ignoran la configuración de trazo. Como IA sin herramienta de
  contornos, puedes construir directamente la geometría contorneada (desplazando las curvas la mitad del grosor del
  trazo), o bien conservar los trazos sin usar `vector-effect` en ningún lado y verificar que, al escalar todo el
  SVG, el grosor del trazo escale en proporción (lo hace cuando el trazo está dentro del viewBox escalado). Señala en
  las notas de entrega los trazos que queden, para que alguien los expanda en un editor vectorial.
- Logos monolínea: elige el grosor del trazo en relación con el tamaño (≥ 8 % del ancho del logo si debe leerse a
  24 px).

## 6. Tipografía en SVG

- Los logos finales no deben depender de fuentes instaladas: `<text>` se ve distinto (o no se ve) en otros equipos.
- Opciones, en orden de preferencia:
  1. **Construye las letras geométricamente** como trazados (ideal para logotipos cortos, monogramas y
     letras-símbolo; además, te obliga a crear letras propias y a la medida).
  2. Si el usuario tiene un archivo de fuente y una herramienta vectorial, compón la palabra, personalízala y
     **conviértela a contornos**; luego pega los datos del trazado.
  3. Solo para exploración o presentación, usa `<text>` con una pila de fuentes claramente nombrada y una nota de que
     el logotipo debe convertirse a contornos antes de la entrega. Nunca entregues `<text>` como archivo maestro
     final.
- Al dibujar letras: grosor de asta constante, compensación óptica en las letras redondas, horizontales más delgadas,
  espaciado óptico (consulta `typography.md`).

## 7. Color, degradados, variantes

- Usa los valores HEX exactos de la paleta; limítate a los colores aprobados.
- Pon los colores directamente en los elementos (`fill="#…"`) en lugar de usar bloques `<style>`, para lograr la
  máxima compatibilidad; si quieres, usa `currentColor` para una variante a una tinta pensada para interfaces.
- Degradados: defínelos en `<defs>` con `gradientUnits="userSpaceOnUse"` y coordenadas explícitas para que se vean
  idénticos en todas partes; conserva siempre, junto a ellos, un archivo maestro en color plano.
- **Conjunto de variantes** que se generan a partir del archivo maestro (`scripts/export_variants.py` automatiza los
  cambios de color):
  - `*-color.svg` (a todo color), `*-black.svg`, `*-white.svg` (versión invertida; considera una geometría un poco
    más delgada), `*-mono-<hex>.svg` (un solo color de la marca).
  - Composiciones (lockups): `horizontal` (versión horizontal), `stacked` (versión apilada), `symbol` (solo el
    símbolo), `wordmark` (solo el logotipo).
  - App/favicon: el símbolo sobre un contenedor sólido de cuadrado redondeado o círculo, con el símbolo dimensionado
    ópticamente (normalmente 60–70 % del contenedor).

## 8. Recetas de construcción comunes

**Círculo perfecto con muesca (anillo abierto)**
```svg
<path fill="none" stroke="#111" stroke-width="32" stroke-linecap="round"
      d="M 201.5 54.5 A 104 104 0 1 0 232 128"/>   <!-- exploración; expándelo para el archivo maestro -->
```

**Contenedor de cuadrado redondeado (ícono de app), radio del 22 %**
```svg
<rect x="0" y="0" width="256" height="256" rx="56" fill="#0F7C80"/>
```

**Triángulo equilátero (lado 203.2, altura 176), centrado en su caja delimitadora**: su masa visual (el centroide)
queda baja, así que súbelo unas cuantas unidades si dentro de un contenedor se ve cargado hacia abajo.
```svg
<polygon points="128,40 229.6,216 26.4,216" fill="#111"/>
```

**Letra "A" como letra-símbolo**: vértice plano, todos los bordes con la misma pendiente de 1 : 2 y un trazo
constante de 48 unidades (las astas, la barra transversal y el vértice miden 48)
```svg
<path fill="#111" fill-rule="evenodd"
      d="M104 32 H152 L248 224 H200 L184 192 H72 L56 224 H8 Z  M96 144 H160 L128 80 Z"/>
```

**Globo de diálogo a partir de un círculo + cola (fusionados)**
```svg
<path fill="#111" d="M128 24 A104 104 0 1 1 61.6 208 L28 236 L37.9 180 A104 104 0 0 1 128 24 Z"/>
```

Estos son puntos de partida; refina las proporciones y agrega el giro propio del concepto.

## 9. Qué evitar en un archivo maestro

| Evita | Por qué | En su lugar |
|---|---|---|
| `<text>` | depende de las fuentes instaladas | trazados convertidos a contornos |
| `<image>` / PNG incrustado | no es vectorial, se ve borroso | trazados vectoriales |
| `filter` (desenfoque, sombra, resplandor) | se renderiza de forma inconsistente, no se puede imprimir | formas planas; simula la sombra con una forma más oscura |
| muchos `<mask>`/`clipPath` | compatibilidad con las herramientas | intégralos en los trazados |
| transformaciones muy anidadas | difíciles de editar, errores de redondeo | aplica las transformaciones a las coordenadas (un solo `translate/scale` envolvente, como el que escribe `export_variants.py`, está bien) |
| 20 colores o más / muchos degradados | mala reproducción, baja recordación | ≤ 3 colores planos; degradados escalonados |
| microdetalles < 1/64 del tamaño | desaparecen en tamaños pequeños | fusiónalos o elimínalos |
| ángulos desviados por un grado | parecen accidentales | ángulos exactos |
| metadatos del editor, precisión enorme | archivos inflados | marcado limpio |

## 10. Contornos y uniones booleanas (producción)

Sin un editor vectorial no puedes unir formas con operaciones booleanas, pero puedes acercarte bastante:
- Los subtrazados superpuestos dentro de **un solo** `<path>` con la regla predeterminada `nonzero` (todos dibujados
  en el mismo sentido) se ven como una unión sin costuras en pantalla y en impresión; esto es aceptable para web y
  para la mayoría de los archivos maestros de impresión.
- Las máquinas de corte, los plóters de vinilo y el software de bordado prefieren contornos realmente fusionados. Si
  Inkscape está instalado, puede expandir los trazos y unirlo todo desde la línea de comandos:
  ```bash
  inkscape logo.svg --actions="select-all:all;object-stroke-to-path;path-union;export-plain-svg;export-filename:logo-outlined.svg;export-do"
  ```
  Si no, indica en la entrega que alguien de diseño debe aplicar *Contornear trazo* (*Outline Stroke*) + *Unificar*
  (*Unite*) en un editor vectorial.

## 11. Validación

Ejecuta esto después de cada iteración importante:
```bash
python3 scripts/svg_audit.py path/to/logo.svg          # estructura, colores, complejidad, ángulos, revisión de texto/ráster
python3 scripts/preview_sheet.py path/to/logo.svg -o preview.html   # tamaños, fondos, una tinta, desenfoque, espejo, favicon
python3 scripts/render_png.py path/to/logo.svg --size 512 -o look.png # render rápido para verlo
```
Abre la hoja de pruebas en un navegador y obsérvala (si eres un agente, usa la herramienta de navegador o de capturas
de pantalla que tengas disponible). La auditoría compara la complejidad del archivo con la distribución de la
biblioteca de referencia, para que veas si tu diseño es inusualmente complejo para un logo.
