# Session 5. Routers and adders in Verilog

Fifth lab session. We will work with tri-state buffers and with wires that can receive several signals at the same time, and we will use them to build routers (a bus transceiver and multiplexers) and adders. We will finish by modelling gate delays.

```{admonition} Learning objectives
:class: tip

- Use tri-state buffers (`bufif1`, `bufif0`, `notif1`, `notif0`) and the high-impedance value `z`.
- Understand how Verilog resolves signal contention on `tri` wires and on special wires.
- Permanently connect a register to a wire with `assign`.
- Build routers and adders by combining modules.
- Stop the simulation with `$stop` and `$finish` and add delays to gates.
```

## Tri-state buffers

In the theory lectures we saw the following buffers, which have an extra control line to put the output in high impedance:

```{figure} ../../_static/verilog/sesion_05/svg/bufif1.svg
---
name: fig-verilog-en-05-bufif1
alt: Active-high tri-state buffer. If G is 0 the output Y is in high impedance; if G is 1, Y copies the value of A.
class: verilog-svg
width: 80%
align: center
---
Tri-state buffer with active-high control.
```

```{figure} ../../_static/verilog/sesion_05/svg/bufif0.svg
---
name: fig-verilog-en-05-bufif0
alt: Active-low tri-state buffer. If the control line is 0, Y copies the value of A; if it is 1, Y is in high impedance.
class: verilog-svg
width: 80%
align: center
---
Tri-state buffer with active-low control.
```

The Verilog statements that instantiate the first buffer (`bufif1`) and the second one (`bufif0`) are:

```verilog
bufif1 bIzquierda(Y,A,G);
bufif0 bDerecha(Y,A,G);
```

There are also the equivalent NOT gates with active-high and active-low tri-state control, `notif1` and `notif0` respectively:

```verilog
notif1 n1(Y,A,G);
notif0 n0(Y,A,G);
```

| Primitive | Active control | Output with active control | Output with inactive control |
|---|:---:|:---:|:---:|
| `bufif1` | 1 | A | z |
| `bufif0` | 0 | A | z |
| `notif1` | 1 | $\overline{A}$ | z |
| `notif0` | 0 | $\overline{A}$ | z |

```{admonition} Argument order
:class: important

As with the other gates, the output comes first, then the data input and finally the control line: `bufif1 b(output, input, control);`.
```

## Signal contention

Several signals may be driven onto a wire at the same time. For Verilog to handle these cases correctly, whenever several signals may coincide, the variable must be declared not as `wire` but as `tri`.

When there is contention on a `tri` variable, it is resolved as follows:

- Signals `1`, `0` or `x` always take priority over high-impedance signals (`z`).
- Ignoring high-impedance signals, if all signals agree, the result is that value. Otherwise, the result is `x`.

Applying these two rules to a `tri` wire driven by two signals gives:

| Signal 1 ↓ · Signal 2 → | 0 | 1 | x | z |
|:---:|:---:|:---:|:---:|:---:|
| **0** | 0 | x | x | 0 |
| **1** | x | 1 | x | 1 |
| **x** | x | x | x | x |
| **z** | 0 | 1 | x | z |

Some logic designs need wires with special behaviour. When there is contention, they act as follows:

| Wire | Behaviour on contention |
|---|---|
| `tri0` | Like `tri`, but if all signals are `z`, the value is `0` (*pull-down* resistor). |
| `tri1` | Same, with value `1` (*pull-up* resistor). |
| `wand` or `triand` | A single `0` makes the result `0`. |
| `wor` or `trior` | A single `1` makes the result `1`. |

## Assigning signals to wires

To permanently connect a register to a wire, we use an **assignment**. It makes the value of the register flow continuously onto the wire. The Verilog statement is `assign`:

```verilog
wire w; reg r;
assign w=r;
```

If two assignments drive the same wire, it must be declared as `tri`, and its value is resolved with the table in the previous section:

```verilog
reg ra, rb;
tri a;
assign a=ra;
assign a=rb;   // Two signals on the same wire
```

## Exercise 1

```{admonition} Statement
:class: note

Let us apply what we have learnt with the following example of a one-bit bus transmitter/receiver, seen in the theory lectures.
```

```{figure} ../../_static/verilog/sesion_05/svg/trans.svg
---
name: fig-verilog-en-05-trans
alt: One-bit bus transmitter/receiver. Inputs G negated and DIR control, through two AND gates, two tri-state buffers that connect A and B in one direction or the other.
class: verilog-svg
width: 85%
align: center
---
One-bit bus transmitter/receiver (transceiver).
```

| $\overline{G}$ | DIR | Operation |
|:---:|:---:|---|
| 0 | 0 | data B → A |
| 0 | 1 | data A → B |
| 1 | x | isolation |

Let us write the module:

```verilog
module Transceiver(inout tri a, inout tri b, input wire g, input wire dir);

  wire ng,ndir,sa1,sa2;

  not (ng,g);        // Not referenced later => no names given
  not (ndir,dir);
  and (sa1,ng,dir);
  and (sa2,ng,ndir);
  bufif1 (b,a,sa1);
  bufif1 (a,b,sa2);

endmodule
```

In the code, line $\overline{G}$ of the figure is called `g`. It is still active low: `not (ng,g)` plays the role of the negation bubbles on the AND gates. The names used are:

```{figure} ../../_static/verilog/sesion_05/svg/trans_nombres.svg
---
name: fig-verilog-en-05-trans-nombres
alt: Transceiver with the Verilog module names g, dir, a, b, sa1 and sa2
class: verilog-svg
width: 85%
align: center
---
The transceiver with the names used in module `Transceiver`.
```

Each line of the module matches a part of the diagram:

| Code | Diagram element |
|---|---|
| `inout tri a, inout tri b` | Bidirectional ports `a` and `b`. They are `tri` because they may receive several signals. |
| `input wire g, input wire dir` | Control inputs. |
| `not (ng,g); not (ndir,dir);` | Negation bubbles on the AND gate inputs. |
| `and (sa1,ng,dir);` | AND gate that produces `sa1`. |
| `and (sa2,ng,ndir);` | AND gate that produces `sa2`. |
| `bufif1 (b,a,sa1);` | Tri-state buffer from `a` to `b`, controlled by `sa1`. |
| `bufif1 (a,b,sa2);` | Tri-state buffer from `b` to `a`, controlled by `sa2`. |

Now we build the test module:

```{figure} ../../_static/verilog/sesion_05/svg/trans_test.svg
---
name: fig-verilog-en-05-trans-test
alt: Transceiver connected to registers g, dir, ra and rb of the test module
class: verilog-svg
width: 90%
align: center
---
The transceiver connected to the registers of module `TestTransceiver`.
```

```verilog
module TestTransceiver;

  tri a,b;
  reg g,dir;
  reg ra,rb;

  Transceiver t(a,b,g,dir);
  assign a=ra; assign b=rb;

  // Behavioural block
  initial
    begin
      $monitor($time," g=%b, dir=%b, a=%b, b=%b, ra=%b, rb=%b",
                     g,dir,a,b,ra,rb);
         ra=0; rb=1; g=1; dir=0;
      #5 ra='bz; rb='bz; g=1; dir=0;
      #5 rb=1; g=0; dir=0;
      #5 ra='bz; rb='bz; g=1; dir=1;
      #5 ra=0; g=0; dir=1;
      #5 ra=0; rb=1; g=0; dir=1;
    end

endmodule
```

| Code | Role in the test |
|---|---|
| `tri a,b;` | Wires connected to the bidirectional ports of the transceiver. |
| `reg g,dir;` | Registers that set the control signals. |
| `reg ra,rb;` | Registers that drive values onto `a` and `b` from outside the transceiver. |
| `Transceiver t(a,b,g,dir);` | Module instance. |
| `assign a=ra; assign b=rb;` | Permanent connection of the registers to the wires. |


## Exercise 2

```{admonition} Statement
:class: note

Build a 4x1 multiplexer module with an output-enable control line OE, so that when this line is inactive the output Y is in high impedance. Otherwise, it works as a normal multiplexer. With two of these multiplexers, build an 8x1 multiplexer module following the diagram in the figure. Test it with an auxiliary module.
```

```{figure} ../../_static/verilog/sesion_05/svg/mux8x1.svg
---
name: fig-verilog-en-05-mux8x1
alt: 8x1 multiplexer made of two 4x1 multiplexers. Negated S2 enables the first one and S2 enables the second; S1 and S0 go to both and their Y outputs are joined.
class: verilog-svg
width: 85%
align: center
---
8x1 multiplexer built from two 4x1 multiplexers with an OE line.
```

## Exercise 3

```{admonition} Statement
:class: note

Build a half-adder module and check that it works correctly.
```

```{figure} ../../_static/verilog/sesion_05/svg/semisuma.svg
---
name: fig-verilog-en-05-semisuma
alt: Half adder HA with inputs e1 and e2 and outputs s and co; inside, an XOR gate gives the sum and an AND gate the carry.
class: verilog-svg
width: 85%
align: center
---
Half adder: block (left) and its inside (right).
```

## Exercise 4

```{admonition} Statement
:class: note

Using the module built in the previous exercise, write a full adder and check that it works.
```

```{figure} ../../_static/verilog/sesion_05/svg/sumador1.svg
---
name: fig-verilog-en-05-sumador1
alt: Full adder made of two half adders HA1 and HA2 and an OR gate that combines their carries
class: verilog-svg
width: 85%
align: center
---
Full adder built from two half adders.
```

## Stopping the simulation

Verilog has two commands to stop the simulation early: `$stop` and `$finish`.

The difference is that the first one stops the simulation but enters debug mode, where the values of registers and signals can be inspected, while the second one ends the simulation for good.

| Command | Effect |
|---|---|
| `$stop` | Stops the simulation and enters debug mode. |
| `$finish` | Ends the simulation for good. |

## Exercise 5

```{admonition} Statement
:class: note

Using the one-bit full adder of the previous exercise, build a four-bit ripple-carry adder module.
```

```{figure} ../../_static/verilog/sesion_05/svg/propaga4.svg
---
name: fig-verilog-en-05-propaga4
alt: Four-bit adder made of four full adders FA0 to FA3; the carry out of each one is the carry in of the next one.
class: verilog-svg
width: 95%
align: center
---
Four-bit ripple-carry adder.
```

## Gate delays

So far we have assumed that when the inputs of a gate change, the output adapts to the new situation instantly. This is far from true: there is a **propagation delay**.

Verilog can model these delays in great detail: independent values can be set for the 0 to 1 transition, the 1 to 0 transition and the transition from any value to high impedance. As a first approximation, here we will use the same value for all transitions.

To specify that a gate has a delay, after the gate type we add the `#` symbol and the delay time units in parentheses:

```text
<gate_type> #(<time>) <name>(<connections>);
```

For example:

```verilog
and #(7) a1(salida, entrada1, entrada2); // AND with delay 7
```

## Exercise 6

```{admonition} Statement
:class: note

Add a delay of two time units to the gates of the four-bit ripple-carry adder of the previous exercise. Looking at the diagram, work out the safety delay of this design (when the output can be guaranteed to hold the correct value and not a transition). Try some input values in practice and check the delays that occur.
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

Content adapted to TeachBook from the reference page <http://avellano.usal.es/~compi/sesion5.htm> (© 2025 Guillermo González Talaván).
