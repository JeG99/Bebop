# Bebop - the data exploration language

## Análisis léxico-sintáctico:

Estatus:
- Funciona correctamente.
- 28 conflictos shift/reduce (todos relacionados con operadores lógicos, comparativos y aritméticos, pero NO necesariamente son errores).
- Se separó la sintaxis de declaracion de variables y estatutos en bloques opcionales
- A las funciones void no se les permite llevar estatuto return, por sintaxis
- A las funciones con return type se les obliga a llevar estatuto return, por sintaxis
- Error de sintaxis

Mejoras:
- Cambiar los parámetros de las funciones especiales para que sintácticamente acepten los tipos y cantidades de argumentos correctos.
- Comentarios para separar las reglas gramaticales por grupos.

## Análisis semántico:

Estatus:
- Se añadió el cubo semántico
- Error de type mismatch por operación
- Error de type mismatch por asignación
- Error de variable no declarada
- Error de función no declarada
- Error de variable ya declarada en el scope actual
