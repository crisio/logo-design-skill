# Lista de verificación de pruebas

Un logo solo está terminado cuando ha superado estas pruebas. La mayoría se pueden hacer con
`scripts/svg_audit.py` (estructura y geometría) y `scripts/preview_sheet.py` (pruebas visuales); el resto requiere
criterio. Aplícalas a cada concepto antes de presentarlo y otra vez al arte final.

## 1. Escala
- [ ] **Favicon de 16 px**: la idea central sobrevive; nada se vuelve una mancha. Si no, diseña una versión
      simplificada para tamaño pequeño (menos elementos, trazos más gruesos, separaciones más amplias); las marcas
      gráficas detalladas pueden conservar una versión reducida que las acompañe.
- [ ] **24–32 px** (listas de apps, avatares en redes sociales): reconocible de un vistazo.
- [ ] **Muy grande** (valla publicitaria, fachada de edificio): las curvas son suaves, no hay puntos de anclaje que
      generen bultos y el kerning se sostiene; los defectos invisibles en tamaños pequeños se vuelven evidentes.
- [ ] **Tamaño mínimo**: reduce hasta que la marca gráfica pierda sus rasgos identificativos; el tamaño justo por
      encima de ese es el mínimo documentado (en px para pantalla y en mm para impresión).

## 2. Color y valor
- [ ] Funciona **a una tinta en negro** sobre blanco.
- [ ] Funciona **a una tinta en blanco** sobre negro, y no se ve más pesada que la versión en negro (irradiación).
      Si se ve más pesada, entrega un archivo de la versión invertida ligeramente adelgazado.
- [ ] Funciona sobre el **color de marca**, sobre **fotos** y sobre **patrones** (si no, usa un recurso gráfico:
      un contorno o un contenedor).
- [ ] **Escala de grises**: los segmentos de color siguen separándose por valor; nada depende solo del tono.
- [ ] Los colores se reproducen en **CMYK** y, si son intensos, tienen equivalentes en tinta directa/Pantone.

## 3. Forma
- [ ] **Prueba de ojos entrecerrados / desenfoque**: la silueta, por sí sola, es distintiva.
- [ ] **Prueba del espejo**: al voltearlo horizontalmente no aparecen errores de proporción a los que tu ojo ya se
      había acostumbrado.
- [ ] **Rotación / lecturas no deseadas**: míralo girado 90° y 180°, muy pequeño y a distancia; muéstraselo a
      alguien que no haya visto el brief. Busca letras accidentales, partes del cuerpo, lecturas ofensivas o
      sexuales, símbolos políticos o religiosos y parecidos con señales de peligro.
- [ ] **Correcciones ópticas** hechas: compensación óptica (overshoot), efecto hueso, adelgazamiento de los trazos
      horizontales, centro óptico.
- [ ] **Geometría limpia**: sin ángulos casi exactos, primitivas perfectas, radios y grosores de trazo coherentes
      (`svg_audit.py` señala los ángulos casi exactos y los detalles diminutos).
- [ ] **Equilibrio**: no está inclinado por accidente; el peso está bien distribuido; en los símbolos, proporciones
      cercanas al cuadrado.

- [ ] **Prueba de letras**: cada letra personalizada se sigue leyendo a primera vista como la letra que debe ser
      (pregunta: "¿qué letra es esta?"). Una K que se lee como h, o una N que se lee como un rayo, necesita
      revisión.
- [ ] **Revisión de uniones**: haz zoom en cada lugar donde los trazos se unen o se superponen; no debe haber
      muescas, astillas, bultos, separaciones finísimas ni trampas de tinta accidentales.
- [ ] **Prueba entre pares**: junto a 3–4 marcas ejemplares de la biblioteca, al mismo tamaño, la tuya se ve igual
      de resuelta.

## 4. Distinción y originalidad
- [ ] **Prueba de estantería**: colocado entre la competencia (`preview_sheet.py --refs-industry <industry>`),
      destaca en lugar de confundirse con el resto.
- [ ] **Prueba de familiaridad**: no te recuerda (ni a nadie a quien le preguntes) a una marca existente. Si te
      resulta familiar y no es tuyo, es de alguien más.
- [ ] **Revisión en la biblioteca**: busca en la biblioteca incluida el mismo tema o técnica
      (`search_library.py --subject <thing>`); asegúrate de que el tuyo sea claramente distinto.
- [ ] **Búsqueda de marcas registradas** (recomiéndasela al usuario): consulta las bases de datos de marcas
      registradas que correspondan y haz una búsqueda inversa de imágenes antes del lanzamiento. Tú no puedes dar
      una autorización legal: dilo claramente.

## 5. Significado y adecuación
- [ ] La idea se puede explicar en **una sola frase**.
- [ ] El tono coincide con los adjetivos de la marca (afilado/redondo, pesado/ligero, cálido/frío, clásico/moderno).
- [ ] Identifica en lugar de explicar; seguirá funcionando si el negocio se expande.
- [ ] El significado cultural de los colores y los símbolos está verificado para las culturas del público.
- [ ] Funciona sin el eslogan y, en el caso de los símbolos, con el tiempo, sin el nombre.

## 6. Medios y producción
- [ ] Impresión a una tinta, bordado (sin trazos finísimos, separaciones ≥ ~1 mm al tamaño de un logo en el pecho
      de una prenda), grabado láser, corte de vinil, señalética, modo oscuro, animación.
- [ ] Ícono de app: con tamaño óptico dentro del mosaico redondeado de la plataforma; sin texto fino.
- [ ] Avatares en redes sociales: sobrevive al recorte circular.
- [ ] Archivo maestro: solo vectores, texto convertido a curvas, trazos expandidos, sin filtros ni imágenes
      rasterizadas, `viewBox` limpio (`svg_audit.py` con puntaje ≥ ~90 y sin ningún `FAIL`).

## 7. Contexto
- [ ] Mostrado en 5–6 **mockups realistas y pertinentes para el negocio** (el vaso de una cafetería, no una bolsa
      de gimnasio), con un estilo coherente. Nunca juzgues un logo solo de forma aislada, sobre una mesa de trabajo
      en blanco.
- [ ] Todas las composiciones (versión horizontal, versión apilada, solo símbolo) probadas en sus tamaños de uso
      previstos.

## Registro de resultados
Resume los resultados de las pruebas al presentar: qué se aprobó, qué se ajustó (p. ej., "adelgacé la versión
invertida un 3 %; amplié la abertura de la contraforma de 6 a 10 unidades para que sobreviva a 16 px") y qué le toca
hacer todavía al usuario (búsqueda de marcas registradas, pruebas de color Pantone).
