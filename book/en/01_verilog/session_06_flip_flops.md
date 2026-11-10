# Session 6. Flip-flops in Verilog

Sixth lab session. We will build flip-flops from logic gates with feedback, add a clock signal to them and see how non-blocking assignments and delays affect the behaviour of sequential circuits.

```{admonition} Learning objectives
:class: tip

- Build an RS flip-flop with NOR gates and add a clock input to it.
- Tell blocking assignment (`=`) from non-blocking assignment (`<=`).
- Generate a clock signal with an `always` block and use conditional `always` blocks (`@`, `posedge`, `negedge`).
- Build an edge-triggered flip-flop with a rising-edge detector.
- Write a JK flip-flop with PRESET and CLEAR and study the effect of delays.
```

## Exercise 1

```{admonition} Statement
:class: note

Write an RS flip-flop using two NOR gates.
```

```{figure} ../../_static/verilog/sesion_06/svg/rs.svg
---
name: fig-verilog-en-06-rs
alt: RS flip-flop made of two cross-coupled NOR gates, with inputs R and S and outputs Q and Q negated, next to its block symbol
class: verilog-svg
width: 85%
align: center
---
RS flip-flop with two NOR gates (left) and its symbol (right).
```

| Function | R | S | $Q_{n+1}$ | $\overline{Q}_{n+1}$ |
|---|:---:|:---:|:---:|:---:|
| Hold | 0 | 0 | $Q_n$ | $\overline{Q}_n$ |
| Set | 0 | 1 | 1 | 0 |
| Reset | 1 | 0 | 0 | 1 |
| Invalid | 1 | 1 | ? | ? |

````{admonition} Questions
:class: note

What is the output if the flip-flop is driven with this sequence of inputs?

```verilog
$monitor($time," R=%b, S=%b, Q=%b, NQ=%b", R, S, Q, NQ);
   R=0; S=0;
#5 R=0; S=1;
#5 R=0; S=0;
#5 R=1; S=0;
#5 R=1; S=1;
#5 R=0; S=0;
#5 R=1; S=1;
#5 S=0; R=0;
```

Why is the output different in the last line and in the third-to-last line?
````

## Non-blocking assignment

When several consecutive assignments appear in Verilog, they are carried out one after another. So the line

```verilog
#5 R=0; S=0;
```

first works out the result of assigning 0 to `R` and its consequences and, afterwards, assigns 0 to `S`.

Verilog has another kind of assignment, the **non-blocking assignment**. Its symbol is `<=`. When the non-blocking assignment is used,

```verilog
#5 R<=0; S<=0;
```

all values are assigned and their consequences are worked out at the same time.

| Assignment | Example | What happens |
|---|---|---|
| Blocking (`=`) | `#5 R=0; S=0;` | 1. `R=0` is assigned and its consequences are worked out. 2. `S=0` is assigned and its consequences are worked out. |
| Non-blocking (`<=`) | `#5 R<=0; S<=0;` | 1. `R` and `S` are set to 0. 2. The consequences are worked out. |

````{admonition} Try it
:class: note

What are the values of `a`, `b`, `c` and `d` at the end of the following example?

```verilog
module Asignaciones;

  integer a,b,c,d;

  initial
    begin
      $monitor($time," a=%d, b=%d, c=%d, d=%d", a,b,c,d);
      #5 a=1; b=2; c=3; d=4;
      #5 a=b; b=a;
      #5 c<=d; d<=c;
    end

endmodule
```
````

## Exercise 2

```{admonition} Statement
:class: note

Add an active-high clock input to the flip-flop of the previous exercise.
```

```{figure} ../../_static/verilog/sesion_06/svg/rsc.svg
---
name: fig-verilog-en-06-rsc
alt: Clocked RS flip-flop. R and S go through two AND gates together with clock C before reaching the two cross-coupled NOR gates. On the right, its block symbol.
class: verilog-svg
width: 85%
align: center
---
RS flip-flop with clock input (left) and its symbol (right).
```

| Function | C | R | S | $Q_{n+1}$ | $\overline{Q}_{n+1}$ |
|---|:---:|:---:|:---:|:---:|:---:|
| Hold | 0 | x | x | $Q_n$ | $\overline{Q}_n$ |
| Hold | 1 | 0 | 0 | $Q_n$ | $\overline{Q}_n$ |
| Set | 1 | 0 | 1 | 1 | 0 |
| Reset | 1 | 1 | 0 | 0 | 1 |
| Invalid | 1 | 1 | 1 | ? | ? |

## Clock signal. The always block

The `always` block tells Verilog to run the given code over and over again for as long as the simulation lasts. We can use an `always` block to build a clock signal:

```verilog
always #7 C=~C;
```

We assume that, to generate the clock signal, a register `C` has been defined beforehand. The `always` block above makes this register switch to its complementary value every 7 time units. We therefore get a clock with a period of 14 time units.

`always` is a block of the same kind as the `initial` block we already know. If it must contain more than one statement, they must be enclosed between `begin` and `end`, as usual.

(verilog-en-06-conditional-always)=
### Conditional always block

The name of a signal can be added to the `always` block so that the block runs whenever that signal changes:

```verilog
always @(variable)
  begin
    ...
  end
```

More than one signal can also be given, separated by commas, meaning that the block runs whenever any of those signals changes:

```verilog
always @(variable1,variable2, ...)
  begin
    ...
  end
```

Finally, by adding the words `posedge` or `negedge` before the variable name, the block runs on the rising or falling edge, respectively.

| Form | When the block runs |
|---|---|
| `always #7 C=~C;` | Over and over again, throughout the simulation. |
| `always @(variable)` | Every time `variable` changes. |
| `always @(variable1,variable2, ...)` | Every time any of the variables changes. |
| `always @(posedge C)` | On every rising edge of `C`. |
| `always @(negedge C)` | On every falling edge of `C`. |

## Exercise 3

```{admonition} Statement
:class: note

Add an `always` block to the tests of the previous exercise to generate a clock signal with a period of 14 time units. Note how the flip-flop only reacts to signals R and S while the clock is high.
```

## Exercise 4

```{admonition} Statement
:class: note

Modify the design of the previous exercise to build an RS flip-flop triggered on the rising edge of the clock. To do so, pass the clock signal through this rising-edge detector before feeding it to the flip-flop of the previous exercise.
```

```{figure} ../../_static/verilog/sesion_06/svg/det.svg
---
name: fig-verilog-en-06-det
alt: Rising-edge detector. Signal C goes through a NOT gate with a delay of one unit, giving Cnr, and through an AND gate together with C itself, giving DET. The timing diagram shows that DET has a short pulse right after each rising edge of C.
class: verilog-svg
width: 95%
align: center
---
Rising-edge detector (left) and its timing diagram (right).
```

The circuit is very simple. The NOT gate delays the signal by one time unit and inverts it. This modified signal and the original one go through an AND gate. The delay and the inversion produce small pulses right after each rising edge of the original signal.

Check that the flip-flop is now triggered on the rising edges of the clock.

## Exercise 5

```{admonition} Statement
:class: note

Write in Verilog and test this circuit, which implements a JK flip-flop that is active on a high clock level and has PRESET and CLEAR lines.
```

```{figure} ../../_static/verilog/sesion_06/svg/jk.svg
---
name: fig-verilog-en-06-jk
alt: JK flip-flop with four NAND gates, inputs J, C and K, active-low PRESET and CLEAR lines and feedback outputs Q and Q negated. On the right, its block symbol.
class: verilog-svg
width: 95%
align: center
---
JK flip-flop active on a high clock level with PRESET and CLEAR (left) and its symbol (right).
```

| Function | $\overline{PR}$ | $\overline{CL}$ | C | J | K | $Q_{n+1}$ | $\overline{Q}_{n+1}$ |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| Preset | 0 | 1 | x | x | x | 1 | 0 |
| Clear | 1 | 0 | x | x | x | 0 | 1 |
| Invalid | 0 | 0 | x | x | x | ? | ? |
| Hold | 1 | 1 | 1 | 0 | 0 | $Q_n$ | $\overline{Q}_n$ |
| Set | 1 | 1 | 1 | 1 | 0 | 1 | 0 |
| Reset | 1 | 1 | 1 | 0 | 1 | 0 | 1 |
| Toggle | 1 | 1 | 1 | 1 | 1 | $\overline{Q}_n$ | $Q_n$ |
| Hold | 1 | 1 | 0 | x | x | $Q_n$ | $\overline{Q}_n$ |

In particular, study the following:

1. With the clock signal held at zero, check that the PRESET and CLEAR signals are asynchronous.
2. With the clock signal held at one, and with PRESET and CLEAR inactive, check how inputs J and K work. When J and K are activated at the same time, the behaviour may not be the expected one, or the simulation may even hang. If so, press `Ctrl` + `C`.
3. Repeat the J=1 and K=1 test, but give all the NAND gates a delay of one time unit.
4. Investigate what happens when you play with the independent delays of each gate, until you reach a desirable behaviour.

As the last item shows, both feedback and delays are essential in sequential circuits.

## Related shell commands

| Command | What it does |
|---|---|
| `ls` | Lists the contents of a directory. |
| `cd` | Changes the working directory. |
| `rm` | Deletes a file. |
| `man` | Shows the manual page of a command. |
| `cat` | Shows the contents of a file. |

## Original source

Content adapted to TeachBook from the reference page <http://avellano.usal.es/~compi/sesion6.htm> (© 2025 Guillermo González Talaván)
