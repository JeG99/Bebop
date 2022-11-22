# The Bebop programming language

## Estado actual del lenguaje:
21-11-22

Estatus:
- Se añadió error de acceso a variable (o casilla de tipo indexado) no definida.
- Ejecución de acceso a arreglos y matrices funciona correctamente en contextos global y locales.
- Ejecución de llamadas de funciones funciona correctamente.
- Recursión implementada y funcionando.
- Se añadieron los 8 programas de prueba requeridos, solo falta mejorar las funciones especiales y mejorar su programa de prueba.

Falta:
- Permitir declaración de arreglos y matrices dentro de funciones.
- Agregar una función (o varias) para graficar arreglos
- Agregar una función de lectura de archivos csv
- Agregar manera de comentar al lenguaje
- Añadir una mejor versión de sqrt (la actual es una aproximación de un método numérico implementado en bebop)