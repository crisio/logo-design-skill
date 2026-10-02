# Presentación, retroalimentación y entrega

Cómo presentar los conceptos para que se juzguen con los criterios correctos, cómo manejar la retroalimentación y los
comités, y qué entregar al final. También cubre la relación de trabajo (honorarios, trabajo especulativo, derechos)
para los usuarios que son diseñadores.

## Contenido
1. Rondas de presentación
2. Estructura de una presentación de conceptos
3. Cómo hablar de los conceptos
4. Retroalimentación, comités y quién decide
5. Entregables finales
6. La relación de trabajo (para usuarios diseñadores)

---

## 1. Rondas de presentación

Un proyecto típico tiene tres presentaciones:
1. **Conceptos (el punto de control)**: tres direcciones distintas con ~80 % de acabado, **en escala de grises**, cada
   una con una idea de una frase y una breve justificación ligada al brief, mostradas en una sola imagen de conjunto, la
   hoja de conceptos (`scripts/concept_sheet.py`). Termina ofreciendo el kit completo y espera. Objetivo: elegir una
   dirección. No se produce nada más antes de esta respuesta.
2. **Refinamiento**: la dirección elegida, ya refinada —correcciones ópticas, tipografía, composiciones (lockups)—,
   con opciones de **color** investigadas frente a las paletas de la competencia y mostradas en contexto con mockups
   en un tablero de presentación (`scripts/presentation_board.py`).
3. **Kit final**: el logo aprobado con su sistema (paleta, tipografía, variantes), las aplicaciones clave, el conjunto
   de archivos y la guía de uso.

En un chat en el que diseña una IA, las rondas 2 y 3 suelen fusionarse. Una vez que el usuario aprueba una dirección y
pide el kit, entrega todo junto: el logo refinado, el color, las composiciones, el tablero, las exportaciones y la guía
de marca. Nunca fusiones la ronda 1 con las demás, salvo que el usuario te haya pedido explícitamente que no te
detengas a consultarle.

¿Por qué tres conceptos? Son suficientes para una elección real y lo bastante pocos para desarrollarlos bien. Tres
conceptos bien desarrollados superan a una docena a medio hacer, y mostrar demasiados transmite falta de convicción.
Haz que los tres sean realmente diferentes (p. ej., un logotipo a medida, una letra-símbolo y un símbolo pictórico o
abstracto) en lugar de tres variaciones de una misma idea.

¿Por qué primero en escala de grises? El color despierta preferencias personales ("odio el verde") que descarrilan la
conversación sobre la idea. La forma tiene que sostenerse por sí sola.

## 2. Estructura de una presentación de conceptos

Para el punto de control, basta con la imagen de conjunto de los conceptos más un mensaje breve en el chat (ver SKILL.md).
Para una presentación más completa al cliente (ronda 2, o cuando el usuario la pida), usa `scripts/presentation_board.py` para generar un tablero de presentación en HTML —define `"industry"` (coffee, food, retail, fashion, software, saas, finance, consumer-app, services, event, education, health) o una lista explícita de `"mockups"` para que cada contexto encaje con el negocio (`--list-mockups` los muestra todos)— o sigue este esquema en el chat o en diapositivas:

1. **Título**: cliente, proyecto, fecha, diseñador(es).
2. **Lo que escuchamos**: el brief en pocas líneas (público, adjetivos, el problema, criterios de éxito). Así todos
   recuerdan los criterios acordados antes de ver cualquier cosa.
3. **Por concepto** (uno a la vez, no todos juntos):
   - Ponle nombre al concepto y da su **idea en una frase**.
   - Muestra el logo en grande, solo, en negro sobre blanco.
   - Explica *cómo responde al brief* (2–4 viñetas). Menciona brevemente las decisiones de oficio (geometría, letras
     dibujadas a medida).
   - Muéstralo en tamaño pequeño (favicon/ícono de app) y en versión invertida.
   - Muestra 5–6 **mockups pertinentes para el negocio**, con un estilo consistente (una marca de café en vasos y en
     la fachada del local; un SaaS en un ícono de app, el encabezado de un sitio web y una credencial de congreso).
4. **Comparación**: los tres lado a lado y al mismo tamaño.
5. **Recomendación**: cuál recomiendas y por qué (el diseñador es el experto; ten un punto de vista).
6. **Próximos pasos**: qué pasa después de elegir y qué retroalimentación necesitas.

Mantén en perspectiva el papel del logo: un logo no puede cargar con historias de marca profundas. El objetivo es
comunicar algo sobre la marca de forma rápida y sencilla; el resto le corresponde al sistema de identidad y a lo que la
marca hace.

## 3. Cómo hablar de los conceptos

- Empieza por la idea y el brief, no por cuánto tiempo tomó ni qué herramienta se usó.
- Vincula cada decisión con los criterios: "Terminales redondeados porque 'cercana' fue el primer adjetivo que nos diste."
- Muestra el potencial del sistema: los patrones, íconos y animaciones que un concepto podría generar. Un logo
  minimalista suele verse demasiado simple por sí solo; mostrado en uso, su simplicidad se vuelve una ventaja que le da
  aire al resto de la identidad.
- Anticipa las objeciones (parecido con X, legibilidad en tamaño pequeño) y respóndelas antes de que surjan.
- Si un cliente pide algo que contradice el brief, vuelve al brief; explica los pros y contras sin condescendencia.

## 4. Retroalimentación, comités y quién decide

- **Identifica a quien decide** e involúcralo directamente en las presentaciones. La retroalimentación que llega a
  través de intermediarios pierde contexto; las decisiones que se toman sin quien decide terminan revirtiéndose.
- **Comités**: muchas voces tienden a ponerse de acuerdo en la opción menos objetable (la más débil), y la gente se
  alinea con la opinión que más se hace oír. Presenta al grupo más pequeño que incluya a quien decide; recoge
  retroalimentación individual y por escrito, basada en los criterios, en lugar de abrir un debate; reserva los grupos
  focales para verificar que se entiende, no para votar por gustos.
- **Valora toda la retroalimentación**: hasta la que irrita contiene información. Los clientes suelen conocer su
  negocio mejor que el diseñador. No te enamores de tu propio trabajo y nunca demonices al cliente.
- **Traduce la retroalimentación en problemas**: "Hazlo más grande" puede significar "le falta presencia"; "No me gusta
  el color" puede significar "se siente frío". Pregunta *por qué* antes de cambiar nada.
- **Promete menos y entrega más**; cumple los plazos: la confiabilidad genera la confianza que abre la puerta a ideas
  más audaces.
- **Sé firme, no terco**: sostén la línea estratégica, cede en los detalles y recuerda que el diseñador es el
  catalizador del cambio; cierta incomodidad es normal. El trabajo es lograr un logo eficaz, no que todos se sientan
  bien.

## 5. Entregables finales

**Arte maestro (vector)**: SVG (web/desarrollo), PDF (impresión) y, si el usuario tiene las herramientas, AI/EPS para
imprentas y agencias. **Mapa de bits (ráster)**: PNG con transparencia (p. ej., 512, 1024 y 2048 px) y JPG sobre
fondo blanco para uso en oficina.

**Variantes** (genéralas con `scripts/export_variants.py`):
- A todo color, a una tinta en negro, a una tinta en blanco (versión invertida) y a una tinta en el color de la marca.
- Composiciones (lockups): versión horizontal, versión apilada, solo el símbolo, solo el logotipo (+ con eslogan, si
  lo hay).
- Favicon (SVG + PNG de 32/48; ICO si se pide), ícono de app (cuadrado de 1024 px, con la placa de cada plataforma),
  avatar para redes sociales (apto para recorte circular).

**Nombres de archivo**: `brand-logo-horizontal-color.svg`, `brand-logo-stacked-white.png`, `brand-symbol-black.svg` …
Organiza las carpetas por uso: `print/`, `digital/`, `social/`, `source/`.

**Guía de marca básica** (de al menos una página; ver `templates/brand-guidelines-template.md`): área de protección,
tamaños mínimos, códigos de color, fondos aprobados, tipografías, ejemplos de usos incorrectos y qué archivo usar en
cada caso (muchos clientes le mandan a su imprenta el archivo digital en RGB; déjalo explícito).

**Notas de entrega**: justificación del diseño (un párrafo por cada decisión clave), resultados de las pruebas,
pendientes (búsqueda de marcas registradas, pruebas de color Pantone, convertir a contornos cualquier texto o trazo
restante) y notas sobre la licencia de las fuentes usadas.

Lista de verificación final antes de enviar: ver `process.md` §7 y `testing-checklist.md`.

## 6. La relación de trabajo (para usuarios diseñadores)

- **Habla de dinero desde el principio**; los honorarios dependen del alcance (número de conceptos, rondas,
  entregables, uso/derechos, plazos, tamaño del cliente). Cobrar por hora les conviene a quienes empiezan; los
  diseñadores con experiencia suelen cobrar por proyecto (resolver rápido es fruto de años de práctica). Sube tus
  tarifas a medida que crecen la demanda y la experiencia.
- **Cobra por adelantado** (p. ej., un anticipo antes de empezar), fija por escrito los límites de revisiones y los
  plazos, y maneja los costos de impresión por separado.
- **Evita el trabajo especulativo** (propuestas gratuitas o concursos abiertos de diseño): devalúa la experiencia y
  se salta el descubrimiento que hace que un logo sea bueno. El trabajo pro bono para causas en las que
  crees es otra cosa; elígelo de forma deliberada.
- **Derechos y propiedad**: aclara cuándo se transfieren los derechos (normalmente al recibir el pago completo) y si el
  diseñador puede mostrar el trabajo en su portafolio. Los conceptos no usados suelen seguir siendo del diseñador.
- **Originalidad**: nunca hagas pasar por original una modificación ligera de un trabajo existente. Si descubres un
  parecido no intencional, sé honesto, corrígelo y, si hace falta, arregla las cosas con el autor original.
- **Mantente involucrado** después del lanzamiento: ofrece auditorías periódicas y dirección de arte; eso protege el
  trabajo y trae clientes recurrentes.
