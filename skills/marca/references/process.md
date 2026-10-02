# El proceso de diseño en detalle

Las etapas que van del brief al arte final, adaptadas tanto para una IA que diseña trabajando con código SVG como
para un diseñador humano con su cuaderno de bocetos. SKILL.md ofrece la versión corta; lee este documento para conocer
los detalles de cada etapa.

## Contenido
1. Mapa de etapas
2. Conceptualización
3. Moodboards y recopilación de referencias
4. Exploración ("bocetado"): tres etapas
5. Desarrollo en vector
6. Refinamiento y retícula
7. Lista de verificación del arte final
8. Hábitos de trabajo

---

## 1. Mapa de etapas

| Etapa | Resultado | Condición para avanzar |
|---|---|---|
| Colaboración / descubrimiento | Brief, criterios, calendario, quién decide | Brief acordado |
| Conceptualización | Mapa de palabras, 6–10 conceptos de una frase | Los conceptos son distintos y fieles al brief |
| Exploración | Muchas formas preliminares por concepto | 2–4 direcciones que vale la pena desarrollar |
| Desarrollo | Versiones vectoriales limpias en negro de 3 conceptos | Presentables con ~80 % de acabado |
| Presentación 1 (punto de control) | 3 conceptos en escala de grises en una sola imagen de conjunto + ofrecimiento del kit | El usuario elige una dirección y pide el kit |
| Refinamiento | Correcciones ópticas, retícula, color, tipografía, composiciones (lockups) | Logo final aprobado |
| Sistema y aplicaciones | Paleta, tipografías, variantes, patrones, aplicaciones clave | Sistema aprobado |
| Producción | Archivos finales, especificaciones, guía de marca | Entregado; plan de auditoría |

Si es un rediseño, integra durante la exploración el reconocimiento de marca que ya existe (colores, formas, detalles
históricos).

## 2. Conceptualización

- Empieza por el nombre y un brief detallado: desde la gran idea de la marca hasta cómo opera en el día a día.
- Las pistas más útiles son los **adjetivos** que describen la marca; aportan señales visuales abstractas que pueden
  convertirse en símbolos. Explora también: las letras y el significado del nombre, la promesa, el mundo del público,
  el proceso y los materiales del producto, el lugar y el origen.
- Si el nombre contiene algo visual (una letra y un número con formas marcadas, una palabra que es un objeto), el
  concepto puede estar escondido a plena vista.
- Escribe cada concepto en **una sola frase** ("Una 'T' cuyo travesaño es el borde superior de un escudo, para una
  empresa de logística cuya promesa es la protección"). Si no se puede decir en una frase, no se entenderá de un
  vistazo.
- Busca conceptos ingeniosos *y* visualmente agradables: los logos que combinan una idea ingeniosa con un buen
  atractivo visual causan la primera impresión más fuerte.
- Toma en cuenta la demografía y la cultura del público (colorido y redondeado para niños; audaz para ciertos
  públicos; símbolos culturales cuando sean pertinentes), pero la estrategia de marca tiene la última palabra: un
  producto infantil puede tener una identidad adulta.

## 3. Moodboards y recopilación de referencias

- No solo logos: incluye naturaleza, arquitectura, pintura, materiales, tipografía, fotografía y detalles de producto.
- Organiza los moodboards (tableros de inspiración) por dirección —clásica, futurista/de alta tecnología,
  colorida, monocromática— y por tipo de logo (símbolo pictórico, letra-símbolo, monograma), cada uno con imágenes
  pertinentes. Los límites claros facilitan las decisiones.
- Usa la biblioteca para buscar logos de referencia por técnica y tema
  (`scripts/search_library.py --technique negative-space --exemplary`). Las referencias sirven para aprender
  construcción y tono; nunca para calcarlas.
- Los moodboards pueden compartirse con el cliente para alinearse en el estilo, o quedarse en privado; los clientes no
  siempre pueden prever cómo se desarrollará una dirección, así que no dejes que una preferencia de estilo temprana
  fije de antemano el resultado.

## 4. Exploración: tres etapas

Un diseñador humano hace esto con lápiz y papel calco; como IA, haz lo equivalente con descripciones rápidas y
miniaturas SVG preliminares. La lógica es la misma.

### Etapa A — Inicial (cantidad antes que calidad)
- Vuelca ideas sin juzgar la claridad, el espaciado, la forma ni la silueta. Trazos toscos, formas imperfectas,
  curvas descuidadas. La página debería parecer un campo de batalla de ideas a medio formar.
- La cantidad importa porque deja que ocurran accidentes inesperados. Para una IA: enumera 15–30 microvariaciones
  repartidas entre los 6–10 conceptos (distintos tratamientos de letra, encuadres, contenedores, combinaciones de
  espacio negativo, ángulos).
- Las miniaturas SVG preliminares de 64–128 px son ideales: el tamaño pequeño obliga a pensar en la silueta.

### Etapa B — Refinamiento (de ~30 % a ~60 %)
- Elige el concepto más prometedor por intuición; quizá represente apenas un ~30 % del resultado final. La meta es
  llegar al 50–60 %.
- Vuelve a dibujarlo como referencia y luego haz muchas versiones parecidas, cada una probando una mejora nueva: cómo
  interactúan los elementos, un flujo equilibrado, el contorno, la proporción. Compara cada versión con la anterior;
  conserva lo que funciona y elimina lo que no.

### Etapa C — Ajuste fino (limpio y preciso)
- Calca la mejor versión una y otra vez, con pequeñas mejoras, hasta que la forma quede limpia y precisa. Al final
  deberían quedar pocos cambios formales para la etapa vectorial.

Los diseñadores que se detienen en el primer resultado aceptable renuncian a la calidad que podrían alcanzar. Sigue
agregando y quitando.

## 5. Desarrollo en vector

- **Copia y luego cambia.** Antes de cada cambio importante, duplica la versión actual y colócala junto a la anterior.
  Cuando algo salga mal, podrás ver exactamente dónde. (En el trabajo con SVG: guarda `concept-a-v1.svg`, `-v2.svg` …
  y compáralos con `scripts/preview_sheet.py --compare`.)
- **Pocos puntos de anclaje.** Los puntos de anclaje tienen mucho poder; demasiados vuelven las curvas irregulares y
  dentadas. Elimina de vez en cuando los que sobran. Las curvas limpias salen de pocos puntos de anclaje bien ubicados,
  con manejadores alineados a la tangente de la curva (manejadores horizontales o verticales en los puntos extremos).
- **Construye con formas.** Usa círculos, rectángulos y radios consistentes para construir y para revisar curvas y
  esquinas.
- **Primero en negro.** Desarrolla en negro sólido sobre blanco. El color llega después de elegir el concepto.
- Presenta con alrededor de un **80 % de acabado**: lo bastante refinado para juzgar la idea, pero no tan pulido como
  para desperdiciar esfuerzo en una dirección que termine descartándose.

## 6. Refinamiento y retícula

Después de que se aprueba una dirección:
1. **Alineación**: verifica que todas las horizontales y verticales sean exactas (no desviadas 1–2°). Lleva los
   ángulos casi exactos al ángulo estándar más cercano (43° → 45°).
2. **Primitivas**: círculos perfectamente circulares, cuadrados realmente cuadrados, radios consistentes donde
   corresponda.
3. **Consistencia**: grosores de trazo, anchos de separación, radios de esquina, ángulos de los remates.
4. **Correcciones ópticas**: compensación óptica (overshoot), efecto hueso, irradiación (versión invertida),
   adelgazamiento de los trazos horizontales, centro óptico (ver `visual-techniques.md`).
5. **Color**: construye la paleta y pruébala sobre distintos fondos (ver `color.md`).
6. **Tipografía y composiciones (lockups)**: termina el logotipo, el espaciado y todas las composiciones (ver
   `typography.md`).
7. **Pruebas de escala**: ver `testing-checklist.md`.

No fuerces a la retícula las curvas orgánicas que no se descomponen en círculos; déjalas como están.

## 7. Lista de verificación del arte final

- [ ] Sin puntos de anclaje duplicados, sueltos o innecesarios; sin trazados abiertos en formas con relleno.
- [ ] Ángulos precisos, sobre todo en la silueta exterior.
- [ ] Todo el texto convertido a contornos; sin texto editable, sin imágenes rasterizadas, sin filtros ni efectos en
  el archivo maestro.
- [ ] Trazos expandidos a rellenos (salvo en una variante basada en trazos hecha a propósito).
- [ ] Formas unidas o combinadas donde deban ser una sola (sin huecos ni superposiciones finísimas que se vean como
  costuras).
- [ ] Mesa de trabajo/viewBox ajustada al logo con márgenes consistentes; logo centrado ópticamente.
- [ ] Los colores son los valores exactos de la marca; se entregan las versiones a una tinta e invertida.
- [ ] El conjunto de archivos coincide con los entregables acordados (ver `presentation-delivery.md`).
- [ ] Archivos de trabajo archivados; versiones con nombres claros.

## 8. Hábitos de trabajo

- Lleva contigo un cuaderno de bocetos (o un archivo de notas): las ideas llegan en momentos inesperados y se escapan
  rápido. Fotografía formas interesantes, arquitectura y los espacios negativos de la señalética.
- Experimenta fuera del brief: trabaja en el estilo opuesto al tuyo (color si trabajas en blanco y negro, líneas si
  trabajas con formas sólidas, desordenado si trabajas limpio). Los accidentes —un trazo que se desvía, una capa mal
  configurada— pueden ser justo lo que le faltaba a un proyecto.
- Trata los comentarios del cliente como información valiosa, no como un ataque; los clientes suelen conocer su negocio
  mejor que tú. No te enamores de tus creaciones y no demonices a los clientes.
- Deja que tu proceso, y no tu estado de ánimo, lleve el mando: ojos descansados, comparaciones lado a lado y volver
  siempre al brief.
