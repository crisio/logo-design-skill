# Crítica de un logo

Úsalo cuando el usuario pida tu opinión sobre un logo (suyo o de cualquiera), quiera comparar opciones o necesite un
diagnóstico antes de un rediseño. Sé específico, amable y útil: di qué funciona, qué no, por qué y cómo corregirlo
exactamente.

## Método

1. **Primero entiende el contexto**: a qué se dedica la organización, para quién y qué debería transmitir. Un logo solo
   se puede juzgar en función de su propósito. Si no lo sabes, haz una sola pregunta o explica tus suposiciones.
2. **Primera impresión (2 segundos)**: ¿qué ves, qué sientes y qué recuerdas? ¿Cómo lo llamaría un desconocido?
3. **Revisión técnica**: si hay un SVG, ejecuta `scripts/svg_audit.py` y `scripts/preview_sheet.py`, y luego mira la
   hoja de pruebas. Si es una imagen rasterizada, evalúa visualmente esos mismos puntos.
4. **Revisión de principios**: califica del 1 al 5 cada dimensión de la tabla de abajo, con una línea de evidencia.
5. **Prioriza**: los 3 cambios de mayor impacto, del más importante al menos importante. Que cada uno sea concreto y
   aplicable.
6. **Demuestra (opcional)**: si el usuario lo quiere, bosqueja la corrección como una revisión en SVG.

## Tabla de puntaje

| Dimensión | Pregunta | Puntaje (1–5) | Evidencia |
|---|---|---|---|
| Idea | ¿Hay una sola idea, clara y pertinente? ¿Se puede decir en una frase? | | |
| Simplicidad | ¿Sobra algo? ¿Aguanta los 16 px y la prueba de ojos entrecerrados? | | |
| Diferenciación | ¿Se distingue de la competencia y de las marcas famosas? | | |
| Recordación | ¿Tiene un rasgo definitorio que recordarías mañana? | | |
| Pertinencia / tono | ¿Su carácter (forma, peso, color, tipografía) corresponde a la marca? | | |
| Oficio | ¿Geometría limpia, correcciones ópticas, pesos coherentes, buen espaciado y kerning? | | |
| Versatilidad | ¿Funciona a una tinta, en versión invertida, pequeño, grande, bordado, como ícono de app y en composiciones (lockups)? | | |
| Longevidad | ¿Se basa en un concepto más que en una moda? ¿Va a envejecer pronto? | | |
| Color | ¿Pocos colores, con propósito, propios, accesibles y reproducibles? | | |
| Tipografía | ¿Adecuada, personalizada, legible, bien espaciada, con ≤ 2 familias? | | |

El total sobre 50 es solo una guía aproximada; un solo defecto grave (ilegible en tamaño pequeño, parecido a un
competidor, una lectura ofensiva) pesa más que un total alto.

## Diagnósticos y correcciones frecuentes

| Síntoma | Causa probable | Corrección |
|---|---|---|
| Se vuelve una mancha en tamaños pequeños | Demasiados elementos, líneas delgadas, espacios estrechos | Quita detalles, engrosa los trazos, abre los espacios; haz una versión para tamaños pequeños |
| Se ve genérico o de plantilla | Tipografía de catálogo, símbolo trillado (globo terráqueo, trazo curvo tipo swoosh, bombilla) | Personaliza las letras, busca un giro propio, saca la idea del nombre o de la promesa |
| Se ve anticuado | Efectos (degradados, biseles, sombras), fuentes de moda | Aplánalo, simplifícalo, elige una dirección tipográfica más atemporal |
| Está recargado | Dos o tres ideas compitiendo | Quédate con una idea; lleva las demás al sistema de identidad |
| El símbolo y la tipografía parecen de marcas distintas | Lógicas distintas de geometría y peso | Comparte radios, grosores de trazo y ángulos; reequilibra los tamaños |
| Se siente inestable | Inclinación accidental, peso cargado arriba | Ensancha la base, corrige los ejes, revisa el centro óptico |
| El círculo se ve pequeño junto a las letras | Falta compensación óptica (overshoot) | Agranda las formas redondas un 1–3 % |
| El rectángulo redondeado se ve estrangulado | Efecto hueso | Suaviza las transiciones de curvatura |
| La versión invertida se ve más gruesa | Irradiación | Adelgaza un poco la versión en blanco |
| No funciona sobre fotos | Falta un recurso gráfico | Agrega una versión con contorno o contenedor |
| Un significado oculto que nadie ve | Demasiado sutil o demasiado complejo | Que sea un extra, no el punto central; o simplifícalo hasta que se lea |
| Una lectura desafortunada | Ceguera del diseñador tras mirarlo demasiado tiempo | Cambia la forma problemática; pruébalo con ojos frescos |

## Formato de respuesta

```markdown
## Crítica del logo — <nombre>
**Primera impresión:** <1–2 frases>
**Qué funciona:** <2–3 viñetas>
**Tabla de puntaje:** <la tabla de arriba, completa>
**Los 3 cambios principales (por orden de prioridad):**
1. <cambio>: por qué y cómo (concreto: "abre la contraforma de la e de 6 a 12 unidades")
2. …
3. …
**Siguiente paso (opcional):** <ofrece un SVG revisado o direcciones alternativas>
```

Tono: critica el trabajo, nunca a la persona. Equilibra la honestidad con el ánimo; el objetivo es una mejor marca
gráfica.
