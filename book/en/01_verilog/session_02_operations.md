# Session 2. Bit operations

In session 1 we learned to store values in registers and print them in different bases. Now we are going to **manipulate their bits one by one**: turn some on, turn others off, and leave the rest untouched.

```{admonition} Learning objectives
:class: tip

- Tell bitwise operators (`~`, `&`, `|`, `^`) apart from logical operators (`!`, `&&`, `||`).
- Compute the one's complement of a register.
- Build a binary mask to set, clear, or flip a group of bits.
- Use reduction operators to apply a logical operation to every bit of a register.
- Compute a parity bit and understand what it is for.
```

## Bit operations

Sometimes we want to act on a specific group of bits while **leaving the rest unchanged**. This happens, for instance, when a control register holds several independent flags: we want to change one without touching the others.

In this session we will learn to set, clear, flip, and reduce the bits of a register in Verilog.

```{admonition} Two families of operators that look alike
:class: warning

Verilog has **bitwise** operators and **logical** operators. They are written in similar ways and do different things:

| Bitwise | Logical | Difference |
|---|---|---|
| `~` (NOT) | `!` | `~` inverts every bit; `!` gives 1 or 0 depending on whether the whole register is zero |
| `&` (AND) | `&&` | `&` works bit by bit; `&&` works on truth values |
| `\|` (OR) | `\|\|` | `\|` works bit by bit; `\|\|` works on truth values |

In this session we **always** use the ones in the left column. Writing `&&` where `&` was needed is the most frequent mistake in this lab.
```

## One's complement: the `~` operator

Changing every bit of a register from 0 to 1 and from 1 to 0 is called the **one's complement**. In Verilog we do it with the `~` operator, also known as bitwise NOT:

| Operation | Value |
|---|---|
| Original | `1011101010101011` |
| `~` | `0100010101010100` |

```verilog
reg [15:0] r;

initial
begin
  r = 16'b1011101010101011;
  $display("original   = %b", r);
  $display("complement = %b", ~r);
end
```

## Masks: the key idea of this session

To touch only some bits we use a **mask**: a binary value the same size as the register, where we mark the positions we care about.

The recipe always has two steps:

1. Build the mask marking the positions to touch.
2. Combine register and mask with the right operator: `|` to set, `&` to clear, `^` to flip.

```{admonition} How bits are numbered
:class: note

In this book bit **0** is the rightmost one (the least significant), just as in the `reg [15:0]` notation of session 1. So "the third bit counting from the right" is bit number 2.
```

## Setting bits: OR (`|`)

To **set** a group of bits while leaving the rest as they are, we build a mask with a **1** in every position we want to turn on and a **0** in the ones we want to leave alone. Then we combine it with the register using an **OR** operation (`|`).

It works because `x | 0` leaves `x` as it was, while `x | 1` is always 1.

For example, to set the first, third, and seventh bits counting from the right, the mask is `'b1000101`:

| Operation | Value |
|---|---|
| Register | `1011101010101011` |
| `\|` mask | `0000000001000101` |
| Result | `1011101011101111` |

The three bits marked by the mask are now 1, and the others have not moved.

```verilog
r = r | 16'b0000000001000101;
```

## Clearing bits: AND (`&`)

The mask is built **the other way round**: a **0** in every place we want to turn off and a **1** everywhere else. The operation is **AND** (`&`).

It works because `x & 1` leaves `x` as it was, while `x & 0` is always 0.

To clear the same first, third, and seventh bits from the right, the mask is `~'b1000101`, which in 16 bits looks like this:

| Operation | Value |
|---|---|
| Register | `1011101010101011` |
| `&` mask | `1111111110111010` |
| Result | `1011101010101010` |

Note the trick: instead of writing the long mask by hand, write the "set" mask and apply `~` to it. It is shorter and far harder to get wrong.

```verilog
r = r & ~16'b0000000001000101;
```

## Flipping bits: XOR (`^`)

Here we change a group of bits to their opposite value, leaving the rest alone. The mask is built just as in the set case, and the operation is **XOR** (`^`).

It works because `x ^ 0` leaves `x` as it was, while `x ^ 1` inverts `x`.

| Operation | Value |
|---|---|
| Register | `1011101010101011` |
| `^` mask | `0000000001000101` |
| Result | `1011101011101110` |

```verilog
r = r ^ 16'b0000000001000101;
```

## The three masks at a glance

| I want to | Mask | Operator | Why it works |
|---|---|---|---|
| Set bits | `1` where I touch, `0` elsewhere | `\|` | `x \| 0 = x`, `x \| 1 = 1` |
| Clear bits | `0` where I touch, `1` elsewhere | `&` | `x & 1 = x`, `x & 0 = 0` |
| Flip bits | `1` where I touch, `0` elsewhere | `^` | `x ^ 0 = x`, `x ^ 1 = NOT x` |

Two of the three masks are written the same way; what changes is the operator. The clearing one is the same mask, negated with `~`.

## Exercise 1. Set, clear, and flip

Declare an unsigned sixteen-bit register and give it any initial value. Counting from the right:

1. Set the fifth bit.
2. Clear the ninth, tenth, and eleventh bits.
3. Flip the sixteenth bit.

Print the register contents in binary **before and after** the operations, so you can compare them.

## Reduction operations

In Verilog we can, with **a single instruction**, apply a logical operation to every bit of a register. This is called a **reduction**.

The operator is written in front of the register, with no second operand. For example, if `r` is a four-bit register whose value is `'b1100`, the AND reduction is written `&r` and is equivalent to:

```text
0 & 0 & 1 & 1
```

That is, the operation is applied to all the bits of the register, right to left. The result is **a single bit**.

Reduction works with all the main operations:

| Operation | Symbol | Operation | Symbol |
|---|---|---|---|
| and | `&` | nand | `~&` |
| or | `\|` | nor | `~\|` |
| xor | `^` | xnor | `~^` or `^~` |

```{admonition} What each reduction answers
:class: tip

Reductions answer very specific questions about a register:

- `&r` is 1 only if **every** bit is 1.
- `|r` is 1 if **any** bit is 1, that is, if the register is not zero.

Before using a reduction, ask what you want to know about the register and pick the operator that answers that question.
```

## Exercise 2. The parity bit

The **even parity** bit of a register is defined like this:

- 0, if the number of bits set to 1 in the register is even.
- 1, if the number of bits set to 1 in the register is odd.

The **odd parity** bit is exactly the opposite:

- 0, if the number of bits set to 1 in the register is odd.
- 1, if the number of bits set to 1 in the register is even.

These bits are used to **detect transmission errors**: the sender computes the parity and sends it along with the data; the receiver computes it again and checks that both match. If they do not, some bit changed along the way.

Write a Verilog program that, given an eight-bit register:

1. Clears the most significant bit of the register.
2. Prints the register in binary.
3. Computes the even parity bit of the register using a reduction instruction.
4. Stores that bit in the most significant bit of the register.
5. Prints the modified register in binary.

Finally, decide **without Verilog's help**: if `8'b10101010` is received with the odd parity bit stored in the most significant bit, is it a transmission error or not?

## Related terminal commands

The usual ones; keep them at hand during the lab:

| Command | What it does |
|---|---|
| `ls` | Lists the contents of a directory |
| `cd` | Changes the working directory |
| `cat` | Shows the contents of a file |
| `rm` | Deletes a file |
| `man` | Shows the manual page of a command. Quit with `q` |

## Common errors in this session

| Symptom | What to check |
|---|---|
| The result is always `1` or `0`, never a bit pattern | You used a logical operator (`&&`, `\|\|`, `!`) where a bitwise one was needed (`&`, `\|`, `~`) |
| Bits change that should not have changed | The mask is not the size of the register, or you counted bits from the wrong side |
| Clearing sets everything to zero | You used the setting mask without negating it with `~` |
| The reduction returns several bits | You wrote the operator between two registers instead of in front of a single one |
| The result shows `x` | The register had no value assigned before operating, as we saw in session 1 |

## Closing checkpoint

Before moving on to session 3 you should be able to, without looking at your notes:

- explain the difference between `&` and `&&`;
- write the mask that sets, clears, or flips a given group of bits;
- say which operator goes with each of those three masks;
- compute the even parity bit of a register with a single instruction.

Save the `.v` file for each exercise and write down next to it what you expected and what the simulation actually printed.

## Original Source

Content adapted to TeachBook from the course reference page: <http://avellano.fis.usal.es/~compi/sesion2.htm>.
