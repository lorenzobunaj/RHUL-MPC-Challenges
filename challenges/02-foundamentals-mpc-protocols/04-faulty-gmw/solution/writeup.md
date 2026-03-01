# Faulty GMW

**Challenge name**: Faulty GMW\
**Category**: Foundamentals MPC Protocols\
**Author**: Lorenzo Bunaj

## Challenge

The flag is encrypted using a secret generated as the output of $C : (x, y) \mapsto \text{secret}$, with $x, y \in_R [0, 255]^{16 \cdot 4}$ and secret defined as.

```math
\text{secret} = (t_1 \oplus t_2) \oplus (t_3 \land t_4)
```

where $t_i = x_i \oplus y_i$ if $i \not = 4$ and $t_3 = x_3 \land y_3$, s.t.

```math
x_i = x[16i : 16(i+1)] \\
y_i = y[16i : 16(i+1)]
```

After the encryption, the server participates in a GMW protocol with the user where $C$ is evaluated using shares and GMW XOR, NOT and AND gates, using $x$ and $y$ as inputs.
The shares are defined as:
```math
\begin{cases}
    x = s_x \oplus r_x \\
    y = s_y \oplus r_y
\end{cases}
```
with $r_i \in_R [0, 255]^{16}$.

At the end of the protocol, the server takes the final share from the user and XORs it with its final share, and use the result to decrypt the encrypted flag.

If the two shares are correct, the server will output the original flag.

## Solution

The vulnerability lies in the fact that, differently from the previous exercise, the original circuit used to compute secret and its GMW implementation are not coherent.

In particular, following the server GMW computation in the evaluation of the $t_i$ values, we see that $t_2$ is computed as $t_2 = x_2 \land y_2$. So the server is using an AND gate while it should be using a XOR one.

We need to strictly follow the circuit logic to get the flag, so, during the communication for the evaluation of $t_2$, we need to send a payload to the server in order to trick it to execute a XOR operation instead of a AND one.

For the faulty AND gate, we will therefore send the table

```math
\text{table}(r_x, s_y) = \{r \oplus (s_x' \oplus r_x) \oplus (s_y \oplus r_y')\}_{s_x', r_y' \in \{0,1\}}
```

the server will then pick the rows $n$ for which $n = 2s_x + r_y$, obtaining a share of a XOR gate
