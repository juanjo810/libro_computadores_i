# Session 9. ALU in Verilog

Ninth and last lab session. We will see how to include other source files in a Verilog program and we will use the 74181 arithmetic logic unit (ALU) seen in the theory lectures to carry out arithmetic and logic operations.

```{admonition} Learning objectives
:class: tip

- Include a source file inside another one with `` `include ``.
- Use an existing module, the 74181 ALU, from its diagram and its operation table.
- Chain several operations by storing the intermediate values in registers.
```

## Including source files

At any point, we can include another file, which will work just as if we had typed it at that point. The command is `` `include ``. So, to include the file `SumadorAuxiliar.v`, we type:

```verilog
`include "SumadorAuxiliar.v"
```

## Exercise 1

```{admonition} Statement
:class: note

The file [`74181.v`](https://juanjo810.github.io/libro_computadores_i/_static/verilog/sesion_09/74181.v) contains the Verilog code of the 74181 ALU seen in the theory lectures. Write a Verilog file with a module that carries out the following operations using that ALU:

1. 7+4
2. 2+6+1
3. $0110_2$ AND $1010_2$
4. $0110_2$ XOR $1010_2$
5. $0110_2$ OR NOT ($1010_2$ XNOR $0111_2$) (2 operations)
6. 2*7
7. 3*5+1 (2 operations)
```

You can find the original file at <https://github.com/lisper/cpus-caddr/blob/master/rtl/74181.v.orig>.

For multiple operations, registers must be used to store the intermediate values. Let us recall the diagram and the operation table of this integrated circuit:

```{figure} ../../_static/verilog/sesion_09/svg/74181.svg
---
name: fig-verilog-en-09-74181
alt: Diagram of the 74181 ALU. The four-bit operands A and B come in from the top. The four-bit operation select S, mode M and the negated carry in come in from the left. AEB and the negated carry out go out on the right, and the four-bit result F goes out at the bottom.
class: verilog-svg
width: 60%
align: center
---
Diagram of the 74181.
```

In the table, the vertical bar ($\mid$) stands for the OR operation, juxtaposition ($AB$) stands for the AND operation and the $+$ sign stands for arithmetic addition.

| $S$ | Arithmetic ($M=0$) | Logic ($M=1$) |
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

If you look at the module definition:

```verilog
module Circuit74181 (S, A, B, M, CNb, F, X, Y, CN4b, AEB);
```

you will notice that the negated carry lines are `CNb` and `CN4b`, respectively. Lines `X` and `Y` can be left unconnected.

| Port | Bits | Line in the diagram |
|---|:---:|---|
| `S` | 4 | Operation select $S$. |
| `A`, `B` | 4 | Operands $A$ and $B$. |
| `M` | 1 | Mode $M$: arithmetic (0) or logic (1). |
| `CNb` | 1 | Negated carry in, $\overline{C}_n$. |
| `F` | 4 | Result $F$. |
| `X`, `Y` | 1 | Can be left unconnected. |
| `CN4b` | 1 | Negated carry out, $\overline{C}_{n+4}$. |
| `AEB` | 1 | Output $AEB$. |

## Related shell commands

| Command | What it does |
|---|---|
| `ls` | Lists the contents of a directory. |
| `cd` | Changes the working directory. |
| `rm` | Deletes a file. |
| `man` | Shows the manual page of a command. |
| `cat` | Shows the contents of a file. |

## Original source

Content adapted to TeachBook from the reference page <http://avellano.usal.es/~compi/sesion9.htm> (© 2025 Guillermo González Talaván)
