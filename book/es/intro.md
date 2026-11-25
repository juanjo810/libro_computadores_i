# Computadores I

Bienvenido al libro de prácticas de **Computadores I**.

Este material acompaña el aprendizaje de los fundamentos de diseño digital usando **Verilog** como lenguaje de descripción de hardware. La asignatura parte de una idea sencilla: un computador no es una caja mágica, sino una composición ordenada de señales, puertas lógicas, módulos, registros, contadores y unidades aritmético-lógicas.

## Qué vas a aprender

Al trabajar con este libro aprenderás a:

- describir circuitos digitales mediante módulos Verilog;
- simular el comportamiento de puertas lógicas, buses, biestables, registros y contadores;
- interpretar señales, estados y retardos de propagación;
- construir componentes combinacionales y secuenciales de forma incremental;
- relacionar cada ejercicio con los esquemas y tablas de referencia de la sesión.

## Cómo está organizado el curso

El curso se estructura en sesiones prácticas. Cada sesión incluye las explicaciones de Verilog que hacen falta, los enunciados de los ejercicios y los esquemas y tablas de referencia, para no perder de vista el circuito que se está programando.

```{admonition} Método de trabajo recomendado
:class: tip

Antes de escribir código, identifica las entradas, salidas y señales internas del circuito. Después consulta las figuras de referencia, escribe el módulo Verilog y comprueba la simulación. Si el resultado no coincide con lo esperado, vuelve a la figura y revisa las conexiones.
```

## Índice de sesiones

| Sesión | Qué se trabaja |
|---|---|
| [Sesión 0. Terminal de Ubuntu para Verilog](01_verilog/sesion_00_terminal_ubuntu.md) | Carpetas, archivos, editores básicos y primer contacto con `iverilog`. |
| [Sesión 1. Introducción a Verilog](01_verilog/sesion_01_introduccion.md) | Entorno de trabajo, módulos básicos y salida por pantalla. |
| [Sesión 2. Operaciones con bits](01_verilog/sesion_02_operaciones.md) | Máscaras, paridad y reducción de bits. |
| [Sesión 3. Puertas lógicas en Verilog](01_verilog/sesion_03_puertas_logicas.md) | AND, OR, NOT, NAND, NOR, XOR, XNOR y funciones combinacionales. |
| [Sesión 4. Módulos en Verilog](01_verilog/sesion_04_modulos.md) | Interfaces, jerarquía de módulos y comparadores. |
| [Sesión 5. Encaminadores y sumadores en Verilog](01_verilog/sesion_05_encaminadores_y_sumadores.md) | Búferes triestado, multiplexores, sumadores y retardos de puerta. |
| [Sesión 6. Biestables en Verilog](01_verilog/sesion_06_biestables.md) | Biestables RS y JK, señal de reloj, flancos y bloques `always`. |
| [Sesión 7. Registros en Verilog](01_verilog/sesion_07_registros.md) | Modelos de comportamiento, registros de desplazamiento y cronogramas con GTKwave. |
| [Sesión 8. Contadores en Verilog](01_verilog/sesion_08_contadores.md) | Contadores ascendentes/descendentes, contador síncrono y transiciones de estado. |
| [Sesión 9. ALU en Verilog](01_verilog/sesion_09_alu.md) | Inclusión de ficheros y uso de la ALU 74181. |

Las sesiones están pensadas para seguirse en orden: cada una reutiliza lo construido en las anteriores. También puedes cambiar al libro en inglés desde el selector de idioma de la barra superior.

## Fuente de referencia

Prácticamente todas las sesiones de este libro están basadas en las prácticas de la página web de la asignatura **Computadores I** de la Universidad de Salamanca, elaborada por Guillermo González Talaván:

<http://avellano.usal.es/~compi/>

Al final de las sesiones 1 a 9 se enlaza la página original de la que procede su contenido.
