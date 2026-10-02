# Cuestionario de rediseño para un agente que ya tiene marca

Úsalo cuando un agente ya tiene nombre, logo o personaje y se quiere **rediseñar**: nombre nuevo, símbolo nuevo o
peluche nuevo. Cambia lo que va entre «<>», copia todo lo que está debajo de la línea y pégalo en la sesión de Claude
Code que conoce el agente. Esa sesión responde con una **Ficha de rediseño**. Tráela a la sesión de diseño junto con la
primera Ficha de marca del agente.

Este cuestionario solo pide lo que está escrito en el proyecto. **Tus opiniones no las sabe el agente**: escríbelas
directo en la sesión de diseño. Son estas cinco:
1. Qué no te gusta del personaje o del logo actual, y dónde lo viste (Telegram, web, hoja de prueba).
2. Por qué quieres cambiar el nombre y si ya te gusta alguna idea.
3. Qué quieres conservar: el color, el trazo de la familia, los ojitos, el fieltro… o nada.
4. Qué camino prefieres en Telegram: el mismo bot con nombre y foto nuevos, o un bot nuevo.
5. Quién aprueba el nombre y el diseño, y para cuándo.

---

Vamos a **rediseñar la marca de este agente**: nombre nuevo, símbolo nuevo y personaje de peluche nuevo. Hoy se llama
«<nombre actual>» (antes «<nombres anteriores>») y su bot de Telegram es <@usuario del bot, o «no tiene»>. Es parte de
una familia de agentes que ya tienen nombre y color: <Nombre (función, color), …>. El nombre nuevo no puede repetir,
rimar ni sonar parecido a ninguno de ellos ni a «<nombre actual>», y el color nuevo no puede repetir el de otro agente.
Necesito información actualizada y real.

Reglas para responder:
- Antes de responder, revisa el código, el README, la configuración, el historial de cambios (git log), los documentos
  y los registros del proyecto (logs, tablas de mensajes o conversaciones, si existen).
- Responde todo en español. No inventes: si no lo sabes, escribe «No sé»; si lo deduces, escribe «Suposición:».
- Cuando pida ejemplos o citas, cópialos tal cual y cambia los datos sensibles por «XXX» (nombres de personas o
  proveedores, montos, números de registro).
- No copies tokens, contraseñas ni claves aunque aparezcan en la configuración: di solo en qué archivo o variable están.
- No cambies nada del proyecto: solo lee y responde. La única excepción son las capturas de la sección 10: guárdalas en
  una carpeta nueva **fuera del repositorio** y no hagas commits.
- Sé breve: una a tres líneas por punto, salvo en las citas y las tablas. Si un texto copiado pasa de 30 líneas, da la
  ruta del archivo y copia solo la parte que importa. Cuando nombres un archivo, da la ruta y la línea (`archivo:42`).
- Entrega la ficha en **un solo bloque** que abra y cierre con **cuatro** acentos graves (````markdown … ````) y con
  exactamente los títulos de abajo. Así los mensajes o el código que copies no rompen el bloque.

````markdown
## Ficha de rediseño — <nombre actual>

### 1. Inventario de lo que hoy dice «<nombre actual>»
Busca el nombre en todo el proyecto (sin node_modules, .next, dist ni build). Si el nombre es una palabra común del
idioma, separa los usos de la marca de la palabra normal. Una fila por cada lugar donde aparece el nombre, el logo, el
color de la marca o el personaje:

| Qué (nombre, logo, color o personaje) | Dónde (archivo:línea o pantalla) | ¿En producción? ¿Desde cuándo? | Quién lo ve | Cambio: fácil, medio o difícil, y por qué |
|---|---|---|---|---|

Incluye por lo menos: título de la pestaña, encabezado, favicon e íconos, chat («Pregúntale a…»), prompt del sistema
del agente de IA, PDF, Excel, correos (remitente y firma), mensajes de Telegram, nombre y foto del bot, sticker,
personaje o Kot (`kot-avatar.js`, `kot.png`), variables de entorno, base de datos, URL y documentación.
- Cuántos archivos hay que tocar para cambiar el nombre visible, y qué no conviene tocar (rutas, base de datos,
  repositorio):

### 2. Qué cambió y qué viene
- Funciones nuevas o cambiadas desde la primera ficha, con fecha:
- Qué funciones vienen en los próximos meses. ¿Va a manejar algo más que su tarea actual (otros temas, otros países)?

### 3. Cómo lo usan de verdad
- Si el proyecto guarda registros (chat, mensajes del bot, logs), cuenta los últimos 30 días: preguntas al chat, avisos
  enviados y personas distintas que lo usan. Si no hay registros, escribe «No hay registro» y luego «Suposición:»:
- Las 3 tareas que más se hacen, según esos registros o las pantallas más usadas:
- Un caso real reciente en el que el agente ayudó mucho, en 2–3 líneas:
- Errores o quejas registrados (commits de arreglo, issues, errores repetidos, mensajes molestos), con fecha:
- Cómo lo llaman las personas cuando le escriben o hablan de él. Busca el nombre actual, los anteriores, «el bot»,
  «el portal» y «el agente», y di cuál aparece más (citas con fecha):
- Comentarios escritos sobre el nombre, el logo o el personaje actuales (cita, fecha y el rol de quien lo dijo, sin
  nombre). Si no hay, escribe «No hay registro»:

### 4. El oficio y sus palabras
- 10 a 15 palabras del trabajo sacadas de la interfaz, la base de datos, los correos y los mensajes del bot, no
  inventadas. Marca con * las 5 que más aparecen:
- Expresiones o metáforas que el equipo usa por escrito (citas). Si no hay, escribe «No hay registro»:
- Los pasos de un trámite típico, de principio a fin, en máximo 8 pasos, con los objetos reales de cada paso:
- Qué momento del trabajo significa «todo en orden» y cómo lo dicen por escrito:

### 5. Voz
- Cómo se presenta hoy el agente: copia la parte del prompt del sistema (o del archivo de instrucciones) que define su
  nombre, su personalidad y su tono, con la ruta:
- Tú, usted o vos; emojis que usa y para qué; largo típico de un mensaje:
- 3 mensajes reales copiados tal cual: <el aviso principal que manda>, un aviso urgente y una respuesta del chat.
  Marca dónde aparece el nombre del agente en cada uno:
- Palabras sobre su personalidad que estén escritas en el proyecto (README, prompts, comentarios, guía de marca). Si
  no hay, escribe «No hay registro»:

### 6. Restricciones para el nombre nuevo
- Nombres de personas reales del equipo que aparezcan en el proyecto (para no repetirlos):
- Otros agentes, herramientas o bots de la empresa que no estén en la lista de la familia:
- Palabras que ya son estados, columnas, filtros, botones o comandos en el portal y en Telegram, copiadas del código.
  El nombre nuevo no puede ser una de ellas ni parecerse:
- ¿El bot o el chat reaccionan cuando alguien escribe o dicta el nombre del agente (mención, palabra clave, comando)?
  ¿Reciben notas de voz? ¿Cómo queda escrito el nombre al transcribirlo?
- Países donde se usa y modismos locales que conozcas y convenga evitar:
- Propón 6 nombres en español: una palabra, 2–3 sílabas, fáciles de decir y escribir, sin anglicismos. Que salgan del
  vocabulario de la sección 4, que no repitan ni rimen con los nombres de arriba y que no suenen a organismo del Estado.

| Nombre | De dónde sale | Posible choque (doble sentido en algún país, un estado del portal, otro agente) |
|---|---|---|

### 7. Telegram
- Dónde está el token (variable o archivo, no lo copies); si usa webhook o consulta periódica; dónde y cómo se
  programan los avisos:
- A quién le escribe (chats privados, grupo, tema) y dónde se guardan esos chat_id:
- Qué dice hoy cada texto que se cambia en @BotFather sin crear otro bot: nombre visible, descripción, «acerca de»,
  comandos y foto. ¿Ya existe un paquete de stickers del personaje? ¿Con qué nombre y enlace?
- Compara dos caminos. A) El mismo bot con nombre visible y foto nuevos (el @usuario viejo se sigue viendo en el
  perfil). B) Un bot nuevo con el nombre nuevo. Para cada uno: qué archivos cambian, qué tiene que hacer cada persona
  (volver a darle /start, agregarlo otra vez al grupo) y qué se pierde:

### 8. Identidad visual actual
- Colores copiados del archivo donde se definen:

| Token | HEX claro | HEX oscuro | Para qué se usa | Archivo |
|---|---|---|---|---|

- Cada estado con su color, su ícono o emoji y su texto exactos, en el portal, los PDF y Telegram. ¿Algún ícono de
  estado se parece al símbolo actual de la marca? ¿En qué pantallas aparecen juntos?
- El color de la marca: ¿es solo del logo o de toda la interfaz (botones, enlaces, foco)? ¿Algún estado usa ese color?
  ¿En cuántos lugares está escrito a mano en vez de usar el token?
- Colores oficiales o de la empresa que se ven dentro del portal o de sus documentos (logos o formatos de organismos,
  documentos escaneados, la marca de la empresa):
- Dónde se usan hoy el logo, el ícono y el personaje, y a qué tamaño en px:
- Tipografías de la interfaz y de los documentos; si hay modo oscuro y cómo se activa; si algo se imprime en blanco y
  negro:

### 9. Para el símbolo y el personaje
- Objetos, gestos o formas que el equipo ve o toca cada día en este trabajo y que podrían volverse una forma propia.
  Nada oficial ni de salud: sin cruces, sellos del Estado, escudos, banderas, pastillas, cápsulas ni lupas:
- Dónde aparece hoy el personaje (foto del bot, sticker, `<kot-avatar>`, bienvenida del chat, correos) y a qué tamaño.
  Si todavía no se usa en algún lugar, dilo:
- Reglas escritas en el proyecto o en la guía de marca sobre qué no usar, con su fuente:

### 10. Capturas (archivos aparte)
Si puedes controlar un navegador (Playwright, Chrome o similar), abre el portal solo para mirar y guarda, a 1440 px de
ancho, en una carpeta nueva fuera del repositorio: `01-inicio.png` (pantalla principal con el encabezado y el logo),
`02-estados.png` (la lista con los estados de colores), `03-chat.png` (el chat con una pregunta y su respuesta),
`04-oscuro.png` (modo oscuro, si existe), `05-movil.png` (pantalla principal a 390 px), y la primera página de un PDF
y de un Excel exportados. Usa datos de prueba o tapa nombres y números de registro. Si no puedes tomarlas, escribe la
URL o la ruta de cada pantalla.
- Carpeta de las capturas y lista de archivos:

### 11. Algo más
- Algo más que deba saber:
````
