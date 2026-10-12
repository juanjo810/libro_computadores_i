# Session 4. Modules in Verilog

Fourth lab session. We will learn to split a design into modules with well-defined interfaces, to instantiate them inside other modules and to refer to their elements through the hierarchy.

```{admonition} Learning objectives
:class: tip

- Know the features of modular design and the Verilog port types (`input`, `output`, `inout`).
- Declare a module interface and describe its inside with gates and auxiliary wires.
- Instantiate a module inside another one and check it with a test module.
- Navigate the module hierarchy with the dot operator (`.`).
- Leave ports unconnected and use gates with more than two inputs.
```

## Modules

Modular design is widely used in computer science, and hardware design is no exception. It consists of dividing the problem into simpler units called **modules**. Modules should have the following features:

- They must be **self-contained**: from inside a module, the inside of another module cannot be accessed.
- Communication with the outside of a module, or with other modules, must happen through **well-defined interfaces**.
- It is convenient to be able to **nest** modules (build modules inside other modules).

Modular design has many advantages:

- It makes it easier to build complex systems from simpler ones.
- When something fails, it is much easier to locate the fault and debug the design.

In Verilog, modules are electronic modules, and the interfaces with the outside or with other modules are **ports**. There are three kinds of ports:

| Port | Keyword | Information flow | Arrow |
|---|---|---|---|
| Input | `input` | Flows into the module. | Points into the module. |
| Output | `output` | Leaves the module. | Points outwards. |
| Input/output | `inout` | A combination of the two above. | Has a head at both ends. |

Verilog connection rules depend on the port type. The figure below shows the allowed connections for the three port types and the two relevant variable types (`reg` and `wire`):

```{figure} ../../_static/verilog/sesion_04/svg/modulo.svg
---
name: fig-verilog-en-04-modulo
alt: Port connection rules. An input connects to reg or wire outside and to wire inside; an output connects to reg or wire inside and to wire outside; an inout is wire both outside and inside.
class: verilog-svg
width: 85%
align: center
---
Connection rules for module ports.
```

The gates we have already seen can be regarded as small modules predefined by the language.

## Comparator module

The first module we will define and build is the one-bit comparator seen in the theory lectures:

| a | b | a > b | a = b | a < b |
|:---:|:---:|:---:|:---:|:---:|
| 0 | 0 | 0 | 1 | 0 |
| 0 | 1 | 0 | 0 | 1 |
| 1 | 0 | 1 | 0 | 0 |
| 1 | 1 | 0 | 1 | 0 |

```{figure} ../../_static/verilog/sesion_04/svg/comp1.svg
---
name: fig-verilog-en-04-comp1
alt: One-bit comparator with two inverters, two AND gates and a NOR gate
class: verilog-svg
width: 80%
align: center
---
One-bit comparator.
```

As you can see, this module has two inputs, which we will call `a` and `b`, both one bit wide, and three outputs, which we will call `mayor` (greater), `igual` (equal) and `menor` (less), also one bit wide each.

When defining a module in Verilog, the first step is to declare its **interface**:

```verilog
// One-bit comparator module
module Comp1(output wire mayor, output wire igual, output wire menor,
             input wire a, input wire b);
  // The module code goes here
endmodule
```

In the module body we must connect the gates. To do so, we name each of them and, if needed, some auxiliary wires. For example:

```{figure} ../../_static/verilog/sesion_04/svg/comp1_nombres.svg
---
name: fig-verilog-en-04-comp1-nombres
alt: One-bit comparator with the gate and wire names used in Verilog
class: verilog-svg
width: 80%
align: center
---
The comparator with the gate names (`nArriba`, `nAbajo`, `aArriba`, `aAbajo`, `n`) and the auxiliary wires (`wArriba`, `wAbajo`).
```

```verilog
// One-bit comparator module
module Comp1(output wire mayor, output wire igual, output wire menor,
             input wire a, input wire b);

  wire wArriba, wAbajo;

  not nArriba(wArriba,a);
  not nAbajo(wAbajo,b);
  and aArriba(mayor,a,wAbajo);
  and aAbajo(menor,b,wArriba);
  nor n(igual,mayor,menor);

endmodule
```

To check that the result is correct, we define an auxiliary module in the same file:

```verilog
module TestComp1;

  reg a,b;
  wire M,m,igual;

  Comp1 c(M,igual,m,a,b);

  // Behavioural block
  initial
    begin
      $monitor($time," a=%b, b=%b, mayor=%b, igual=%b, menor=%b",
                     a,b,M,igual,m);
      a=0; b=0;
      #5 a=0; b=1;
      #5 a=1; b=0;
      #5 a=1; b=1;
    end

endmodule
```

The key line is `Comp1 c(M,igual,m,a,b)`. Earlier we defined the interface and behaviour of the module. In this line we build an **instance** of the module named `c`. A definition can be instantiated as many times as needed.

```{admonition} Connections follow the interface order
:class: important

When instantiating `Comp1 c(M,igual,m,a,b);`, each variable is connected to the port in the same position in the module declaration:

| Position | `Comp1` port | `TestComp1` variable |
|:---:|---|---|
| 1 | `output mayor` | `M` |
| 2 | `output igual` | `igual` |
| 3 | `output menor` | `m` |
| 4 | `input a` | `a` |
| 5 | `input b` | `b` |

Names do not need to match: what matters is the order.
```

The program output is:

```text
                   0 a=0, b=0, mayor=0, igual=1, menor=0
                   5 a=0, b=1, mayor=0, igual=0, menor=1
                  10 a=1, b=0, mayor=1, igual=0, menor=0
                  15 a=1, b=1, mayor=0, igual=1, menor=0
```

If you save both modules in a file called `TestComp1.v`, compile and run it as usual:

```bash
iverilog -o TestComp1 TestComp1.v
./TestComp1
```

## Module hierarchy. Naming

Instantiating modules inside other modules creates a **module hierarchy**. For the one-bit comparator above, the hierarchy looks like this:

```{figure} ../../_static/verilog/sesion_04/svg/jerarquia.svg
---
name: fig-verilog-en-04-jerarquia
alt: Hierarchy tree of TestComp1. The root module contains instance c of Comp1, registers a and b and wires M, m and igual. Instance c contains gates nArriba, nAbajo, aArriba, aAbajo and n and wires wArriba and wAbajo.
class: verilog-svg
width: 90%
align: center
---
Module hierarchy of `TestComp1`. Highlighted: the path to gate `aAbajo` inside module `c`.
```

The root module has no name and is instantiated automatically by Verilog. To refer to an object that belongs directly to the root module from the root module itself, simply write the object's name, as we have done so far.

But what if, from the root module, we want to access gate `aAbajo` of module `c`? We use a **dot** (`.`) to go down the object hierarchy. So, to access that gate, we would write `c.aAbajo`. The scheme extends naturally when there are more levels.

## Exercise 1

```{admonition} Statement
:class: note

Instantiate the previous module twice to build a two-bit comparator, following the diagram in the figure.

Build a module to test all possible inputs (16). Use two two-bit variables as inputs instead of four one-bit variables, that is, all combinations where `a` is in {0,1,2,3} and `b` is also in {0,1,2,3}.
```

```{figure} ../../_static/verilog/sesion_04/svg/comp2.svg
---
name: fig-verilog-en-04-comp2
alt: Two-bit comparator made of two one-bit comparators, COMP1 with a0 and b0 and COMP2 with a1 and b1, and AND and OR gates that combine their outputs into a>b, a=b and a<b
class: verilog-svg
width: 90%
align: center
---
Two-bit comparator built from two one-bit comparators.
```

## Unconnected ports

When instantiating a module, we have seen that its ports are connected by listing the variables, in order, between parentheses. If, for whatever reason, we want to leave a port unconnected, we simply leave its place empty. For example, to use a `Comp1` comparator defined above only for equality, the instantiation line could be:

```verilog
Comp1 c7(,igual,,a,b);
```

In this example we assume that three variables `igual`, `a` and `b` are already defined; they are where we want to make the connections.

## Exercise 2

```{admonition} Statement
:class: note

Write three modules in a single Verilog file: one for a normal 4x2 encoder like the one on the left of the figure, another one for a 4x2 priority encoder like the one on the right, and a test module that shows their outputs for each of the 16 possible inputs. Compare the results.
```

```{figure} ../../_static/verilog/sesion_04/svg/codificadores.svg
---
name: fig-verilog-en-04-codificadores
alt: On the left, a 4x2 encoder with two NOR gates; on the right, a 4x2 priority encoder with an inverter, an AND gate and two OR gates
class: verilog-svg
width: 95%
align: center
---
4x2 encoder (left) and 4x2 priority encoder (right).
```

## Gates with more than two inputs

Verilog allows logic gates with more than two inputs. For example, a four-input AND gate:

```{figure} ../../_static/verilog/sesion_04/svg/and4.svg
---
name: fig-verilog-en-04-and4
alt: Four-input AND gate, equivalent to a tree of three two-input AND gates
class: verilog-svg
width: 85%
align: center
---
Four-input AND gate and its equivalent with two-input gates.
```

The gate on the left is ideally equivalent to the set of gates on the right. In Verilog, to instantiate gates with more than two inputs, simply add arguments to the instantiation line:

```verilog
and a4(salida, entrada1, entrada2, entrada3, entrada4);
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

Content adapted to TeachBook from the reference page: <http://avellano.usal.es/~compi/sesion4.htm> (© 2010 Guillermo González Talaván).
