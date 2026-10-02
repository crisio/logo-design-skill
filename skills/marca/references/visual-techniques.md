# Técnicas visuales y correcciones ópticas

La capa de oficio: cómo se perciben las formas y las pequeñas correcciones que separan un buen logo de uno
perfecto. Léelo durante el desarrollo y el refinamiento (fases 4–5), y cuando hagas una crítica.

## Contenido
1. Geometría, retículas y proporción áurea
2. Equilibrio (estabilidad, proporción, composición, consistencia, escalabilidad)
3. Correcciones ópticas: compensación óptica (overshoot), efecto hueso, irradiación, igualar tamaños a la vista
4. Dinámica de composición entre formas
5. Simetría vs. asimetría
6. Sólido vs. línea
7. Anguloso vs. redondeado
8. Espacio negativo y figura/fondo
9. Paradojas visuales: figuras imposibles, ambigüedad, movimiento
10. Degradados, luz y sombreado
11. Dimensión
12. Recursos de visibilidad (contorno, contenedor)
13. Patrones
14. Revisar con ojos frescos

---

## 1. Geometría, retículas y proporción áurea

- **Mira el mundo como geometría simple.** Entrénate para reducir los objetos a círculos, cuadrados, triángulos y
  sus partes. Cuando sientes la estructura que hay detrás de las cosas, componer se vuelve más fácil y los
  resultados se sienten inevitables.
- **Construye a partir de primitivas.** Círculos, arcos de radios consistentes, líneas rectas en ángulos
  deliberados. Las curvas hechas con segmentos de círculo son fáciles de reticular y de reproducir; las curvas a
  mano alzada son más difíciles de justificar y de corregir.
- **La proporción áurea (≈1.618) y las proporciones de Fibonacci** (1, 2, 3, 5, 8, 13, 21 …) sirven como criterio
  de orden: p. ej., radios de círculos en una construcción que siguen 1 : 1.618 o múltiplos de Fibonacci. Úsalas
  donde ayuden; nunca dejes que los números se impongan a una forma que ya se siente bien. Si una forma se siente
  bien, las matemáticas no deberían estorbar.
- **Ángulos enteros.** Busca ángulos limpios: 0°, 15°, 30°, 45°, 60°, 90°. Un elemento a 43° debería estar a 45°;
  uno a 33.46° debería pasar a 30° o 35°. Las líneas que se desvían 1–2° de la horizontal o la vertical se leen como
  errores, y los ángulos limpios demuestran que los elementos se colocaron a propósito. (Lo mismo con los valores de
  color: prefiere porcentajes CMYK enteros.)
- **Primitivas perfectas.** Un círculo debe ser un círculo perfecto y un cuadrado, un cuadrado perfecto, salvo que la
  desviación sea una corrección óptica intencional.
- **La retícula es para terminar, no para empezar.** Aplica retículas de construcción después de que se apruebe el
  concepto, para encontrar y corregir desalineaciones, radios desiguales y ángulos desviados. Los cambios suelen ser
  demasiado pequeños para que el público los note de forma consciente, pero sí siente la diferencia.
- **No abuses de la retícula.** Puede que las curvas orgánicas complejas no se descompongan en círculos; está bien
  dejarlas sin reticular. Si algo no funciona dentro de la retícula, haz que funcione fuera de ella. Un dibujo de
  construcción saturado de docenas de círculos sin sentido es un truco de presentación, no rigor.

## 2. Equilibrio

1. **Estabilidad**: el logo no debe parecer inclinado por accidente. Debe haber una sensación de gravedad; cuando el
   concepto lo permite, una base más pesada o más ancha se siente bien asentada.
2. **Proporción**: busca una huella general más cercana a un cuadrado que a un rectángulo alargado. Los símbolos muy
   altos o muy anchos son incómodos de usar y de combinar con texto en una composición (lockup). (Datos de la
   biblioteca: ~76 % de los íconos independientes están entre 0.8 : 1 y 1.25 : 1.)
3. **Composición**: distribuye los elementos y los espacios de forma pareja. Las aglomeraciones en una zona y el
   vacío en otra crean disonancia (a menos que la tensión sea la intención).
4. **Consistencia**: mantén los pesos relacionados entre sí. Algo muy grueso junto a algo muy delgado se lee como
   desequilibrio; en los logos de línea, mantén el mismo grosor de trazo en todo el diseño. Repite radios y ángulos.
5. **Escalabilidad**: cada decisión debe sobrevivir a la ampliación y a la reducción.

## 3. Correcciones ópticas

### Compensación óptica (overshoot)
Las formas redondas y puntiagudas se ven más pequeñas que las formas de borde plano con la misma altura medida. Un
círculo colocado entre cuadrados de igual altura se ve demasiado pequeño; una `O` junto a una `H` se ve baja. Deja
que las curvas y los vértices sobresalgan un poco de la línea base, la línea de mayúsculas o el borde: normalmente
**1–3 % de la altura** para las curvas y más para las puntas agudas (triángulos y vértices pueden necesitar 3–6 %).
Hazlo en la etapa final, con uno o dos ajustes de puntos de anclaje. Esta es la diferencia entre excelente y
perfecto.

### Efecto hueso
Donde una curva se une de forma tangente con una línea recta (una cápsula: dos semicírculos unidos por lados rectos;
rectángulos redondeados; triángulos redondeados), el segmento recto parece estrecharse hacia dentro, como un hueso.
Soluciones, de la más rápida a la mejor:
1. Estira las curvas de los extremos hasta volverlas elipses (lo suaviza, pero no lo elimina).
2. Alarga los manejadores de la curva para que la curvatura aumente de forma gradual en vez de saltar de cero al
   círculo completo.
3. Usa una transición de curvatura suave (una esquina tipo "squircle" o superelipse): puntos de anclaje extra que
   pasan con suavidad de recto a curvo; copia la curva ya ajustada a las esquinas simétricas.
No hace falta corregir todos los casos: a veces el efecto hueso es expresivo (da volumen a una figura). Corregirlo
suele liberar espacio interior y hace que los logos redondeados se vean más nítidos en tamaños pequeños. En SVG,
cuando la esquina es prominente, prefiere esquinas de curvatura continua (Béziers cúbicas con manejadores de
≈ 0.55–0.65 del tamaño de la esquina, extendidas más allá del punto de tangencia) en lugar de simples arcos `rx`.

### Irradiación: el blanco sobre negro se ve más grande
Una forma clara sobre fondo oscuro se ve más grande y más gruesa que la misma forma oscura sobre fondo claro.
Consecuencias:
- Un logo en versión invertida (blanco sobre oscuro) se ve más pesado. Entrega una **versión invertida con trazos
  un poco más delgados** (aproximadamente un 2–5 % del grosor del trazo), o reduce un poco la escala de la versión
  invertida. Para lograrlo, desplaza el trazado hacia dentro (expande un trazo delgado y réstalo de la forma).
- Prueba ambas versiones lado a lado hasta que se vean iguales; anota en la guía de marca qué archivo usar.
- Las líneas blancas delgadas sobre fondos oscuros pueden "expandirse" visualmente y cerrarse al imprimir; mantén
  abiertas las contraformas.

### Igualar tamaños a la vista en formas mixtas
Círculos, cuadrados y triángulos con la misma caja delimitadora no se ven del mismo tamaño. Iguálalos a ojo: los
círculos, un poco más grandes que los cuadrados; los triángulos, más grandes todavía. Lo mismo aplica a los íconos de
un set.

### Trazos horizontales vs. verticales
Los trazos horizontales se ven más pesados que los verticales del mismo grosor. En rotulación y en logos
geométricos, haz los horizontales un poco más delgados (a menudo un 5–10 %) para que se vean iguales. Donde los
trazos se unen en ángulos agudos, adelgázalos cerca de la unión para evitar que la tinta se acumule (el problema que
resuelven las trampas de tinta) y forme manchas oscuras en tamaños pequeños.

### Centro óptico
El centro óptico de un área está un poco por encima del centro geométrico. Un logo centrado matemáticamente en un
contenedor a menudo se ve bajo; súbelo un poco. Las formas asimétricas (un triángulo que apunta a la derecha, un
botón de reproducción) deben desplazarse hacia su masa visual, no hacia su caja delimitadora.

## 4. Dinámica de composición entre formas

Las formas crean sensaciones al interactuar. Primero define el objetivo —armonía, tensión, dinamismo, equilibrio,
disonancia, entropía— y después organiza.
- Círculo apoyado sobre un cuadrado del mismo ancho → armonía, estabilidad.
- Cuadrado en equilibrio sobre un círculo → tensión, inestabilidad.
- Círculo junto al vértice de un triángulo → movimiento.
- Círculo justo encima del vértice de un triángulo → tensión equilibrada.
- Diagonales y formas que se afinan → movimiento; horizontales → calma; verticales → aspiración, fuerza.
- Densidad que aumenta a lo largo de una forma (líneas o puntos que pasan de dispersos a densos) → movimiento
  implícito.

La intuición se construye con años de jugar con formas; mientras tanto, prueba variaciones lado a lado.

## 5. Simetría vs. asimetría

- La simetría de espejo perfecta es estable y formal, pero a menudo aburrida; la repetición por reflejo puede
  sentirse mecánica.
- Una asimetría sutil mantiene la mirada en movimiento: un cambio de color en un lado, un detalle agregado o quitado,
  un elemento descentrado, una parte reflejada y luego desplazada.
- Es especialmente útil cuando la silueta general es simétrica: deja que un detalle la rompa.
- La simetría sigue teniendo su lugar en instituciones y en logos que deben sentirse absolutos (sellos, organismos
  públicos).

## 6. Sólido vs. línea

- **Los logos sólidos** se ven estables y fuertes; sus siluetas siguen siendo claras en tamaños pequeños y a
  distancia; las formas contundentes se reproducen bien en cualquier medio.
- **Los logos de línea (monolínea o contorno)** se ven ligeros y elegantes; funcionan bien para marcas serenas o
  refinadas, iconografía de interfaz y señalética interior. Desventajas: son débiles a distancia y en tamaños
  pequeños, a menos que los trazos sean lo bastante gruesos, y son más vulnerables a una mala reproducción.
- Si un logo funciona de las dos formas, elige una como **principal** y la otra como secundaria.
- En el SVG final, convierte los trazos en contornos rellenos (consulta `svg-construction.md`) para que, al escalar,
  la relación entre línea y tamaño no cambie de forma impredecible.

## 7. Anguloso vs. redondeado

- Las formas agudas y angulosas se leen como asertivas, autoritarias, técnicas y a veces amenazantes: por instinto
  tratamos los objetos afilados con cautela.
- Las formas redondeadas se leen como amigables, acogedoras, suaves y seguras: dan ganas de tocarlas y sostenerlas.
- Mantén los elementos afilados fuera de la silueta, a menos que la marca necesite filo (seguridad, deporte,
  rendimiento, precisión de lujo). La mayoría de las marcas quieren sentirse cercanas, así que las esquinas
  redondeadas son un buen punto de partida; pero una esquina apenas redondeada (radio pequeño) suele verse más
  premium que las formas totalmente de píldora.
- Mezcla: un exterior afilado con detalles interiores suaves (o al revés) puede expresar dualidad ("seguro pero
  amigable").

## 8. Espacio negativo y figura/fondo

- Toda silueta tiene espacio a su alrededor. Trata las formas negativas (contraformas, huecos, espacio entre
  elementos) con el mismo cuidado que las positivas: cuando las formas internas de las letras hacen eco de la forma
  exterior, se crea coherencia.
- Un espacio negativo ingenioso (una flecha oculta, un animal entre dos formas, una letra tallada en un objeto) crea
  un momento de descubrimiento. Mantenlo simple: dos elementos con siluetas distintas y relacionados en el concepto.
- Los huecos deben ser lo bastante grandes para sobrevivir a la reducción; un hueco de 1 px a 32 px desaparece. Como
  regla práctica, haz que el hueco más pequeño mida ≥ 1/32 del ancho del logo si debe leerse en tamaños de favicon.

## 9. Paradojas visuales

Cuando algo parece ser una cosa y, al mirarlo de cerca, se convierte en otra, la mente resuelve un pequeño problema y
disfruta la solución. Hay tres familias:
1. **Figuras imposibles**: formas que no pueden existir en 3D (perspectiva invertida, conexiones de líneas
   manipuladas, capas desalineadas). Estudia el concepto, no copies figuras famosas; traslada el principio (p. ej.,
   una letra cuya perspectiva cambia de dirección a la mitad).
2. **Formas ambiguas**: una imagen que se lee como dos. Es raro lograrlo a propósito. El riesgo mayor es la lectura
   *no intencionada*: después de horas de trabajo, quien diseña deja de ver lo que es obvio para los demás (incluidas
   lecturas sexuales u ofensivas). Pide siempre una mirada fresca, gira el logo 90/180° y míralo diminuto y reflejado.
3. **Ilusiones de movimiento**: barridos que se afinan, líneas de velocidad, repetición progresiva. Para transmitir
   velocidad, haz que la forma pase de delgada a gruesa en la dirección de lectura (de izquierda a derecha en las
   culturas de escritura latina); ten en cuenta al público que lee de derecha a izquierda.

Otras herramientas para convertir una forma común en algo memorable: superponer capas, entrelazar, solapar con
transparencia, contraponer lo plano y lo dimensional, y jugar con el color en las intersecciones.

## 10. Degradados, luz y sombreado

- **Los degradados son fáciles y, por eso mismo, un cliché.** Pueden suavizar un logo y darle profundidad, pero se
  reproducen mal: los degradados RGB intensos pierden fuerza en la impresión CMYK y se difuminan en tamaños pequeños.
  A menos que el logo sea solo digital, conserva una versión plana como archivo maestro y trata los degradados como
  una mejora opcional.
- **Simplifica la gradación.** Sustituye un degradado continuo por unos pocos pasos definidos (3–5 bandas planas de
  tonos relacionados). En tamaños pequeños, los pasos se leen como continuos; en tamaños grandes, se ven trabajados
  con oficio en lugar de genéricos.
- **Luz y sombreado para logos simples.** Lo simple no siempre es atractivo: algunos logos se ven sosos porque les
  falta contenido. Introducir una fuente de luz (un pliegue, la sombra de un solapamiento, un brillo) puede aportar
  profundidad y sofisticación. Si el logo es interesante en su estado reducido, no le agregues luz.
- **Pocos tonos.** Muchos tonos de gris matan la nitidez en tamaños pequeños. Usa como máximo brillo, un tono medio,
  sombra y fondo (una reducción de claroscuro "luz–oscuridad"). Para letras-símbolo y símbolos abstractos, suele
  bastar con un tono medio aplicado a las partes que se doblan por debajo o se superponen a otras.
- **Estructura de la luz sobre una esfera**: brillo, tono medio, sombra propia, luz reflejada, sombra proyectada,
  sombra de oclusión. Entiéndela para sombrear cualquier forma de manera convincente; después redúcela a 2–3 tonos.
- **Trazos afinados (estilo grabado)**: gradación tonal construida con trazos en forma de flecha que se adelgazan
  hacia la punta; una manera versátil de dar volumen a formas orgánicas. Lleva mucho tiempo; resérvalo para marcas en
  las que el oficio es el mensaje.

## 11. Dimensión

- Los renders 3D realistas llevan demasiado detalle para un logo.
- La dimensión lograda con los medios más simples —dos o tres caras planas, un pliegue isométrico, un solapamiento—
  puede ser impactante y amplía el terreno de soluciones originales, ya que las combinaciones planas de primitivas
  están casi agotadas.
- Conserva siempre una versión que funcione plana y a una tinta.

## 12. Recursos de visibilidad

Un logo diseñado para fondos claros puede no invertirse bien (un cisne blanco invertido se vuelve un cisne negro:
quizá sea lo deseado, quizá no). Para fondos recargados, fotográficos o multicolor, usa un **recurso gráfico**:
- Un contorno (un trazo claro lo bastante grueso alrededor de la silueta), o
- Una forma contenedora: círculo para logos circulares; cuadrado o cuadrado redondeado para casi todos los demás (lo
  más seguro para formatos rectangulares e íconos de app). Un contenedor básico quizá no sea lo más bello, pero es
  funcional.
- Las proporciones del recurso deben coincidir con las del logo (logo cuadrado → recurso cuadrado; logo ancho →
  recurso ancho); si no coinciden, queda un espacio vacío que distrae.

## 13. Patrones

- La retícula es el corazón de un patrón. Las retículas cuadradas son las más versátiles, pero también las más
  comunes → todo termina pareciéndose. Prueba triángulos, hexágonos, cuadrados girados (rombos) o retículas
  derivadas de los ángulos del logo.
- Los teselados simples son directos, pero se vuelven aburridos; prefiere retículas que permitan variación.
- Distribuye el color de forma pareja; demasiado contraste interrumpe el flujo y muy poco lo vuelve invisible.
- Cuando sea posible, deriva los componentes del logo para que el patrón y el logo se sientan relacionados sin
  duplicarse.
- Prueba en varias escalas (tarjeta, muro, vehículo) y, para impresión, mantén una cobertura de tinta razonable.

## 14. Revisar con ojos frescos (el enfoque dialéctico)

- **Guarda cada iteración significativa** y ponlas lado a lado en vez de sobrescribirlas. Es común que quien diseña
  prefiera una variante inferior en el momento de entusiasmo y pierda la mejor.
- **Compara por pares** de forma directa y elige la más fuerte; luego itera a partir de la ganadora.
- **Descansa antes de decidir**: el cansancio vuelve el juicio menos objetivo.
- **Refleja el logo.** Voltearlo horizontalmente revela problemas de proporción a los que el ojo ya se acostumbró
  (sobre todo en animales y figuras).
- **Difumina, entrecierra los ojos y reduce.** Si la silueta no se entiende difuminada, la idea no es lo bastante
  fuerte.
- **Ayudas físicas**: para figuras complejas, las referencias y las maquetas 3D sencillas (papel, arcilla, alambre)
  revelan mejores puntos de vista e incoherencias.
