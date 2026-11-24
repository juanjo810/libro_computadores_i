# Sesión 9. ALU en Verilog

Novena y última sesión de prácticas. Veremos cómo incluir otros ficheros fuente en un programa Verilog y usaremos la unidad aritmético-lógica (ALU) 74181 vista en teoría para realizar operaciones aritméticas y lógicas.

```{admonition} Objetivos de aprendizaje
:class: tip

- Incluir un fichero fuente dentro de otro con `` `include ``.
- Usar un módulo ya escrito, la ALU 74181, a partir de su esquema y de su tabla de operaciones.
- Encadenar varias operaciones guardando los valores intermedios en registros.
```

## Inclusión de ficheros fuente

Se puede, en un punto cualquiera, incluir otro fichero que funcionará tal y como si lo hubiéramos tecleado en dicho punto. La orden es `` `include ``. Así, si queremos incluir el fichero `SumadorAuxiliar.v`, tecleamos:

```verilog
`include "SumadorAuxiliar.v"
```

## Ejercicio 1

```{admonition} Enunciado
:class: note

El fichero [`74181.v`](https://juanjo810.github.io/libro_computadores_i/_static/verilog/sesion_09/74181.v) contiene el código Verilog de la ALU 74181 vista en teoría. Escríbase un fichero Verilog con un módulo que realice las siguientes operaciones usando dicha ALU:

1. 7+4
2. 2+6+1
3. $0110_2$ AND $1010_2$
4. $0110_2$ XOR $1010_2$
5. $0110_2$ OR NOT ($1010_2$ XNOR $0111_2$) (2 operaciones)
6. 2*7
7. 3*5+1 (2 operaciones)
```

Podéis encontrar el fichero original en <https://github.com/lisper/cpus-caddr/blob/master/rtl/74181.v.orig>.

En el caso de operaciones múltiples, se deben usar registros para almacenar los valores intermedios. Recordemos el esquema y la tabla de operaciones de este circuito integrado:

```{figure} ../../_static/verilog/sesion_09/svg/74181.svg
---
name: fig-verilog-09-74181
alt: Esquema de la ALU 74181. Por arriba entran los operandos A y B, de cuatro bits. Por la izquierda entran la selección de operación S, de cuatro bits, el modo M y el acarreo de entrada negado. Por la derecha salen AEB y el acarreo de salida negado, y por abajo sale el resultado F, de cuatro bits.
class: verilog-svg
width: 60%
align: center
---
Esquema del 74181.
```

En la tabla, la barra vertical ($\mid$) indica la operación OR, la yuxtaposición ($AB$) indica la operación AND y el signo $+$ indica la suma aritmética.

| $S$ | Aritmético ($M=0$) | Lógico ($M=1$) |
|:---:|:---:|:---:|
| 0000 | $A + C_n$ | $\overline{A}$ |
| 0001 | $A \mid B + C_n$ | $\overline{A \mid B}$ |
| 0010 | $A \mid \overline{B} + C_n$ | $\overline{A}B$ |
| 0011 | $-1 + C_n$ | $0$ |
| 0100 | $A + A\overline{B} + C_n$ | $\overline{AB}$ |
| 0101 | $(A \mid B) + A\overline{B} + C_n$ | $\overline{B}$ |
| 0110 | $A - B - 1 + C_n$ | $A \oplus B$ |
| 0111 | $A\overline{B} - 1 + C_n$ | $A\overline{B}$ |
| 1000 | $A + AB + C_n$ | $\overline{A} \mid B$ |
| 1001 | $A + B + C_n$ | $\overline{A \oplus B}$ |
| 1010 | $(A \mid \overline{B}) + AB + C_n$ | $B$ |
| 1011 | $AB - 1 + C_n$ | $AB$ |
| 1100 | $A + A + C_n$ | $1$ |
| 1101 | $(A \mid B) + A + C_n$ | $A \mid \overline{B}$ |
| 1110 | $(A \mid \overline{B}) + A + C_n$ | $A \mid B$ |
| 1111 | $A - 1 + C_n$ | $A$ |

Si observáis la definición del módulo:

```verilog
module Circuit74181 (S, A, B, M, CNb, F, X, Y, CN4b, AEB);
```

os daréis cuenta de que las líneas de acarreo negadas son `CNb` y `CN4b`, respectivamente. Las líneas `X` e `Y` las podéis dejar sin conectar.

| Puerto | Bits | Línea del esquema |
|---|:---:|---|
| `S` | 4 | Selección de operación $S$. |
| `A`, `B` | 4 | Operandos $A$ y $B$. |
| `M` | 1 | Modo $M$: aritmético (0) o lógico (1). |
| `CNb` | 1 | Acarreo de entrada negado, $\overline{C}_n$. |
| `F` | 4 | Resultado $F$. |
| `X`, `Y` | 1 | Se pueden dejar sin conectar. |
| `CN4b` | 1 | Acarreo de salida negado, $\overline{C}_{n+4}$. |
| `AEB` | 1 | Salida $AEB$. |

## Órdenes de la shell relacionadas

| Orden | Para qué sirve |
|---|---|
| `ls` | Lista el contenido de un directorio. |
| `cd` | Cambia el directorio de trabajo. |
| `rm` | Borra un fichero. |
| `man` | Muestra la página de manual de una orden. |
| `cat` | Muestra el contenido de un fichero. |

## Fuente original

Contenido adaptado a TeachBook a partir de la página de referencia <http://avellano.usal.es/~compi/sesion9.htm> (© 2025 Guillermo González Talaván)
