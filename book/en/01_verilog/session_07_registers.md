# Session 7. Registers in Verilog

Seventh lab session. We will describe modules with behavioural models, build a D flip-flop and, with it, several shift registers. We will also see how to dump the signals of a simulation so that they can be studied in a timing diagram with GTKwave.

```{admonition} Learning objectives
:class: tip

- Describe a module with a behavioural model, using conditional `always` blocks and the `case` statement.
- Build a D flip-flop triggered on the falling edge.
- Build SISO, SIPO and parallel-load shift registers.
- Generate a timing diagram of the signals with `$dumpfile` and `$dumpvars` and analyse it with GTKwave.
```

## Behavioural models

```{admonition} Reminder: conditional always block
:class: seealso

As we saw in the {ref}`previous session <verilog-en-06-conditional-always>`, a conditional `always` block runs when certain signals change:

- `always @(C)`: every time `C` changes.
- `always @(CLEAR,PRESET)`: every time `CLEAR` or `PRESET` changes.
- `always @(posedge C)` or `always @(negedge C)`: on every rising or falling edge of `C`.
```

With these blocks we can build modules based on their behaviour. In behavioural models we tell Verilog not how the module is built inside, but how it behaves, that is, how it works: we do not use logic gates, we only care about the behaviour of the module.

Sometimes we do not want to go into that much detail. We would rather describe briefly what we want and let an automatic synthesis tool take care of the low level.

### Example: JK flip-flop

Let us take the JK flip-flop with PRESET and CLEAR from the previous session. How would we write this module based on its behaviour?

```{figure} ../../_static/verilog/sesion_06/svg/jk.svg
---
name: fig-verilog-en-07-jk
alt: JK flip-flop with four NAND gates, inputs J, C and K, active-low PRESET and CLEAR lines and feedback outputs Q and Q negated. On the right, its block symbol.
class: verilog-svg
width: 95%
align: center
---
JK flip-flop with PRESET and CLEAR (left) and its symbol (right).
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

This module describes, with no gates except the NOT for the negated output, a JK flip-flop triggered on the rising edge of the clock, with active-low PRESET and CLEAR lines:

```verilog
module BiestableJK (output reg Q, output wire Qn, input wire J, input wire K,
                    input wire C, input wire PRESET, input wire CLEAR);
  not(Qn,Q);

  initial
    Q=0;

  always @(posedge C)
    case ({J,K})
      2'b10: Q=1;
      2'b01: Q=0;
      2'b11: Q=~Q;
    endcase

  always @(PRESET,CLEAR)
    case ({PRESET,CLEAR})
      2'b01: Q=1;
      2'b10: Q=0;
    endcase
endmodule
```

The first thing we need is something that holds the value of Q, so the output is declared as a register (`output reg`). A NOT gate gives us the value of `Qn`, as before. In the `initial` block, we set the flip-flop to 0.

Next come two blocks that run every time (`always`) a condition is met. The first one, on the rising edge of `C`. The second one, every time `PRESET` or `CLEAR` changes.

The rest of the code is fairly self-explanatory. The concatenation operator (`{}`) builds the two-bit values J,K or PRESET,CLEAR. The `case` statement states what must happen in the cases where something must happen. Its general form is:

```text
case (expression)
  alternative_1: statement_1;
  alternative_2: statement_2;
  ...
  default: default_statement;   // optional
endcase
```

## Exercise 1

```{admonition} Statement
:class: note

Build a D flip-flop with any of the methods we have seen so far or of those seen in the theory lectures.
```

```{figure} ../../_static/verilog/sesion_07/svg/d.svg
---
name: fig-verilog-en-07-d
alt: Symbol of a D flip-flop with data input D, clock input C triggered on the falling edge and output Q
class: verilog-svg
width: 35%
align: center
---
D flip-flop triggered on the falling edge.
```

| Function | C | $Q_{n+1}$ |
|---|:---:|:---:|
| Capture | $\downarrow$ | D |
| Hold | other | $Q_n$ |

`````{admonition} Solutions and comments: with gates
:class: dropdown

We start from the design seen in the theory lectures, which is an active-high level-triggered flip-flop:

```{figure} ../../_static/verilog/sesion_07/svg/dnivel.svg
---
name: fig-verilog-en-07-dnivel
alt: Active-high level-triggered D flip-flop with two AND gates, a NOT gate and an OR gate with feedback. C goes straight to the AND gate of D and, negated, to the AND gate of the Q feedback.
class: verilog-svg
width: 60%
align: center
---
Active-high level-triggered D flip-flop.
```

To turn it into a flip-flop triggered on the rising edge of the clock, we use an adapter like the one seen in the previous session:

```{figure} ../../_static/verilog/sesion_06/svg/det.svg
---
name: fig-verilog-en-07-det
alt: Rising-edge detector. Signal C goes through a NOT gate with a delay of one unit, giving Cnr, and through an AND gate together with C itself, giving DET. The timing diagram shows that DET has a short pulse right after each rising edge of C.
class: verilog-svg
width: 95%
align: center
---
Rising-edge adapter (left) and its timing diagram (right).
```

But the statement asks us to build a flip-flop triggered on the *falling edge* of the clock. There are many ways to get it. The simplest one is to just add a NOT gate at the clock input, so the edges are inverted and we are done.

However, we are going to slightly modify the designs to reach the same goal. First, we slightly modify the original flip-flop design so that it is active low. It is easy to see that, by moving the NOT gate of the first design, the flip-flop feeds back its contents when C is high and lets the data through when C is low. Just what we want:

```{figure} ../../_static/verilog/sesion_07/svg/dbajo.svg
---
name: fig-verilog-en-07-dbajo
alt: Active-low level-triggered D flip-flop. The NOT gate is now on the branch of C that goes to the AND gate of D, and C goes straight to the AND gate of the Q feedback.
class: verilog-svg
width: 60%
align: center
---
Active-low level-triggered D flip-flop.
```

Now, to turn the active-low flip-flop into one triggered on the falling edge, we just replace the AND gate of the previous adapter with an OR gate:

```{figure} ../../_static/verilog/sesion_07/svg/det_or.svg
---
name: fig-verilog-en-07-det-or
alt: Adapter with an OR gate. Signal C and its delayed negation Cnr go into an OR gate that gives DET. The timing diagram shows that DET is 1 except for a short pulse at 0 right after each falling edge of C.
class: verilog-svg
width: 95%
align: center
---
Falling-edge adapter (left) and its timing diagram (right).
```

Let us start building the active-low flip-flop:

```{figure} ../../_static/verilog/sesion_07/svg/dbajo_nombres.svg
---
name: fig-verilog-en-07-dbajo-nombres
alt: Active-low level-triggered D flip-flop with the names of its gates, n, a1, a2 and o, and of its wires, wn, wa1 and wa2
class: verilog-svg
width: 60%
align: center
---
Active-low level-triggered D flip-flop with gate and wire names.
```

With all of the above, we can build the modules `Ddown` (active-low level-triggered D flip-flop), `Detector` (falling-edge detector for an active-low circuit), `Ddownedge` (D flip-flop triggered on the falling edge, that is, the level-triggered one with the edge detector in front of its clock input) and `TestDdownedge` (test module):

```{figure} ../../_static/verilog/sesion_07/svg/ddownedge.svg
---
name: fig-verilog-en-07-ddownedge
alt: D flip-flop triggered on the falling edge. On the left, the adapter with an OR gate; its output goes to the clock input of the active-low level-triggered D flip-flop on the right.
class: verilog-svg
width: 85%
align: center
---
Resulting circuit: adapter and active-low level-triggered flip-flop.
```

```verilog
module Ddown(output wire Q, input wire D, input wire C);
  wire wa1, wa2;

  not n(wn,C);
  and a1(wa1,D,wn);
  and a2(wa2,C,Q);
  or  o(Q,wa1,wa2);
endmodule

module Detector(output wire DET, input wire C);
  wire Cnr;
  not #(1) n(Cnr,C);
  or o(DET,C,Cnr);
endmodule

module Ddownedge(output wire Q, input wire D, input wire C);
  wire wConector;
  Ddown dd(Q,D,wConector);
  Detector det(wConector,C);
endmodule

module TestDdownedge;
  reg rD,rC;
  wire wQ;

  Ddownedge dde(wQ,rD,rC);

  always #7 rC= ~rC;

  initial
  begin
    $monitor($time," C:%b DET:%b D:%b Q:%b",rC,dde.wConector,rD,wQ);
    rC=0; rD=0;
    #5 rD=1;
    #5 rD=1;
    #5 rD=0;
    #5 rD=1;
    #5 rD=0;
    #5 rD=0;
    #5 rD=0;
    #5 rD=1;
    #5 rD=1;
    #5 rD=0;
    #5 rD=1;
    #5 rD=0;
    #5 rD=1;
    #5 rD=1;
    #5 rD=0;
    #5 rD=1;
    $finish;
  end
endmodule
```

The output gives *almost* the expected result: a D flip-flop that reacts to its input only when the clock falls:

```text
 0 C:0 DET:x D:0 Q:x
 1 C:0 DET:1 D:0 Q:x
 5 C:0 DET:1 D:1 Q:x
 7 C:1 DET:1 D:1 Q:x
14 C:0 DET:0 D:1 Q:1
15 C:0 DET:1 D:0 Q:0
20 C:0 DET:1 D:1 Q:0
21 C:1 DET:1 D:1 Q:0
25 C:1 DET:1 D:0 Q:0
28 C:0 DET:0 D:0 Q:0
29 C:0 DET:1 D:0 Q:0
35 C:1 DET:1 D:0 Q:0
40 C:1 DET:1 D:1 Q:0
42 C:0 DET:0 D:1 Q:1
43 C:0 DET:1 D:1 Q:1
49 C:1 DET:1 D:1 Q:1
50 C:1 DET:1 D:0 Q:1
55 C:1 DET:1 D:1 Q:1
56 C:0 DET:0 D:1 Q:1
57 C:0 DET:1 D:1 Q:1
60 C:0 DET:1 D:0 Q:1
63 C:1 DET:1 D:0 Q:1
65 C:1 DET:1 D:1 Q:1
70 C:0 DET:0 D:1 Q:1
71 C:0 DET:1 D:1 Q:1
75 C:0 DET:1 D:0 Q:1
77 C:1 DET:1 D:0 Q:1
80 C:1 DET:1 D:1 Q:1
```

The exception seems to be in lines t=14 and t=15:

```text
[...]
 7 C:1 DET:1 D:1 Q:x
14 C:0 DET:0 D:1 Q:1
15 C:0 DET:1 D:0 Q:0
[...]
```

On the falling edge of the clock at t=14, input D is correctly captured at output Q but, and this is the unexpected part, at t=15 input D is captured again in an unwanted way. This strange behaviour happens because two simultaneous signal changes meet at t=15: D changes from 1 to 0 and DET changes from 0 to 1. Verilog considers the change of D first, so its zero is captured by the flip-flop when DET changes next. In a real circuit, these changes would not meet.

We can tell Verilog that both signals change at the same time if, instead of the assignment operator `=`, we use the non-blocking assignment operator `<=`, seen in the previous session, both for the clock and for the data signal:

```verilog
[...]
  always #7 rC<= ~rC;

  initial
  begin
    $monitor($time," C:%b DET:%b D:%b Q:%b",rC,dde.wConector,rD,wQ);
    rC<=0; rD<=0;
    #5 rD<=1;
    #5 rD<=1;
    #5 rD<=0;
    #5 rD<=1;
    #5 rD<=0;
    #5 rD<=0;
    #5 rD<=0;
    #5 rD<=1;
    #5 rD<=1;
    #5 rD<=0;
    #5 rD<=1;
    #5 rD<=0;
    #5 rD<=1;
    #5 rD<=1;
    #5 rD<=0;
    #5 rD<=1;
    $finish;
  end
[...]
```

With this change, the result is the expected one:

```text
 0 C:0 DET:x D:0 Q:x
 1 C:0 DET:1 D:0 Q:x
 5 C:0 DET:1 D:1 Q:x
 7 C:1 DET:1 D:1 Q:x
14 C:0 DET:0 D:1 Q:1
15 C:0 DET:1 D:0 Q:1
20 C:0 DET:1 D:1 Q:1
21 C:1 DET:1 D:1 Q:1
25 C:1 DET:1 D:0 Q:1
28 C:0 DET:0 D:0 Q:0
29 C:0 DET:1 D:0 Q:0
35 C:1 DET:1 D:0 Q:0
40 C:1 DET:1 D:1 Q:0
42 C:0 DET:0 D:1 Q:1
43 C:0 DET:1 D:1 Q:1
49 C:1 DET:1 D:1 Q:1
50 C:1 DET:1 D:0 Q:1
55 C:1 DET:1 D:1 Q:1
56 C:0 DET:0 D:1 Q:1
57 C:0 DET:1 D:1 Q:1
60 C:0 DET:1 D:0 Q:1
63 C:1 DET:1 D:0 Q:1
65 C:1 DET:1 D:1 Q:1
70 C:0 DET:0 D:1 Q:1
71 C:0 DET:1 D:1 Q:1
75 C:0 DET:1 D:0 Q:1
77 C:1 DET:1 D:0 Q:1
80 C:1 DET:1 D:1 Q:1
```
`````

````{admonition} Solutions and comments: with a behavioural model
:class: dropdown

In behavioural models we tell Verilog not how the module is built inside, but how it behaves, that is, how it works.

In a sense, it is easier and less error-prone than the previous method. If we replace the definition of the previous module with this one, we should get the same result more easily:

```verilog
module Ddownedge(output reg Q, input wire D, input wire C);
  always @(negedge C)
  begin
   Q = D;
  end

  initial
  begin
    Q = 0;
  end
endmodule
```

And in the corresponding output, we see how the flip-flop responds only on the falling edges of the clock:

```text
 0 C:0 D:0 Q:0
 5 C:0 D:1 Q:0
 7 C:1 D:1 Q:0
14 C:0 D:1 Q:1
15 C:0 D:0 Q:1
20 C:0 D:1 Q:1
21 C:1 D:1 Q:1
25 C:1 D:0 Q:1
28 C:0 D:0 Q:0
35 C:1 D:0 Q:0
40 C:1 D:1 Q:0
42 C:0 D:1 Q:1
49 C:1 D:1 Q:1
50 C:1 D:0 Q:1
55 C:1 D:1 Q:1
56 C:0 D:1 Q:1
60 C:0 D:0 Q:1
63 C:1 D:0 Q:1
65 C:1 D:1 Q:1
70 C:0 D:1 Q:1
75 C:0 D:0 Q:1
77 C:1 D:0 Q:1
80 C:1 D:1 Q:1
```

In this case, not only is the Verilog code simpler than in the previous case, but we also do not run into the problem of signal changes meeting.
````

## Exercise 2

```{admonition} Statement
:class: note

With the module built in the previous exercise, build a SISO register.
```

```{figure} ../../_static/verilog/sesion_07/svg/siso.svg
---
name: fig-verilog-en-07-siso
alt: Four-bit SISO register. Four chained D flip-flops, with the Q output of each one connected to the D input of the next one, serial input I, serial output O, common clock C triggered on the falling edge and common active-low CLR line.
class: verilog-svg
width: 95%
align: center
---
Four-bit SISO register.
```

Clear the contents of the flip-flops with CLR. Apply a clock signal and some random inputs and check that the output is the expected one.

````{admonition} Solutions and comments: first solution
:class: dropdown

We are going to solve the problem using the D module built in the previous exercise. Using four of those modules and naming them and the unnamed wires, the problem looks like this:

```{figure} ../../_static/verilog/sesion_07/svg/siso_nombres.svg
---
name: fig-verilog-en-07-siso-nombres
alt: Four-bit SISO register with the flip-flops named B1, B2, B3 and B4 and the inner wires named C1, C2 and C3
class: verilog-svg
width: 95%
align: center
---
Four-bit SISO register with flip-flop and wire names.
```

The result can be:

```verilog
module D(output reg Q, input wire D, input wire C, input wire nCLR);
  always@(negedge C)
  begin
    if (nCLR == 1)
    begin
     Q = D;
    end
  end

  always @(nCLR)
  begin
    if (nCLR == 0)
    begin
      Q = 0;
    end
  end

  initial
  begin
    Q = 0;
  end
endmodule

module SISO (output wire O, input wire I, input wire C, input wire nCLR);
  wire C1;
  wire C2;
  wire C3;
  D B1 (C1, I, C, nCLR);
  D B2 (C2, C1, C, nCLR);
  D B3 (C3, C2, C, nCLR);
  D B4 (O, C3, C, nCLR);
endmodule
```

We test the SISO module with registers and a wire inside a test module with no inputs or outputs, as in this diagram:

```{figure} ../../_static/verilog/sesion_07/svg/siso_prueba.svg
---
name: fig-verilog-en-07-siso-prueba
alt: Test module for the SISO register. Registers lorena, angelica and pato are connected to inputs I, C and nCLR of the SISO module called hector, and its output O to wire javi.
class: verilog-svg
width: 75%
align: center
---
Test module for the SISO register.
```

Or, written in Verilog:

```verilog
module probador;
  reg lorena;
  reg angelica;
  reg pato;
  wire javi;
  SISO hector(javi, lorena, angelica, pato);

  initial
  begin
    $dumpfile("datosSISO.dmp");
    $dumpvars(1,hector);
    $monitor($time, " I=%b, C=%b, O=%b, nCLR=%b",
             lorena, angelica, javi, pato);
    lorena=1; angelica=1; pato=0;
    #5 pato=1;
    #7 lorena=0;
    #7 lorena=1;
    #7 lorena=0;
    #7 lorena=1;
    #7 lorena=1;
    #7 lorena=1;
    #7 lorena=0;
    #7 lorena=0;
    #15 $finish;
  end

  always
  begin
    #7 angelica=~angelica;
  end
endmodule
```

As you can see, we have added an `always` block that generates the clock signal, with a period of 14 time units, in register `angelica`.

The code needed to dump the inner variables of the main SISO module `hector`, explained in the next section, is also included. The dump goes to the file `datosSISO.dmp`, so that the signals can be viewed with GTKwave. We compile with `iverilog`, for example:

```text
$ iverilog siso.v -o siso
$ ./siso
VCD info: dumpfile datosSISO.dmp opened for output.
 0 I=1, C=1, O=0, nCLR=0
 5 I=1, C=1, O=0, nCLR=1
 7 I=1, C=0, O=0, nCLR=1
12 I=0, C=0, O=0, nCLR=1
14 I=0, C=1, O=0, nCLR=1
19 I=1, C=1, O=0, nCLR=1
21 I=1, C=0, O=1, nCLR=1
26 I=0, C=0, O=1, nCLR=1
28 I=0, C=1, O=1, nCLR=1
33 I=1, C=1, O=1, nCLR=1
35 I=1, C=0, O=1, nCLR=1
42 I=1, C=1, O=1, nCLR=1
49 I=1, C=0, O=1, nCLR=1
54 I=0, C=0, O=1, nCLR=1
56 I=0, C=1, O=1, nCLR=1
63 I=0, C=0, O=1, nCLR=1
70 I=0, C=1, O=1, nCLR=1
$ ls -l datosSISO.dmp
-rw-r--r-- 1 gyermo gyermo 507 2010-12-02 01:09 datosSISO.dmp
$ gtkwave datosSISO.dmp &
```

The timing diagram we get is somewhat disappointing. We would expect that, on every falling edge of the clock, the signal travels from `I`, through `C1`, `C2`, `C3` and up to `O`. However, it seems to propagate all at once through `C3` and `O`:

```{figure} ../../_static/verilog/sesion_07/svg/sol_siso_1.svg
---
name: fig-verilog-en-07-sol-siso-1
alt: Wrong timing diagram of the SISO register. C1 rises on the first falling edge of the clock, but C2, C3 and O all rise at the same time on the second falling edge, at t=21.
class: verilog-svg
width: 100%
align: center
---
Wrong timing diagram: the signal propagates all at once.
```

And the most curious thing is that, if we compile the program with `cver`, it works fine. Who can make sense of this?
````

````{admonition} Solutions and comments: the mystery solved
:class: dropdown

The explanation is simpler than it seems. The problem is that we have modelled flip-flops that are not realistic. Real flip-flops take *some* time, however small, to propagate the signal. In Iverilog, because propagation is instant, when flip-flop `B3` is about to capture the signal on wire `C2`, flip-flop `B2` has already changed it to the new value. In Cver, this does not happen. It always captures the old signal, never the new one.

The simplest fix is to model the flip-flops with some delay. For example, one time unit between capturing the signal and making it available at output Q of the flip-flop. We change the reaction to the falling edge of the clock so that it reads:

```verilog
  always@(negedge C)
  begin
    if (nCLR == 1)
    begin
     Q = #1 D;
    end
  end
```

Note that this is not the same as writing:

```verilog
     #1 Q = D;
```

In the first case, the signal is captured and, one time unit later, assigned to Q. In the second one, the simulation first waits one time unit and then captures the signal and transfers it to Q at once.

Now the timing diagram of the run does give something reasonable:

```{figure} ../../_static/verilog/sesion_07/svg/sol_siso_2.svg
---
name: fig-verilog-en-07-sol-siso-2
alt: Timing diagram of the SISO register with delay in the flip-flops. C1 rises at t=8, C2 at t=22, C3 at t=36 and O at t=50, one time unit after each falling edge of the clock.
class: verilog-svg
width: 100%
align: center
---
Timing diagram with delay in the flip-flops: the signal moves one flip-flop forward on each falling edge of the clock.
```

If you look closely, you will also notice the delay of that one time unit we introduced between the fall of the clock and the propagation of the signal at the output of the flip-flops.
````

````{admonition} Solutions and comments: solution?
:class: dropdown

The previous solution seems **not** to be completely right. If it were a true SISO register, we should see input signal I travel through the register, exactly the same, on every clock cycle. However, if we look at the previous diagram, the signal that appears on C1, C2, C3 and O is not the same as the input signal...

Actually, the program works perfectly. What happens is that signal I changes very fast in the example and, every time the clock signal falls, not all the changes of I can be seen. I changes every 7 time units, while the clock falls every 14, because the clock changes value every 7.

If we want to see the signal propagate, we must make it change every 14 time units. We do so by replacing every `#7` with `#14` in our `probador` module:

```verilog
module probador;
  reg lorena;
  reg angelica;
  reg pato;
  wire javi;
  SISO hector(javi, lorena, angelica, pato);

  initial
  begin
    $dumpfile("datosSISO.dmp");
    $dumpvars(1,hector);
    $monitor($time, " I=%b, C=%b, O=%b, nCLR=%b",
             lorena, angelica, javi, pato);
    lorena=1; angelica=1; pato=0;
    #12 pato=1;
    #14 lorena=0;
    #14 lorena=1;
    #14 lorena=0;
    #14 lorena=1;
    #14 lorena=1;
    #14 lorena=1;
    #14 lorena=0;
    #14 lorena=0;
    #15 $finish;
  end

  always
  begin
    #7 angelica=~angelica;
  end
endmodule
```

At last we get an output that is, touch wood, perfect:

```{figure} ../../_static/verilog/sesion_07/svg/sol_siso_3.svg
---
name: fig-verilog-en-07-sol-siso-3
alt: Correct timing diagram of the SISO register. The shape of input signal I is repeated on C1, C2, C3 and O, delayed one clock cycle at each flip-flop.
class: verilog-svg
width: 100%
align: center
---
Correct timing diagram: the input signal travels through the register.
```
````

## Signal debugging in Verilog

A timing diagram of the signals of a Verilog design can be generated. To do so, we use the commands described in this section. The first one sets the output file. It must be placed at the start of the program, at the beginning of the `initial` block:

```verilog
$dumpfile("file_name.dmp");
```

We must also state which signals we want to follow:

```verilog
$dumpvars(depth,object_name);
```

This is also done at the start of the simulation. The object name is the name of the module or variable to follow. If it is a module, a depth greater than 1 tells how many levels of the object hierarchy to go into. If the SISO register of the previous exercise is called `pepe` and we want to follow all its signals but not those of the objects it contains, the command would be:

```verilog
$dumpvars(1,pepe);
```

All that is left is to start or stop the dump at will. The dump starts right after `$dumpvars`. Every time we want to stop it, we write the command `$dumpoff;`, and every time we want to resume it, we write `$dumpon;`.

| Command | What it does |
|---|---|
| `$dumpfile("file.dmp");` | Names the dump file. |
| `$dumpvars(depth,name);` | Chooses the signals to dump and starts the dump. |
| `$dumpoff;` | Stops the dump. |
| `$dumpon;` | Resumes the dump. |

The output dumped into the file is not meant for humans. It must be analysed with a graphical program. One of them, available for Linux, is called GTKwave. Let us look at the output produced for the previous example:

```{figure} ../../_static/verilog/sesion_07/svg/cronograma_siso.svg
---
name: fig-verilog-en-07-gtkwave
alt: GTKwave timing diagram with signals C, nCLEAR, I, w01, w12, w23 and O of the SISO register. After nCLEAR goes high, the changes of input I appear one after another on the inner wires w01, w12 and w23 and finally at output O.
class: verilog-svg
width: 100%
align: center
---
GTKwave output for the SISO register of the previous exercise.
```

To get this output, we run the program from the command line with `gtkwave dump_file_name`. For this to work, the program must be installed on your Linux system. Once inside, you can examine the signals by browsing the upper-left window. To make the signals appear in the timing diagram, drag them from the lower-left window to the long window right next to it.

## Exercise 3

```{admonition} Statement
:class: note

Slightly modify the code of the previous exercise to get the following SIPO register. Test it. For the O wires, use a single four-bit variable instead of four one-bit variables.
```

```{figure} ../../_static/verilog/sesion_07/svg/sipo.svg
---
name: fig-verilog-en-07-sipo
alt: Four-bit SIPO register. An AND gate combines inputs E and I and feeds the chain of four D flip-flops; the flip-flop outputs are the parallel outputs O3, O2, O1 and O0. Common clock C triggered on the falling edge and common active-low CLR line.
class: verilog-svg
width: 95%
align: center
---
Four-bit SIPO register.
```

## Exercise 4

```{admonition} Statement
:class: note

Build and test the following four-bit register. Can you design it in a modular way? Load a value through the parallel input and shift it towards the serial output.
```

```{figure} ../../_static/verilog/sesion_07/svg/pisiso.svg
---
name: fig-verilog-en-07-pisiso
alt: Four-bit register with serial input I, parallel inputs I3 to I0 and serial output O. In each stage, the negated S/P line chooses, through two AND gates and a NOR gate, between the serial input and the parallel input; the result reaches the R and S inputs of an RS flip-flop. The flip-flop clock is C AND CE, and the negated CLR line is common.
class: verilog-svg
width: 100%
align: center
---
Four-bit register with serial input, parallel input and serial output.
```

````{admonition} Hint: how to split it into modules
:class: dropdown

We can split the design into modules:

1. A serial/parallel selector module. Depending on the S/$\overline{\text{P}}$ line, it chooses between parallel input $I_p$ and serial input $I_s$, and gives the output and its negation for the inputs of the RS flip-flop:

   ```{figure} ../../_static/verilog/sesion_07/svg/selector.svg
   ---
   name: fig-verilog-en-07-selector
   alt: Serial/parallel selector module. One AND gate combines Ip with the inverted select line and another combines the select line with Is; a NOR gate joins both and gives Q, and a NOT gate gives Q negated.
   class: verilog-svg
   width: 60%
   align: center
   ---
   Serial/parallel selector module.
   ```

2. An RS flip-flop. You can start from the one of the previous session and add a falling-edge clock, as in exercise 1, and the nCLR signal. Alternatively, you can write an RS module that models its behaviour.
````

## Related shell commands

| Command | What it does |
|---|---|
| `ls` | Lists the contents of a directory. |
| `cd` | Changes the working directory. |
| `rm` | Deletes a file. |
| `man` | Shows the manual page of a command. |
| `cat` | Shows the contents of a file. |

## Original source

Content adapted to TeachBook from the reference page <http://avellano.usal.es/~compi/sesion7.htm> (© 2010 Guillermo González Talaván)
