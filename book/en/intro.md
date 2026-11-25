# Computers I

Welcome to the **Computers I** practice book.

This material supports the study of digital design fundamentals using **Verilog** as a hardware description language. The course starts from a simple idea: a computer is not a magic box, but an ordered composition of signals, logic gates, modules, registers, counters, and arithmetic-logic units.

## What you will learn

By working through this book, you will learn to:

- describe digital circuits with Verilog modules;
- simulate the behavior of logic gates, buses, flip-flops, registers, and counters;
- interpret signals, states, and propagation delays;
- build combinational and sequential components step by step;
- connect each exercise with the reference diagrams and tables for the session.

## How the course is organized

The course is organized into practice sessions. Each session includes the Verilog explanations you need, the exercise statements and the reference diagrams and tables, to keep the circuit being programmed clearly in view.

```{admonition} Recommended workflow
:class: tip

Before writing code, identify the circuit inputs, outputs, and internal signals. Then consult the reference figures, write the Verilog module, and check the simulation. If the result does not match what you expected, return to the figure and review the connections.
```

## Session index

| Session | What it covers |
|---|---|
| [Session 0. Ubuntu Terminal for Verilog](01_verilog/session_00_ubuntu_terminal.md) | Folders, files, basic editors, and first contact with `iverilog`. |
| [Session 1. Introduction to Verilog](01_verilog/session_01_introduction.md) | Working environment, basic modules, and screen output. |
| [Session 2. Bit operations](01_verilog/session_02_operations.md) | Masks, parity, and bit reduction. |
| [Session 3. Logic Gates in Verilog](01_verilog/session_03_logic_gates.md) | AND, OR, NOT, NAND, NOR, XOR, XNOR, and combinational functions. |
| [Session 4. Modules in Verilog](01_verilog/session_04_modules.md) | Interfaces, module hierarchy, and comparators. |
| [Session 5. Routers and adders in Verilog](01_verilog/session_05_routers_and_adders.md) | Tri-state buffers, multiplexers, adders, and gate delays. |
| [Session 6. Flip-flops in Verilog](01_verilog/session_06_flip_flops.md) | RS and JK flip-flops, clock signal, edges, and `always` blocks. |
| [Session 7. Registers in Verilog](01_verilog/session_07_registers.md) | Behavioural models, shift registers, and timing diagrams with GTKwave. |
| [Session 8. Counters in Verilog](01_verilog/session_08_counters.md) | Up/down counters, synchronous counter, and state transitions. |
| [Session 9. ALU in Verilog](01_verilog/session_09_alu.md) | File inclusion and use of the 74181 ALU. |

The sessions are meant to be followed in order: each one reuses what was built in the previous ones. You can also switch to the Spanish book from the language selector in the top bar.

## Reference source

Practically all the sessions in this book are based on the lab sessions of the web page of the **Computers I** course at the University of Salamanca, written by Guillermo González Talaván:

<http://avellano.usal.es/~compi/>

At the end of sessions 1 to 9 there is a link to the original page their content comes from.
