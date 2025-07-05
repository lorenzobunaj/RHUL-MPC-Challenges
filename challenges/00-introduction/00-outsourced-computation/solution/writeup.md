## Protocol
- $P_A$ sends
    $$
    I_A^1 = f_r(\text{flag})
    $$

    to $P_B$.
    Where $f_r(x) = 3^r x$, with $r \in_R [8, 9, \dots, 15]$.

- $P_B$ computes
    $$
    I_B^1 = I_A^1 \oplus g(s_B)
    $$

    where $g(x) = (x = 0 \lor (x \land (x-1) = 0))$ and sends it to $P_A$.

- $P_A$ computes
    $$
    I_A^2 = I_B^1 \oplus K
    $$

    where $K = 0101...1010$ with $(2 * r + 1)$ bits, and sends it to $P_B$

- $P_B$ computes
    $$
    I_B^2 = I_A^2 \oplus g(s_B \gg 1)
    $$

    and publish it.

## Vulnerability

It seems like the protocol is made of many hard computations, which makes hard to retrieve the flag.

In reality, if we analyze the function $g$, performed on the inputs by $P_B$, we notice that, if $\text{len}(x) > 1$,
$$
    g(x) = g(x \gg 1)\;\; \forall t \in \mathbb{N}
$$

So, calling $g(s_B) = g(s_B \gg 1) = T$, we have
$$
    I_B^2 = I_A^2 \oplus T = I_A^1 \oplus T \oplus K \oplus T = I_A^1 \oplus K
$$

Then we see the protocol is just local computation by $P_A$.

The goal to get the flag is therefore to invert $P_A$ computation.

We can bruteforce the parameter $r$, since it can just assume integer values from 8 to 15, and calculate $K$ and $f^{-1}_{r_0}(I_A^1)$. We will apply the two inverse operations until the first 4 bytes of the result are "RHUL".