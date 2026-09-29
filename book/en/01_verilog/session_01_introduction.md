# Session 1. Introduction to Verilog

In session 0 we learned to move around the terminal. Now we start writing Verilog: we will create our first program, compile it, run it, and use `$display` to see on screen what happens inside the registers.

```{admonition} Learning objectives
:class: tip

- Understand what Verilog is and what a hardware description language is for.
- Create, compile, and run a `.v` file with `iverilog`.
- Write comments, character strings, and numeric constants in different bases.
- Declare registers (`reg`) of one or several bits, signed and unsigned.
- Print values with `$display` using the right format codes.
- Apply arithmetic operators, tell `reg` from `wire`, and recognise the `x` and `z` values.
```

## What Verilog is

Verilog is a **hardware description language** (*HDL*). It was created in 1983 and is standardised by the IEEE.

The difference from an ordinary programming language matters: when we write in C we give orders to a processor that already exists; when we write in Verilog we **describe a circuit**. From that description, synthesis tools can automatically generate the logic gates and their interconnections.

With the arrival of VLSI technology (*Very Large Scale Integration*), with more than 100,000 transistors on a single chip, designing by hand stopped being viable. That is why these tools became an industry standard.

```{admonition} Verilog looks a lot like C
:class: note

Verilog syntax is almost identical to C: same comments, same arithmetic operators, same format codes. Everything you learn here will help you in the Programming courses, and the other way around.
```

Besides synthesising circuits, an HDL lets us **simulate and debug** them. In these first sessions we will use Verilog almost as if it were a programming language: we will simulate small programs to understand how data is represented and manipulated inside a computer.

## Preparing the working environment

The labs run on GNU/Linux. We will use **Icarus Verilog** (`iverilog`), a free Verilog implementation.

Check that it is installed:

```bash
iverilog -V
```

If it answers with a version number, you already have it. If it answers `command not found`, install it:

```bash
sudo apt update
sudo apt install iverilog
```

```{admonition} Working at home
:class: tip

Everything is already installed on the lab computers. To work at home, install a Debian-based Linux distribution (Debian itself, Ubuntu, or Kubuntu) and run the commands above. There is also `gplcver`, another free implementation; it is used as `cver file.v` and needs no previous compilation.
```

You also need a plain text editor. Any will do: `gedit`, `kate`, `nano`, `vi`, and so on. The examples use `gedit`.

Create a folder for this session and enter it:

```bash
mkdir -p ~/verilog/session_01
cd ~/verilog/session_01
```

## First program: `hello.v`

Although the purpose of Verilog is to design hardware, it is a tradition that the first program in any language prints the words *Hello world* on screen.

Open the editor:

```bash
gedit hello.v
```

And write:

```verilog
/* Example program: hello.v */

module hello;

  initial
    // We print the message and a newline
    $display("Hello, world\n");

endmodule
```

Save it and check that the file exists:

```bash
ls -l
```

A line like this should appear:

```text
-rw-r--r-- 1 student student 151 sep 18 20:50 hello.v
```

Now **compile** the program. The `-o` option gives the name of the executable we want:

```bash
iverilog hello.v -o hello
```

And **run it**:

```bash
./hello
```

The output is:

```text
Hello, world
```

```{admonition} The working cycle for every session
:class: important

This cycle repeats in every lab of the course:

1. Edit the `.v` file with `gedit`.
2. Compile with `iverilog file.v -o simulation`.
3. Run with `./simulation`.
4. Compare the output with what you had predicted.

If compilation reports errors, **do not run**: fix the file first and compile again.
```

## Comments

Comments are written exactly as in C. The simulator ignores them, but for whoever reads the code they are essential.

```verilog
/* This is one kind of comment */

/* This kind of comment can span
   several lines */

// This kind of comment can only span one line
```

## Character strings

Character strings are enclosed in double quotes (`"`). Some characters are written in a special way:

| Sequence | Meaning |
|---|---|
| `\n` | Newline |
| `\t` | Tab |
| `%%` | The `%` character |
| `\\` | The `\` character |
| `\"` | Double quote |
| `\xxx` | Any character, with `xxx` in octal |

The string `"Hello, world\n"` has 14 characters: the 5 of *Hello*, a comma, a space, the 5 of *world*, and one special character that produces the newline (`\n`). Note that `\n` counts as **a single character**, even though we write it with two symbols.

## Numeric constants

Unless stated otherwise, Verilog reads a numeric constant as **decimal**. To use other bases we add a prefix:

| Prefix | Base | Example | Decimal value |
|---|---|---|---|
| `'b` | Binary | `'b1011` | 11 |
| `'o` | Octal | `'o17` | 15 |
| `'d` | Decimal | `'d25` | 25 |
| `'h` | Hexadecimal | `'hD1C` | 3356 |

For a negative number the minus sign goes in front of everything: `-'hD1C`.

**Real** numbers are written with the point as decimal separator, or in scientific notation, for example `7.237e10`. Only base 10 is allowed for reals.

To keep long binary numbers readable, underscores may be inserted. The simulator ignores them:

```verilog
// These two constants are exactly the same value
'b1_1011_1111_1000
'b1101111111000
```

## Numeric data types

For these first programs we will use two variable types meant for simulation, not for describing hardware:

| Type | Holds | Size |
|---|---|---|
| `integer` | A signed integer | The computer word size, at least 32 bits |
| `real` | A floating-point number | Machine dependent |

Later, in the {ref}`registers` section, we will see `reg`, the type that does represent actual bit storage.

## Code blocks: `begin` and `end`

In C, statements such as `for`, `if`, or `while` accept in their body either a single statement or a block of several enclosed in braces (`{` and `}`). In Verilog that same role is played by the reserved words **`begin`** and **`end`**.

That is why in `hello.v` the `initial` block has no `begin` or `end`: it contains a single statement. As soon as there are two or more, they become mandatory:

```verilog
initial
begin
  i = 4;
  f = 2.7172;
  $display("i is %d and f is %g", i, f);
end
```

## The `$display` function

A function takes several arguments (or parameters) and normally returns a value. In programming it can also run statements when called, and it may return nothing at all. Parameters are written in parentheses after the name, separated by commas.

`$display` accepts an arbitrary number of arguments and returns nothing: its job is to **print information on screen**. With no arguments it prints a newline. With arguments, the first one is always a character string.

To print the content of a variable we include a **format code** where we want its value to appear, and we add the variable as an extra argument. The format code also states the base we want to see:

```verilog
integer i;
real f;

initial
begin
  i = 4;
  f = 2.7172;
  $display("i is %d and f is %g", i, f);
end
```

The output is:

```text
i is           4 and f is 2.7172
```

`$display` replaced `%d` with the content of the variable given as second argument (`i`), and `%g` with the one given as third (`f`). Order matters: the first format code matches the first argument after the string.

These are the available format codes. Uppercase is also accepted, with the same meaning:

| Code | Prints |
|---|---|
| `%d` | Integer in decimal |
| `%b` | Integer in binary |
| `%o` | Integer in octal |
| `%h` | Integer in hexadecimal |
| `%c` | Character |
| `%s` | Character string |
| `%f` | Real in decimal format |
| `%e` | Real in scientific format |
| `%g` | Real in the shorter of the two formats above |

```{admonition} The same number, four different faces
:class: tip

A register does not store "a decimal number" or "a hexadecimal number": it stores bits. The base only appears when we print it. Try showing the same value with `%d`, `%b`, `%o`, and `%h` and check that all four outputs describe the same content.
```

## Anatomy of a Verilog program

A complete program using everything so far looks like this:

```{figure} ../../_static/verilog/sesion_01/ej_1_9.png
---
name: fig-verilog-en-01-ej-1-9
alt: Example Verilog program with two variables and one call to $display.
width: 85%
align: center
---
Example program with two variables and one call to `$display`.
```

Let us see which parts it is made of:

```{figure} ../../_static/verilog/sesion_01/ej_1_9_comentado.png
---
name: fig-verilog-en-01-ej-1-9-comentado
alt: The same program with its five zones marked: module name, variable definitions, initial block, statement area, and end of module.
width: 85%
align: center
---
The same program with its five zones marked.
```

**A. Module name and start.** A program may have several modules, and must have at least one. Each module carries a name; in this example it is `ej_1_9`.

**B. Variable definition area.** Variables are the elements able to hold a value. They all have a name that identifies them (`i` and `f` in the example) and a **type**, which states what kind of values they can hold. Here the first is an `integer` and the second a `real`. All module variables are declared in this zone.

**C. `initial` block.** The statements go here, and run one after another. If the block holds a single statement, as in `hello.v`, `begin` and `end` are not needed; in every other case they are, to mark where the block starts and ends.

**D. Statement area.** A statement may span several lines: what marks its end is the **semicolon**, which is mandatory. In the example we give values to `i` and `f` and then print their content with `$display`.

**E. End of module.** It must be closed with `endmodule`. Note that `endmodule` does **not** take a semicolon.

```{admonition} Two rules that save many errors
:class: warning

- The `module` statement, variable declarations, and instructions **must** end in a semicolon (`;`).
- `begin`, `end`, and `endmodule` take no semicolon.
```

## Exercise 1. Base conversions

Answer these questions **by hand first**, then check them with a Verilog program:

1. Express the number `0x1FEA` in decimal.
2. Express the binary number `1000101` in decimal.
3. Express the number `1234` in octal.
4. Convert the binary number `1010011` to hexadecimal.

(registers)=
## Registers

Variables of type `reg` represent **storage units**: they are the closest thing to a set of flip-flops holding bits.

Unless stated otherwise, a register is **one bit** wide. For more bits we must declare it explicitly, giving the range. Registers wider than one bit are **unsigned** by default; if we want them signed we add the `signed` keyword:

```verilog
reg clock;           /* One-bit register */
reg [31:0] busA;     /* 32-bit register, unsigned */
reg signed [63:0] m; /* 64-bit register, signed */
```

The notation `[31:0]` means that the most significant bit is 31 and the least significant is 0.

When assigning a value we can write the whole register or just a subset of its bits. If what we assign is a constant, we may prefix it with its size in bits:

```verilog
clock = 1'b0;         // 1 bit, binary value 0
busA = 'hAAAABBBB;    // the whole register
busA[7:4] = 4'hC;     // only bits 7 down to 4
m = -1;               // signed register
```

## Exercise 2. Working with registers

Declare the variables of the previous section, assign them those same values, and print them in hexadecimal. **Before running**, try to predict what will appear on screen.

Then answer, first by hand and then with Verilog:

1. Store the number `2323` in a 16-bit register and print it in binary and hexadecimal.
2. Write, in hexadecimal, binary, and decimal, the largest and the smallest number that can be stored in a 16-bit **unsigned** register.
3. What is the binary expression of the number `6789` when represented in two's complement in a 16-bit register?
4. Express `-22` in an eight-bit register and move it into a 16-bit one **extending the sign**.

## Arithmetic operators

The arithmetic operators match those of C, with one addition:

| Operator | Operation |
|---|---|
| `+` | Addition |
| `-` | Subtraction |
| `*` | Multiplication |
| `/` | Division |
| `%` | Modulo (remainder of integer division) |
| `**` | Exponentiation (not present in C) |

Dividing two integer quantities returns **only the integer part** of the quotient. For the remainder we use the modulo operator `%`. For example, `17 / 5` is `3` and `17 % 5` is `2`.

## Nets and wires

There is a special kind of variable in Verilog generically called **nets**. The most common one is **`wire`**.

These variables are used just like real wires: to **connect** gates or modules to each other. Their size is one bit by default.

The key difference from registers is this:

| | `reg` | `wire` |
|---|---|---|
| What it does | **Stores** a value | **Carries** a value |
| Where its value comes from | An assignment inside a block | Another element feeding it continuously |
| Analogy | A switch that stays set | A wire that only carries what reaches it |

A `wire` needs some other element to supply its value at all times; it cannot remember it by itself. We will use wires in earnest from the logic gates session onwards.

## Special values: `x` and `z`

Every bit of a wire or a register can, besides 0 and 1, take one of these two values:

- **`x` — undefined**: the value may be zero or one, but it is not known. It shows up, for instance, when we read a register we never assigned anything to.
- **`z` — high impedance**: with its usual meaning in electronics; the wire is effectively disconnected.

Both `x` and `z` work as ordinary digits inside a constant. For example, `'b11xxzz00` means the first two bits are 1, the next two are unknown, the next two are in high impedance, and the last two are 0.

One rule is worth knowing: if we assign a register a value with **fewer bits** than the register has, the leftover bits on the left are filled as follows:

| Most significant bit of the assigned value | What the left side is filled with |
|---|---|
| `0` or `1` | With `0` |
| `x` | With `x` |
| `z` | With `z` |

## Exercise 3. Registers with undefined values

Define a 16-bit register whose four most significant bits are zeros, the next four ones, the next four `x`, and the last four `z`.

Print the register value in binary. Then perform arithmetic operations with it (an addition, a multiplication) and print the result.

## Related terminal commands

A reminder from session 0 with the commands you will use most in these labs:

| Command | What it does |
|---|---|
| `ls` | Lists the contents of a directory |
| `cd` | Changes the working directory |
| `cat` | Shows the contents of a file |
| `rm` | Deletes a file |
| `man` | Shows the manual page of a command. Quit with `q` |

## Common errors in this session

| Message or symptom | What to check |
|---|---|
| `syntax error` when compiling | A semicolon is missing at the end of a statement or a declaration |
| `I give up.` after the previous error | The usual `iverilog` message when it cannot continue; fix the first error in the list and compile again |
| Nothing is printed | The `initial` block is missing, or the `$display` is outside the module |
| `x` is printed instead of a number | The variable has no assigned value, or an operation involved a value containing `x` |
| `./hello: No such file or directory` | You have not compiled yet, or the name after `-o` does not match the one you run |
| The number is right in decimal but wrong in binary | Check the format code: `%d` and `%b` are not interchangeable |

## Closing checkpoint

Before moving on to session 2 you should be able to, without looking at your notes:

- write a minimal module with `module`, `initial`, and `endmodule`;
- compile and run it with `iverilog` and `./`;
- write a constant in the four bases;
- declare an N-bit register, signed and unsigned;
- print the same value in decimal, binary, octal, and hexadecimal.

Save the `.v` file for each exercise and write down next to it what you expected and what the simulation actually printed. Comparing both is the fastest way to find mistakes.

## Original Source

Content adapted to TeachBook from the course reference page: <http://avellano.fis.usal.es/~compi/sesion1.htm>.
