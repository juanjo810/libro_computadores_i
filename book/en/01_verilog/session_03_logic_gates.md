# Session 3. Logic Gates in Verilog

Third lab session. We will use Verilog to check how the logic gates seen in the theory lectures behave, and we will build the truth table of circuits made of several gates.

```{admonition} Learning objectives
:class: tip

- Instantiate Verilog primitive gates (`and`, `or`, `not`, `nand`, `nor`, `xor`, `xnor`, `buf`).
- Follow a simulation with `$monitor` and `$time`.
- Check truth tables with the values `0`, `1`, `x` and `z`.
- Connect several gates through auxiliary wires to build logic functions.
- Use Verilog relational and logical operators.
```

## AND gate

Let us recall from the theory lectures how an AND gate behaves:

```{figure} ../../_static/verilog/sesion_03/and.png
---
name: fig-verilog-en-03-and
alt: Truth table and symbol of the AND gate
width: 85%
align: center
---
AND gate: truth table, FALSE/TRUE equivalence and symbol.
```

Let us check, with Verilog, how this gate works:

```verilog
/* AND gate check: TestAnd.v */

module TestAnd;

  reg a,b; // Inputs
  wire  salida;

  and a1(salida,a,b);

  // Behavioural block
  initial
    begin
      $monitor($time," a=%b, b=%b, a.b=%b", a,b,salida);
      a=0; b=0;
      #5 a=0; b=1;
      #5 a=1; b=0;
      #5 a=1; b=1;
    end

endmodule
```

The program defines two **registers**, `a` and `b`, which provide the gate inputs, and a **wire**, `salida` (output), which carries the gate output for each value of `a` and `b`.

The gate itself is then created (**instantiated**) and given the name `a1`. For Verilog basic gates the name is optional; names are used to refer to the created elements. In the same line where the gate is created, its inputs and outputs are connected to the variables defined before.

```{figure} ../../_static/verilog/sesion_03/andvar.png
---
name: fig-verilog-en-03-andvar
alt: Instance a1 of an AND gate with inputs a and b and output salida
width: 35%
align: center
---
Instance `and a1(salida,a,b);`: the first argument is the output (a `wire`) and the following ones are the inputs (the `reg`s `a` and `b`).
```

```{admonition} Argument order
:class: important

In Verilog primitive gates **the output always comes first**, followed by the inputs: `and a1(salida, a, b);`.
```

Finally comes the **behavioural block** of the main module `TestAnd`. The `$monitor` command tells the simulator to watch the variables `a`, `b` and `salida`. Every time any of them changes, a line is printed automatically showing the simulation time (`$time`). Time units are arbitrary.

Next, `a` and `b` are initialised to zero. Five time units later (`#5`), `b` is set to one. The two remaining cases follow.

The program output gives the expected result:

```text
                   0 a=0, b=0, a.b=0
                   5 a=0, b=1, a.b=0
                  10 a=1, b=0, a.b=0
                  15 a=1, b=1, a.b=1
```

To try it, remember the workflow from session 0:

```bash
iverilog -o TestAnd TestAnd.v
./TestAnd
```

## Exercise 1

```{admonition} Statement
:class: note

Complete the AND gate table adding `x` (undefined) and `z` (high impedance) as possible inputs. The table must therefore have sixteen rows.
```

```{admonition} Hint
:class: seealso

To assign the undefined or high-impedance value to a register, use the constants `'bx` and `'bz`. For example: `#5 a=0; b='bx;`.
```

## Other simple gates in Verilog

Let us recall some other gates from the theory lectures and how they are written in Verilog. The pattern is always the same: output first, then inputs.

| Gate | Verilog | Expression |
|---|---|---|
| AND | `and(salida,a,b)` | $a \cdot b$ |
| OR | `or(salida,a,b)` | $a + b$ |
| NOT | `not(salida,a)` | $\overline{a}$ |
| NAND | `nand(salida,a,b)` | $\overline{a \cdot b}$ |
| NOR | `nor(salida,a,b)` | $\overline{a + b}$ |
| XOR | `xor(salida,a,b)` | $a \oplus b$ |
| XNOR | `xnor(salida,a,b)` | $\overline{a \oplus b}$ |
| BUFFER | `buf(salida,a)` | $a$ |

### OR gate · `or(salida,a,b)`

```{figure} ../../_static/verilog/sesion_03/or.png
---
name: fig-verilog-en-03-or
alt: Truth table and symbol of the OR gate
width: 85%
align: center
---
OR gate.
```

```verilog
reg a,b; // Inputs
wire salida;

or o1(salida,a,b);
```

### NOT gate · `not(salida,a)`

```{figure} ../../_static/verilog/sesion_03/not.png
---
name: fig-verilog-en-03-not
alt: Truth table and symbol of the NOT gate
width: 70%
align: center
---
NOT gate.
```

```verilog
reg a; // Input
wire salida;

not n1(salida,a);
```

### NAND gate · `nand(salida,a,b)` and NOR gate · `nor(salida,a,b)`

```{figure} ../../_static/verilog/sesion_03/nand.png
---
name: fig-verilog-en-03-nand
alt: Truth table and symbol of the NAND gate
width: 70%
align: center
---
NAND gate.
```

```{figure} ../../_static/verilog/sesion_03/nor.png
---
name: fig-verilog-en-03-nor
alt: Truth table and symbol of the NOR gate
width: 70%
align: center
---
NOR gate.
```

```verilog
reg a,b; // Inputs
wire salidaNand, salidaNor;

nand na1(salidaNand,a,b);
nor  no1(salidaNor,a,b);
```

### XOR gate · `xor(salida,a,b)` and XNOR gate · `xnor(salida,a,b)`

```{figure} ../../_static/verilog/sesion_03/xor.png
---
name: fig-verilog-en-03-xor
alt: Truth table and symbol of the XOR gate
width: 70%
align: center
---
XOR gate.
```

```{figure} ../../_static/verilog/sesion_03/xnor.png
---
name: fig-verilog-en-03-xnor
alt: Truth table and symbol of the XNOR gate
width: 70%
align: center
---
XNOR gate.
```

```verilog
reg a,b; // Inputs
wire salidaXor, salidaXnor;

xor  x1(salidaXor,a,b);
xnor xn1(salidaXnor,a,b);
```

### BUFFER gate · `buf(salida,a)`

```{figure} ../../_static/verilog/sesion_03/buf.png
---
name: fig-verilog-en-03-buf
alt: Truth table and symbol of the BUFFER gate
width: 70%
align: center
---
BUFFER gate.
```

```verilog
reg a; // Input
wire salida;

buf b1(salida,a);
```

## Exercise 2

```{admonition} Statement
:class: note

On paper, draw a table with sixteen rows and as many columns as logic gates seen. Fill it in with the outputs of each gate for every possible input combination made of `0`, `1`, `x` and `z`. Add the gates one by one to the code of the previous exercise and check with Verilog whether your table is correct.
```

```{admonition} Hint
:class: seealso

Declare a different output wire for each gate (`salidaAnd`, `salidaOr`, ...) and add all of them to the `$monitor` command. The `not` and `buf` gates only have one input: connect it to `a`.
```

## Interconnecting logic gates

We will build the truth table of the logic function $f_2(a,b,c) = ab + c$ with the help of Verilog.

```{figure} ../../_static/verilog/sesion_03/f2.png
---
name: fig-verilog-en-03-f2
alt: Circuit for f2 made of an AND gate of a and b whose output goes, together with c, into an OR gate
width: 60%
align: center
---
Circuit for $f_2(a,b,c) = ab + c$.
```

Instead of writing the 8 possible combinations of `a`, `b` and `c` by hand, we will build a three-bit register, initialise it to zero and increment it until it reaches 7 ($111_2$):

```verilog
// Truth table of f2(a,b,c)=ab+c

module f2;

  reg [2:0] r; // Inputs: a=r[2], b=r[1], c=r[0]
  wire  salida, ab;

  and a1(ab,r[2],r[1]);
  or  o1(salida,ab,r[0]);

  // Behavioural block
  initial
    begin
      $display("                     a b c | f2");
      $display("                     ----------");
      $monitor($time," %b %b %b | %b", r[2],r[1], r[0], salida);
      r=0; // r=000 => a=0, b=0, c=0
      while (r!='b111) #5 r=r+1;
    end

endmodule
```

Each value of register `r` corresponds to one input combination:

| `r` | Binary | `r[2]` = a | `r[1]` = b | `r[0]` = c |
|:---:|:---:|:---:|:---:|:---:|
| 0 | $000_2$ | 0 | 0 | 0 |
| 1 | $001_2$ | 0 | 0 | 1 |
| 2 | $010_2$ | 0 | 1 | 0 |
| 3 | $011_2$ | 0 | 1 | 1 |
| 4 | $100_2$ | 1 | 0 | 0 |
| 5 | $101_2$ | 1 | 0 | 1 |
| 6 | $110_2$ | 1 | 1 | 0 |
| 7 | $111_2$ | 1 | 1 | 1 |

An auxiliary wire `ab` connects the output of AND gate `a1` to one input of OR gate `o1`.

```{figure} ../../_static/verilog/sesion_03/f2var.png
---
name: fig-verilog-en-03-f2var
alt: Circuit for f2 with the Verilog names r[2], r[1], r[0], a1, ab, o1 and salida
width: 55%
align: center
---
The same circuit with the names used in the program: the auxiliary wire `ab` joins `a1` and `o1`.
```

The result of running it matches the table from the theory lectures:

```{figure} ../../_static/verilog/sesion_03/tablaf2.png
---
name: fig-verilog-en-03-tablaf2
alt: Truth table of f2 with columns a, b, c, ab and f2
width: 25%
align: center
---
Truth table of $f_2$ from the theory lectures.
```

```text
                     a b c | f2
                     ----------
                   0 0 0 0 | 0
                   5 0 0 1 | 1
                  10 0 1 0 | 0
                  15 0 1 1 | 1
                  20 1 0 0 | 0
                  25 1 0 1 | 1
                  30 1 1 0 | 1
                  35 1 1 1 | 1
```

## Relational operators

Besides `!=`, already seen, Verilog supports the following relational operators:

| Operator | Meaning |
|:---:|---|
| `<` | less than |
| `<=` | less than or equal to |
| `==` | equal to |
| `!=` | not equal to |
| `>=` | greater than or equal to |
| `>` | greater than |
| `===` | case equality (takes `x` and `z` into account) |
| `!==` | case inequality (takes `x` and `z` into account) |

When any operand contains `x` or `z`, the result is `x`. Otherwise, the result is 1 if the condition holds and 0 if it does not.

For a strict equality comparison (taking `x`s and `z`s into account) use `===` (case equality) and `!==` (case inequality).

## Logical operators

To express a condition inside a Verilog program we sometimes need the logical operators AND, OR and NOT. In Verilog they are written as:

| Operator | Meaning |
|:---:|---|
| `&&` | AND |
| `\|\|` | OR |
| `!` | NOT |

So, to express something like *"If it is not the case that a is greater than zero and b is different from four..."*, we would write:

```verilog
if (!(a>0 && b!=4)) ...
```

Applying De Morgan's laws, we know the same condition can be written as:

```verilog
if (a<=0 || b==4) ...
```

```{admonition} Do not mix up logical and bitwise operators
:class: warning

`&&`, `||` and `!` are **logical** operators: they return a single truth value. `&`, `|` and `~`, seen in session 2, operate **bit by bit** on registers.
```

## Exercise 3

```{admonition} Statement
:class: note

Build the truth table of function $f_3$ from the theory lectures, whose gate diagram is shown below:
```

```{figure} ../../_static/verilog/sesion_03/f3for.png
---
name: fig-verilog-en-03-f3for
alt: Expression f3(a,b,c) = bc + ab not c + not b c + c
width: 45%
align: center
---
Expression of function $f_3$.
```

```{figure} ../../_static/verilog/sesion_03/f3.png
---
name: fig-verilog-en-03-f3
alt: Gate diagram of f3 with two inverters, four AND gates and three OR gates
width: 65%
align: center
---
Gate diagram of $f_3(a,b,c) = bc + ab\overline{c} + \overline{b}c + c$.
```

```{admonition} Hint
:class: seealso

Follow the same scheme as for $f_2$: a register `reg [2:0] r` for the inputs and an auxiliary wire (`wire`) for each intermediate output in the diagram (inverters, AND gates and OR gates).
```

## Exercise 4

```{admonition} Statement
:class: note

Check, with a Verilog program, that function $f_3$ is equivalent to this other one built only with NAND gates:
```

```{figure} ../../_static/verilog/sesion_03/f3nand.png
---
name: fig-verilog-en-03-f3nand
alt: Circuit for f3 with three NAND gates
width: 50%
align: center
---
$f_3$ implemented with NAND gates only.
```

## Related shell commands

| Command | What it does |
|---|---|
| `ls` | Lists the contents of a directory. |
| `cd` | Changes the working directory. |
| `rm` | Deletes a file. |
| `man` | Shows the manual page of a command. |
| `cat` | Shows the contents of a file. |

## Original source

Content adapted to TeachBook from the reference page: <http://avellano.usal.es/~compi/sesion3.htm> (© 2010 Guillermo González Talaván).
