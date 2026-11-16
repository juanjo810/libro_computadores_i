# Session 8. Counters in Verilog

Eighth lab session. We will build counters from T and JK flip-flops, see what happens when the counting direction is changed halfway through and analyse a counter with an arbitrary counting sequence.

```{admonition} Learning objectives
:class: tip

- Write an up/down counter built from T flip-flops.
- Add PRESET, CLEAR and HOLD lines to a flip-flop without modifying its inside.
- Check that a synchronous counter with JK flip-flops works.
- Analyse a counter with an arbitrary counting sequence and build its state transition diagram.
```

## Counters

A counter is a digital circuit that increments or decrements its count one by one, following a clock signal. Counters are built with flip-flops, such as T and JK flip-flops:

```{figure} ../../_static/verilog/sesion_08/svg/biestables.svg
---
name: fig-verilog-en-08-biestables
alt: Symbols of a T flip-flop, with a clock input triggered on the falling edge and output Q, and of a JK flip-flop, with inputs J, C and K and outputs Q and Q negated
class: verilog-svg
width: 55%
align: center
---
T flip-flop (left) and JK flip-flop (right).
```

In the counters of this session we will find:

| Lines | What they are for |
|---|---|
| DEC/$\overline{\text{INC}}$ and C | Inputs: counting mode (decrement or increment) and clock signal. |
| $Q_n \ldots Q_0$ | Output: the number of the count (5, 4, 3, 2...). |
| PRESET, CLEAR and HOLD | Additional inputs, asynchronous and active low. |

## Exercise 1

```{admonition} Statement
:class: note

Write in Verilog the following counter, which can count up or down. Check it. Use a four-bit variable for the output instead of four one-bit variables.
```

```{figure} ../../_static/verilog/sesion_08/svg/contador.svg
---
name: fig-verilog-en-08-contador
alt: Four-bit counter with four chained T flip-flops. Clock C goes into the first one. Between every two flip-flops, an XOR gate combines the Q output of the previous one with the DEC/INC-negated line, and its output is the clock of the next one. The outputs are Q1, Q2, Q3 and Q4.
class: verilog-svg
width: 100%
align: center
---
Up/down counter.
```

What do you observe if you change the mode selection line (increment or decrement) halfway through, without clearing the counter?

Add active-low, asynchronous PRESET and CLEAR lines to the flip-flops of the counter. Modify the design by adding an extra HOLD line, also active low, so that if that line is active, the flip-flop does not respond to signal T. Use the PRESET and CLEAR inputs for this; do not modify the inside of the T flip-flop.

Run a last simulation in which, every time you change the counting mode, you activate HOLD beforehand and deactivate it afterwards, so that the count changes direction normally, with no jumps.

````{admonition} Solutions and comments: solution
:class: dropdown

First, a module that simulates the behaviour of a T flip-flop, that is, one that changes the state of its output on every falling edge of the clock signal:

```verilog
module T(output reg Q, input wire C);
  always @(negedge C)
  begin
    Q=~Q;
  end

  initial
  begin
    Q=0;
  end
endmodule
```

We name the flip-flops, the gates and the wires:

```{figure} ../../_static/verilog/sesion_08/svg/contador_nombres.svg
---
name: fig-verilog-en-08-contador-nombres
alt: Up/down counter with the names used in the code. The flip-flops are called T1 to T4; the XOR gates, x1 to x3; their outputs, b1 to b3; the flip-flop outputs, Q[0] to Q[3], and the mode line, DECnINC.
class: verilog-svg
width: 100%
align: center
---
Up/down counter with flip-flop, gate and wire names.
```

And we write the module:

```verilog
module contador(output wire [3:0] Q, input wire C, input wire DECnINC);
  wire b1, b2, b3;

  xor x1(b1, Q[0], DECnINC);
  xor x2(b2, Q[1], DECnINC);
  xor x3(b3, Q[2], DECnINC);

  T T1(Q[0], C);
  T T2(Q[1], b1);
  T T3(Q[2], b2);
  T T4(Q[3], b3);
endmodule
```

We build a test module with a clock signal of period 10. For 100 time units we set the counter to count down and, for the next 100 units, to count up:

```verilog
module prueba;
  reg rC, rDECnINC;
  wire [3:0] cQ;
  contador pedro(cQ, rC, rDECnINC);

  initial
    begin
      $monitor($time," DECnINC=%b, C=%b, Q=%b(%d)", rDECnINC, rC, cQ, cQ);
      rC=0; rDECnINC=1;
      #100 rDECnINC=0;
      #100 $finish;
    end

  always
    begin
      #5 rC=~rC;
    end
endmodule
```

We run it and get the following result:

```text
  0 DECnINC=1, C=0, Q=1111(15)
  5 DECnINC=1, C=1, Q=1111(15)
 10 DECnINC=1, C=0, Q=1110(14)
 15 DECnINC=1, C=1, Q=1110(14)
 20 DECnINC=1, C=0, Q=1101(13)
 25 DECnINC=1, C=1, Q=1101(13)
 30 DECnINC=1, C=0, Q=1100(12)
 35 DECnINC=1, C=1, Q=1100(12)
 40 DECnINC=1, C=0, Q=1011(11)
 45 DECnINC=1, C=1, Q=1011(11)
 50 DECnINC=1, C=0, Q=1010(10)
 55 DECnINC=1, C=1, Q=1010(10)
 60 DECnINC=1, C=0, Q=1001( 9)
 65 DECnINC=1, C=1, Q=1001( 9)
 70 DECnINC=1, C=0, Q=1000( 8)
 75 DECnINC=1, C=1, Q=1000( 8)
 80 DECnINC=1, C=0, Q=0111( 7)
 85 DECnINC=1, C=1, Q=0111( 7)
 90 DECnINC=1, C=0, Q=0110( 6)
 95 DECnINC=1, C=1, Q=0110( 6)
100 DECnINC=0, C=0, Q=1001( 9)
105 DECnINC=0, C=1, Q=1001( 9)
110 DECnINC=0, C=0, Q=1010(10)
115 DECnINC=0, C=1, Q=1010(10)
120 DECnINC=0, C=0, Q=1011(11)
125 DECnINC=0, C=1, Q=1011(11)
130 DECnINC=0, C=0, Q=1100(12)
135 DECnINC=0, C=1, Q=1100(12)
140 DECnINC=0, C=0, Q=1101(13)
145 DECnINC=0, C=1, Q=1101(13)
150 DECnINC=0, C=0, Q=1110(14)
155 DECnINC=0, C=1, Q=1110(14)
160 DECnINC=0, C=0, Q=1111(15)
165 DECnINC=0, C=1, Q=1111(15)
170 DECnINC=0, C=0, Q=0000( 0)
175 DECnINC=0, C=1, Q=0000( 0)
180 DECnINC=0, C=0, Q=0001( 1)
185 DECnINC=0, C=1, Q=0001( 1)
190 DECnINC=0, C=0, Q=0010( 2)
195 DECnINC=0, C=1, Q=0010( 2)
```

The counter works as expected. Every time the clock signal falls (goes from 1 to 0), the counter goes down or up depending on the counting mode we have set. However, as the statement says, there is a small jump in the count when changing from counting down to counting up (time 100). This jump makes sense because the output of the XOR gates changes when signal `DECnINC` changes, and this changes the T input of the flip-flops.

```{figure} ../../_static/verilog/sesion_08/svg/cron_salto.svg
---
name: fig-verilog-en-08-cron-salto
alt: Timing diagram of the counter without a HOLD line. The count goes down from 15 to 6 and, when DECnINC changes at t=100, it jumps from 6 to 9 and keeps going up.
class: verilog-svg
width: 100%
align: center
---
Timing diagram of the counter: when the counting mode changes, the count jumps from 6 to 9.
```
````

````{admonition} Solutions and comments: improved solution
:class: dropdown

We continue improving the counter following the instructions in the statement of the exercise.

The first thing is to add active-low PRESET and CLEAR lines to the T flip-flop. We take the chance to build a negated Q output so that the flip-flop is as complete as possible:

```{figure} ../../_static/verilog/sesion_08/svg/t_completo.svg
---
name: fig-verilog-en-08-t-completo
alt: T flip-flop with clock input C triggered on the falling edge, outputs Q and nQ and lines nCLEAR and nPRESET at the bottom
class: verilog-svg
width: 60%
align: center
---
T flip-flop with nCLEAR and nPRESET lines and nQ output.
```

```verilog
module T(output reg Q, output wire nQ,
         input wire C, input wire nCLEAR, input wire nPRESET);
  not N(nQ, Q);

  always @(negedge C)
  begin
    if (nCLEAR==1 && nPRESET==1) Q=~Q;
  end

  always @(nCLEAR)
  begin
    if (nCLEAR==0) Q=0;
  end

  always @(nPRESET)
  begin
    if (nPRESET==0) Q=1;
  end

  initial
  begin
    Q=0;
  end
endmodule
```

We have added code so that:

1. When line `nCLEAR` is activated, the flip-flop is set to 0.
2. When line `nPRESET` is activated, the flip-flop is set to 1.
3. Output `nQ` is a wire connected to register `Q` through a NOT gate.
4. Signals `nCLEAR` and `nPRESET` take priority over the clock signal (the `if` statement in the `always` block of signal `C`).

We follow the instructions and build a `Thold` module with an inner `T` module and an extra line, `nHOLD`, which, when active, makes the flip-flop ignore the clock signal. No sooner said than done:

```{figure} ../../_static/verilog/sesion_08/svg/thold.svg
---
name: fig-verilog-en-08-thold
alt: T flip-flop with a HOLD line. Two OR gates combine nHOLD with Q and with nQ. Their outputs go, together with nCLEAR and nPRESET, into two AND gates that feed the nCLEAR and nPRESET lines of the T flip-flop.
class: verilog-svg
width: 70%
align: center
---
T flip-flop with a HOLD line.
```

We can see how signals `nCLEAR` and `nPRESET`, when active, are passed on to the T flip-flop with priority. If they are inactive and `nHOLD` is also inactive, everything works as if the T flip-flop had not been modified.

However, when `nHOLD` is active (equal to 0), `Q` is passed on to `nCLEAR` and `nQ` is passed on to `nPRESET`. The net effect is that, in these circumstances, the flip-flop keeps its value and, since these lines take priority, the flip-flop ignores clock `C`, just what we wanted. Let us add names:

```{figure} ../../_static/verilog/sesion_08/svg/thold_nombres.svg
---
name: fig-verilog-en-08-thold-nombres
alt: T flip-flop with a HOLD line and the names used in the code. The flip-flop is called jose; the AND gates, aC and aP; the OR gates, oC and oP, and the wires, cCLEAR, cPRESET, cOC and cOP.
class: verilog-svg
width: 70%
align: center
---
T flip-flop with a HOLD line and gate and wire names.
```

And now, the code:

```verilog
module Thold(output wire Q, output wire nQ,
             input wire C, input wire nCLEAR, input wire nPRESET, input wire nHOLD);
  wire cCLEAR, cPRESET, cOC, cOP;
  T jose(Q, nQ, C, cCLEAR, cPRESET);
  and aC(cCLEAR, nCLEAR, cOC);
  or oC(cOC, nHOLD, Q);
  and aP(cPRESET, nPRESET, cOP);
  or oP(cOP, nHOLD, nQ);
endmodule
```

In the `contador` module above, the old `T` flip-flops must be replaced with the new `Thold` ones. Their extra lines are left unconnected (`nQ`) or inactive, that is, equal to 1 (`nCLEAR` and `nPRESET`):

```verilog
module contador(output wire [3:0] Q,input wire C,input wire DECnINC, input wire nHOLD);
  wire b1,b2,b3;

  xor x1(b1,Q[0],DECnINC);
  xor x2(b2,Q[1],DECnINC);
  xor x3(b3,Q[2],DECnINC);

  Thold T1(Q[0], ,  C, 1'b1, 1'b1, nHOLD);
  Thold T2(Q[1], , b1, 1'b1, 1'b1, nHOLD);
  Thold T3(Q[2], , b2, 1'b1, 1'b1, nHOLD);
  Thold T4(Q[3], , b3, 1'b1, 1'b1, nHOLD);
endmodule
```

And, finally, in the test module. Line `nHOLD` is activated temporarily when we want to change the counting direction:

```verilog
module prueba;
  reg rC;
  reg rDECnINC;
  reg rnHOLD;
  wire [3:0] cQ;
  contador pedro(cQ,rC,rDECnINC,rnHOLD);

  initial
  begin
        $monitor($time," DECnINC=%b nHOLD=%b C=%b Q=%b(%d)",
                 rDECnINC,rnHOLD,rC,cQ,cQ);
        rC=0;
        rDECnINC=1;
        rnHOLD=1;
        #99 rnHOLD=0;   /* nHOLD temporarily at 0 */
        #1  rDECnINC=0;
        #1  rnHOLD=1;   /* Restore nHOLD to 1 */
        #99 $finish;
  end
  always
  begin
        #5 rC=~rC;
  end
endmodule
```

The output is the expected one:

```text
  0 DECnINC=1 nHOLD=1 C=0 Q=1111(15)
  5 DECnINC=1 nHOLD=1 C=1 Q=1111(15)
 10 DECnINC=1 nHOLD=1 C=0 Q=1110(14)
 15 DECnINC=1 nHOLD=1 C=1 Q=1110(14)
 20 DECnINC=1 nHOLD=1 C=0 Q=1101(13)
 25 DECnINC=1 nHOLD=1 C=1 Q=1101(13)
 30 DECnINC=1 nHOLD=1 C=0 Q=1100(12)
 35 DECnINC=1 nHOLD=1 C=1 Q=1100(12)
 40 DECnINC=1 nHOLD=1 C=0 Q=1011(11)
 45 DECnINC=1 nHOLD=1 C=1 Q=1011(11)
 50 DECnINC=1 nHOLD=1 C=0 Q=1010(10)
 55 DECnINC=1 nHOLD=1 C=1 Q=1010(10)
 60 DECnINC=1 nHOLD=1 C=0 Q=1001( 9)
 65 DECnINC=1 nHOLD=1 C=1 Q=1001( 9)
 70 DECnINC=1 nHOLD=1 C=0 Q=1000( 8)
 75 DECnINC=1 nHOLD=1 C=1 Q=1000( 8)
 80 DECnINC=1 nHOLD=1 C=0 Q=0111( 7)
 85 DECnINC=1 nHOLD=1 C=1 Q=0111( 7)
 90 DECnINC=1 nHOLD=1 C=0 Q=0110( 6)
 95 DECnINC=1 nHOLD=1 C=1 Q=0110( 6)
 99 DECnINC=1 nHOLD=0 C=1 Q=0110( 6)
100 DECnINC=0 nHOLD=0 C=0 Q=0110( 6)
101 DECnINC=0 nHOLD=1 C=0 Q=0110( 6)
105 DECnINC=0 nHOLD=1 C=1 Q=0110( 6)
110 DECnINC=0 nHOLD=1 C=0 Q=0111( 7)
115 DECnINC=0 nHOLD=1 C=1 Q=0111( 7)
120 DECnINC=0 nHOLD=1 C=0 Q=1000( 8)
125 DECnINC=0 nHOLD=1 C=1 Q=1000( 8)
130 DECnINC=0 nHOLD=1 C=0 Q=1001( 9)
135 DECnINC=0 nHOLD=1 C=1 Q=1001( 9)
140 DECnINC=0 nHOLD=1 C=0 Q=1010(10)
145 DECnINC=0 nHOLD=1 C=1 Q=1010(10)
150 DECnINC=0 nHOLD=1 C=0 Q=1011(11)
155 DECnINC=0 nHOLD=1 C=1 Q=1011(11)
160 DECnINC=0 nHOLD=1 C=0 Q=1100(12)
165 DECnINC=0 nHOLD=1 C=1 Q=1100(12)
170 DECnINC=0 nHOLD=1 C=0 Q=1101(13)
175 DECnINC=0 nHOLD=1 C=1 Q=1101(13)
180 DECnINC=0 nHOLD=1 C=0 Q=1110(14)
185 DECnINC=0 nHOLD=1 C=1 Q=1110(14)
190 DECnINC=0 nHOLD=1 C=0 Q=1111(15)
195 DECnINC=0 nHOLD=1 C=1 Q=1111(15)
```

And the timing diagram speaks for itself:

```{figure} ../../_static/verilog/sesion_08/svg/cron_contador.svg
---
name: fig-verilog-en-08-cron-contador
alt: Timing diagram of the counter with a HOLD line. The count goes down from 15 to 6; nHOLD is activated for an instant around t=100, while DECnINC changes, and the count keeps going up from 6 with no jumps, up to 15.
class: verilog-svg
width: 100%
align: center
---
Timing diagram of the up/down counter with a HOLD line.
```
````

## Exercise 2

```{admonition} Statement
:class: note

Check, with Verilog, that this synchronous counter works correctly.
```

```{figure} ../../_static/verilog/sesion_08/svg/contsinc.svg
---
name: fig-verilog-en-08-contsinc
alt: Four-bit synchronous counter with four JK flip-flops with a common clock. In each flip-flop J and K are tied together. Those of the first one are 1; those of the second one receive Q1; those of the third one, the AND of Q1 and Q2, and those of the fourth one, the AND of Q1, Q2 and Q3.
class: verilog-svg
width: 100%
align: center
---
Synchronous counter.
```

## Exercise 3

```{admonition} Statement
:class: note

The task is to analyse the following counter with an arbitrary counting sequence and build its state transition diagram.
```

```{figure} ../../_static/verilog/sesion_08/svg/analisis.svg
---
name: fig-verilog-en-08-analisis
alt: Counter with an arbitrary counting sequence, with three JK flip-flops with a common clock and outputs Q0, Q1 and Q2. The first one has output Q2 negated at J and the XOR of Q1 and Q2 at K. The second one has J at 1 and the AND of Q0 and Q2 negated at K. The third one has output Q0 at J and output Q0 negated at K.
class: verilog-svg
width: 100%
align: center
---
Circuit to analyse.
```

Let us recall the steps to follow:

1. First, write the equations of the Js and Ks of the flip-flops as a function of the output variables $Q_2Q_1Q_0$.
2. With the help of those equations, build a table with all the states and the values of the Js and Ks of the flip-flops for each state.
3. Complete the table with the new state that the state of each row leads to.
4. Draw the state transition diagram from the table.

Check that you have done the exercise correctly by writing the circuit in Verilog.

## Related shell commands

| Command | What it does |
|---|---|
| `ls` | Lists the contents of a directory. |
| `cd` | Changes the working directory. |
| `rm` | Deletes a file. |
| `man` | Shows the manual page of a command. |
| `cat` | Shows the contents of a file. |

## Original source

Content adapted to TeachBook from the reference page <http://avellano.usal.es/~compi/sesion8.htm> (© 2019 Guillermo González Talaván)
