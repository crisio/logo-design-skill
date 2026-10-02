# Cuestionario de marca para un agente o proyecto

Copia todo lo que está debajo de la línea y pégalo en la sesión de Claude Code que conoce el agente o proyecto.
Esa sesión responde con una **Ficha de marca**. Trae la ficha a la sesión de diseño y úsala como brief.

---

Necesito crear la identidad visual (nombre, logo y kit de marca) del agente/proyecto en el que trabajas en esta sesión.
Antes de responder, revisa el código, el README y la configuración del proyecto para contestar con datos reales.

Reglas para responder:
- Responde todo en español.
- No inventes. Si no lo sabes, escribe «No sé». Si puedes deducirlo, escribe «Suposición:» y tu mejor respuesta.
- Sé concreto: frases cortas, sin jerga técnica cuando hables de lo que hace el agente.
- Entrega la respuesta completa en **un solo bloque de código markdown** con exactamente los títulos de abajo, para
  que yo pueda copiarla de una vez.

```markdown
## Ficha de marca — <nombre actual del agente o proyecto>

### 1. Identidad
- Nombre actual (escrito exacto, con mayúsculas):
- ¿Es definitivo o provisional? ¿La gente ya le dice de otra forma (apodo)?
- Ruta absoluta de la carpeta del proyecto:
- Qué hace, en una frase que entienda cualquier persona:
- Sus 3 a 5 funciones principales:
- Qué problema resuelve y a quién. Qué pasaría si no existiera:
- Qué lo hace diferente de otras opciones:

### 2. Usuarios
- Quién lo usa (perfil, edad aproximada, profesión, país, nivel técnico):
- ¿Lo usan clientes, el equipo interno o ambos?
- Dónde y cómo lo usan (WhatsApp, web, app iOS/Android, Slack, correo, terminal, otro):
- Qué deben sentir, pensar o hacer después de usarlo:

### 3. Personalidad
- 3 a 5 palabras de cómo debe sentirse la marca:
- 2 o 3 palabras de cómo NO debe sentirse:
- Si fuera una persona, ¿cómo hablaría y cómo se vería?
- Tono de sus mensajes (formal o cercano, tú o usted, con o sin emojis):
- Su promesa o gran idea, en una línea:

### 4. Contexto
- ¿Pertenece a una empresa o a una familia de productos o agentes? ¿Cuál? ¿Debe parecerse a los demás?
- Competidores o productos parecidos:
- Marcas o logos que te gustan, y por qué:
- Símbolos, colores o clichés de su sector que hay que evitar:

### 5. Lo que ya existe en el código
- ¿Ya hay logo, ícono o favicon? Rutas de los archivos:
- Colores definidos (hex, variables CSS, tokens, tailwind.config, Assets.xcassets, etc.):
- Tipografías que usa:
- Plataforma y tecnología (framework web, iOS, Android, bot, CLI…):
- Dónde se colocan los íconos y el logo dentro del proyecto:

### 6. Dónde aparecerá el logo (ordena por prioridad)
- Favicon, ícono de app, avatar o foto de perfil del bot, encabezado web, correos, PDF o facturas, redes sociales,
  impresos, uniformes, letreros, otro:
- ¿Necesita modo oscuro? ¿Tamaños muy pequeños? ¿Impresión a una sola tinta o bordado?

### 7. Nombre
Propón 5 nombres en español para este agente:
- Cortos: una sola palabra, de 2 a 3 sílabas.
- Fáciles de decir y de escribir para un hispanohablante, sin letras raras ni anglicismos.
- Relacionados con lo que hace o con cómo debe sentirse.
- Que no sean de una marca conocida del mismo sector, hasta donde sepas.

| Nombre | Por qué |
|---|---|
| | |

### 8. Proyecto
- Estado (idea, prototipo, en producción) y fecha de lanzamiento:
- ¿Quién decide la versión final?
- Qué entregables necesitas (logo, ícono de app, favicon, avatar, guía de uso, otro):
- Algo más que deba saber:

### 9. Personaje 3D (opcional)
- Rasgos del logo o de la identidad que debe conservar:
- Textura que mejor le va (fieltro, peluche de pelo corto, arcilla suave o goma mate) y por qué:
- Dónde se usará el personaje (avatar del bot, chat, bienvenida, presentaciones):
- Qué hay que evitar en el personaje:
```
