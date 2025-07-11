# Garbled Circuits

**Challenge name**: Garbled Circuits\
**Category**: Foundamentals MPC Protocols\
**Author**: Lorenzo Bunaj

## Challenge

This challenge implements a GC (garbled circuit), where the secret used to encrypt the flag is divided in bytes (16).

The generic byte $s_x$ is then encrypted in the gate $G_{i, j}$ as

```math
L_{i,j}^1 = \text{000}\dots\text{000}s_x
```

where $i = x / 4$ and $j = x \mod 4$.

Looking more closer the gates of the circuit, we notice that the same four operations are repeated: AND, NOR, NAND, XOR. We notice that each column of gates (e.g. the set $C_n = \{G_{i, j} : i = n, j \le 3\}$) contains all and only those four operations and the same applies to the rows $R_m =\{G_{i, j} : i = \le 3, j = m\}$. Even more, the order in which they appear it's always the same: AND, NOR, NAND, XOR, AND, NOR, NAND, $\dots$.

So, by just knowing the first gate $G_{0,0}$, we can reconstruct the logic of the whole GC.

We additionally know all the labels and the pointer bits of the input wires.

## Solution

The solution of this challenge is very similar to the one already saw for the single gate circuit, with the additional fact that, once we got the labels of the first column of gates, we need to use them to get the ones of the second column, and so on.

Once we got $(L_{i,j}^0, L_{i,j}^1)$ for all the combinations of $i$ and $j$, we can extract the last byte from each $L^1$ and get the secret to decrypt the flag, similarly to what done before.