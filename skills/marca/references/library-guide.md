# La biblioteca de referencia: guía y hallazgos

La skill incluye **más de 1400 logos SVG reales** (≈1200 marcas; 233 marcas traen tanto la composición completa como
un símbolo `-icon` independiente), cada uno clasificado visualmente por tipo de logo, técnica, geometría, tema,
tipografía, tono y sector. Úsala para aprender *cómo* se construyen los logos y para ver qué aspecto tiene ya un
sector.

> **Los logos son marcas registradas de sus respectivos propietarios.** Se incluyen solo como material de estudio.
> Nunca los copies, calques ni modifiques ligeramente para un cliente. Si tu concepto se parece a alguno, cámbialo.

## Contenido
1. Qué incluye y dónde está
2. Cómo aprovecharla bien
3. Hallazgos basados en datos
4. Lecciones seleccionadas por técnica (con archivos de ejemplo)
5. Esquema del catálogo y cómo ampliar la biblioteca

---

## 1. Qué incluye y dónde está

```
assets/library/
  svg/                  más de 1400 archivos de logo (<marca>.svg = logo completo, <marca>-icon.svg = símbolo independiente)
  catalog.json          un registro por archivo: estructura + colores + complejidad + clasificación visual
  classifications.json  las etiquetas visuales (fuente de verdad para mark_type, techniques, subject, …)
  stats.json            distribuciones que usa svg_audit.py (puntos de anclaje, colores, tipos…)
  gallery.html          explorador visual con filtros, pensado para personas; ábrelo localmente en un navegador
```
La colección está muy cargada hacia marcas de tecnología (herramientas para desarrolladores 21 %,
frameworks/bibliotecas 17 %, nube 7 %, bases de datos 6 %, testing/monitoreo 6 %…). Ten presente ese sesgo: sus
convenciones son convenciones *tech*.
Sectores como alimentos y bebidas, moda, hotelería, salud o servicios públicos casi no están representados: para
ellos, usa `--subject`/`--query` para encontrar logos que compartan tema o técnica (tazas, hojas, arcos, la letra K…),
arma la prueba de estantería con archivos elegidos a mano mediante `preview_sheet.py --refs …` y apóyate en lo que tú
sabes de las convenciones del sector.

## 2. Cómo aprovecharla bien

- **Estudia una técnica antes de usarla**: toma 5–8 archivos ejemplares y *lee el SVG* para ver cómo está construida
  la geometría (con qué pocos puntos de anclaje, qué primitivas, cómo se recorta el espacio negativo):
  `python3 scripts/search_library.py --technique negative-space --exemplary --format paths`
- **Mapea las convenciones de un sector** antes de diseñar, y luego decide dónde ajustarte a ellas y dónde apartarte:
  `python3 scripts/search_library.py --industry security-identity --summary`
- **Comprueba que tu idea no esté ya tomada** (los temas del catálogo están en inglés, así que busca en inglés):
  `python3 scripts/search_library.py --subject "rocket"`
- **Haz la prueba de estantería de tu concepto** frente a logos reales:
  `python3 scripts/preview_sheet.py concept.svg --refs-industry developer-tools -o shelf.html`
- **Calibra la complejidad**: `svg_audit.py` compara tu cantidad de puntos de anclaje y de colores con la biblioteca.
- Para inspirarte por sensación: `--mood friendly`, `--mood technical`, `--type-style serif`, `--case lowercase`.

Filtros útiles: `--type`, `--symbol-type`, `--technique`, `--geometry`, `--industry`, `--color`, `--primary-color`,
`--max-colors`, `--aspect`, `--variant icon`, `--type-style`, `--case`, `--mood`, `--subject`, `--query`,
`--exemplary`, `--no-gradient`, `--summary`, `--list-values`.

## 3. Hallazgos basados en datos

Entre paréntesis va el valor del catálogo que usas en los filtros (`--list-values` los muestra todos).

**Tipos de logo (por archivo)** — símbolo abstracto (`abstract`) 23.5 %, imagotipo (`combination`) 20.6 %, símbolo
pictórico (`pictorial`) 20.2 %, letra-símbolo (`letterform`) 15.2 %, logotipo (`wordmark`) 9.9 %, emblema
(`emblem`) 3.8 %, mascota (`mascot`) 3.8 %, sigla (`lettermark`) 3.0 %. (Los archivos de ícono independiente inflan
los tipos de símbolo).
Dentro de los imagotipos, el símbolo es abstracto en 43 %, pictórico en 33 %, letra-símbolo en 17 % y mascota en 5 %.

**Proporciones** — el 55 % de los archivos son casi cuadrados (0.8–1.25 : 1). De las marcas que tienen ambos
archivos, ~9 de cada 10 composiciones son anchas (> 2.5 : 1) y ~3 de cada 4 íconos son casi cuadrados: símbolo +
versión horizontal es la pareja estándar.

**Color** — mediana de 2 colores; ≈ 75 % usa ≤ 3; ≈ 47 % de los íconos independientes son a una tinta. Hay degradados
en ≈ 19 % de los archivos. Matiz dominante: azul ≈ 22 %, rojo ≈ 13 %, monocromo ≈ 13 %, multicolor ≈ 28 %; el
amarillo y el rosa son raros.
→ En tecnología, el azul es camuflaje; los matices cálidos o poco comunes son una forma fácil de diferenciarse.

**Geometría** — el círculo (`circle`) es la base más común (26 %), luego orgánica (`organic`, 14 %), cuadrado
(`square`, 14 %), forma libre (`freeform`, 13 %), triángulo (`triangle`, 8 %), hexágono (`hexagon`, 8 %; 10 % entre
marcas de desarrollo/nube/datos: un cliché del sector) y cuadrado redondeado (`rounded-square`, 7 %).

**Técnicas** — contención (`containment`) 32 %, espacio negativo (`negative-space`) 20 %, monolínea
(`line-monoline`) 17 %, segmentos de color (`color-segments`) 14 %, sombreado dimensional (`dimensional-shading`)
10 %, construcción geométrica (`geometric-construction`) 9 %, repetición modular (`modular-repetition`) 7.5 %,
superposición/transparencia (`overlap-transparency`) 7 %, significado oculto (`hidden-meaning`) 7 %, isométrica
(`isometric-3d`) 6 %, simetría radial (`radial-symmetry`) 6 %, sustitución de letras (`letter-substitution`) 3 %.
→ Encerrar un símbolo en un círculo o un cuadrado es el recurso más común: útil para íconos de app, pero también
genérico. El espacio negativo y el significado oculto aparecen en la mayoría de los logos más sólidos (ejemplares).

**Tipografía (541 archivos con texto)** — sans geométrica (`geometric-sans`) 49 %, a medida/display
(`display-custom`) 19 %, grotesca (`grotesque-sans`) 13 %, humanista (`humanist-sans`) 8 %, caligráfica (`script`)
5 %, serif (`serif`) 3 %, egipcia (`slab`) 1 %, redondeada (`rounded-sans`) 1 %. Caja: minúsculas (`lowercase`)
36 %, mayúsculas (`uppercase`) 32 %, tipo título (`titlecase`) 20 %, mixta (`mixed`) 13 %.
→ La sans geométrica en minúsculas es lo predeterminado en tecnología; un logotipo serif, egipcio, humanista o
realmente a medida destaca.

**Complejidad** — los símbolos cuadrados tienen una mediana de ~53 puntos de anclaje (p75 ≈ 96, p90 ≈ 194). Los
logos ejemplares se concentran en el extremo bajo: los grandes logos se construyen con pocos puntos, colocados a
propósito.

**Etiquetas de tono (`mood`)** más usadas — `technical` (técnico), `friendly` (amigable), `bold` (audaz), `modern`
(moderno), `playful` (lúdico). Lo "amigable" casi siempre lo transmiten la geometría redondeada y las minúsculas; lo
"técnico", la monolínea, las retículas, los corchetes y las formas isométricas.

## 4. Lecciones seleccionadas por técnica (con archivos de ejemplo)

Todos los archivos de abajo están en `assets/library/svg/`. Léelos como SVG para estudiar su construcción.

**Espacio negativo** — la figura y el fondo cargan significado.
- `auth0-icon.svg` estrella tallada en un escudo · `apache-camel.svg` camello recortado de un círculo · `doctrine.svg`
  flecha recortada de una gota · `esdoc.svg` cara de búho hecha por completo con espacio negativo · `houndci.svg`
  perfil de perro en un cuadrado · `npm-icon.svg` letra tallada en un cuadrado sólido · `khan_academy-icon.svg` brote
  que se lee como una persona.

**Significado oculto / doble lectura** — una forma, dos ideas.
- `airbnb.svg` un solo bucle = pin + corazón + A · `amplitude-icon.svg` A = onda de sonido · `astro.svg` A = cohete ·
  `gnome-icon.svg` huella = G · `spidermonkey-icon.svg` mono = S · `kissmetrics.svg` corazón + gráfico de barras ·
  `botanalytics.svg` borde del globo de diálogo = línea de gráfico · `twitch.svg` globo de diálogo con ojos.

**Sustitución de letras y logotipos a medida** — hacer que un nombre sea propio.
- `hubspot.svg` rueda dentada como la "o" · `fastly.svg` cronómetro dentro de una letra · `tor.svg` cebolla como "o" ·
  `sparkpost.svg` llama en lugar de la "O" · `mozilla.svg` sintaxis de URL en el nombre · `100tb.svg` doble cero como
  infinito · `adyen.svg` letras cuadradas totalmente a medida · `nextjs.svg` trazo de la X prolongado · `go.svg`
  cursiva + líneas de velocidad · `stripe.svg` minúsculas a medida con espaciado ajustado.

**Letras-símbolo** — una letra, una idea.
- `kotlin-icon.svg` K a partir de un solo corte triangular · `patreon.svg` P = barra + círculo · `pagekit.svg` P a
  partir de un cuadrado con muesca · `gatsby.svg` G a partir de círculo + diagonal · `pinterest.svg` P como un pin ·
  `zendesk-icon.svg` Z a partir de triángulos y semicírculos · `mesos.svg` M a partir de triángulos · `metabase.svg`
  M a partir de una retícula de puntos · `mobx.svg` `]v[` se lee como M.

**Construcción geométrica** — primitivas, radios coherentes, ángulos limpios.
- `elm.svg` cuadrado de tangram · `framer.svg` cuadrados y triángulos · `google-photos.svg` cuatro semicírculos ·
  `circleci.svg` anillo con muesca · `vercel-icon.svg` un solo triángulo · `twitter.svg` pájaro hecho con arcos de
  círculo · `buck.svg` venado monolínea de geometría estricta · `tsuru.svg` grulla de origami · `figma.svg` círculos
  modulares.

**Repetición modular y simetría radial**
- `slack-icon.svg` módulos rotados que forman un numeral (#) · `dropbox.svg` cinco rombos · `openai-icon.svg` un
  módulo rotado seis veces · `cardano-icon.svg` puntos graduados · `centos-icon.svg` molinete · `ibm.svg` franjas que
  unifican las letras · `tidal-icon.svg` cuatro diamantes · `ubuntu.svg` tres figuras en un anillo.

**Volumen con recursos planos** — profundidad sin realismo.
- `ethereum.svg` octaedro facetado · `sketch.svg` gema facetada · `codesandbox.svg` cubo hecho con cortes · `unity.svg`
  cubo a partir de espacio negativo · `webpack.svg` cubo dentro de un cubo · `tensorflow.svg` una sola forma se lee
  como T y como F · `laravel.svg` L isométrica monolínea.

**Superposición y segmentos de color**
- `mastercard.svg` dos círculos superpuestos · `dreamhost.svg` media luna hecha con dos círculos · `chrome.svg` tres
  segmentos + núcleo · `google-icon.svg` G segmentada · `lit-icon.svg` llama facetada · `playwright.svg` dos máscaras.

**Reducción pictórica** — objetos reducidos a su silueta más característica.
- `apple.svg` · `redhat-icon.svg` · `couchbase.svg` · `docker-icon.svg` · `swift.svg` · `snowpack.svg` ·
  `stackoverflow-icon.svg` · `trello.svg` · `youtube-icon.svg` · `whatsapp.svg` · `gitlab.svg` (animal facetado).

**Mascotas resueltas con sencillez**
- `android-icon.svg` construido con primitivas redondeadas · `discord-icon.svg` control de videojuego = cara ·
  `github-icon.svg` silueta contundente en un círculo · `giantswarm.svg` glifos de terminal como ojos.

**Emblemas y contenedores**
- `markdown.svg` M + flecha dentro de un marco · `jupyter.svg` órbitas que enmarcan el nombre · `lua.svg` luna que
  orbita un planeta.

**Imagotipos como sistema**
- `soundcloud.svg` nube construida con barras de sonido · `tableau.svg` grupo de signos de suma que se repite en el
  nombre · `aws.svg` flecha-sonrisa bajo una tipografía sencilla · `arduino.svg` lazo de infinito que contiene − y + ·
  `microsoft.svg` cuatro cuadrados.

Más ejemplos: `python3 scripts/search_library.py --exemplary --type <type>` (141 archivos están marcados como
ejemplares).

## 5. Esquema del catálogo y cómo ampliar la biblioteca

Cada registro de `catalog.json`:

| Campo | Significado |
|---|---|
| `file`, `brand`, `variant` (`main`/`icon`), `pair` | identidad del archivo y de su contraparte |
| `width`, `height`, `aspect`, `aspect_class` | proporciones del lienzo |
| `bytes`, `shapes`, `anchors` | tamaño y complejidad |
| `colors`, `n_colors`, `color_families`, `primary_family`, `gradients`, `has_mask`, `has_filter` | datos de color |
| `mark_type`, `symbol_type` | `wordmark` (logotipo) · `lettermark` (sigla) · `letterform` (letra-símbolo) · `pictorial` (símbolo pictórico) · `abstract` (símbolo abstracto) · `mascot` (mascota) · `emblem` (emblema) · `combination` (imagotipo) |
| `subject` | qué representa, en pocas palabras (en inglés) |
| `geometry`, `techniques` | vocabulario de construcción (ver `--list-values`) |
| `type_style`, `case` | tipografía, cuando la hay |
| `mood`, `industry`, `exemplary`, `note` | tono, sector, marca de ejemplo didáctico y por qué lo es |

Para agregar logos: coloca los SVG en `assets/library/svg/`, añade a `classifications.json` objetos de clasificación
con las mismas claves y ejecuta `python3 scripts/build_catalog.py` (y `--check` para verificar la cobertura). Agrega
solo logos que tengas derecho a redistribuir como referencia.
