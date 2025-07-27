# Half Gates

**Challenge name**: Half Gates\
**Category**: Implementation Techniques\
**Author**: Lorenzo Bunaj

## Challenge

In this challenge, the server behaves like the garbler $G$ in a Half Gates setup, which uses FreeXOR and Point and Permute.

The flag is encrypted using the secret the hashed value of $V_c$, which is the bitwise AND of $V_a$ and $V_b$. Our goal is therefore to compute $V_c$ bit by bit, by following the server logic.

In particular, we can compute each bit of $v_c$ as $v_a \land v_b$ (where $v_a, v_b$ are the bits of $V_a, V_b$ respectively), using the Half Gates protocol implemented by the server.

Let's break down each round (which correspond to the calculation of one bit) into two steps:
- Evaluating the Generator Gate $v_a \land r$
- Evaluating the Evaluator Gate $v_a \land (r \oplus v_b)$

We can then calculate $v_c$ as
```math
vc = (v_a \land r) \oplus (v_a \land (v_b \oplus r))
```

And finally decrypt the flag.

## Solution

The challenge is about how to evaluate each gate.

### Generator Gate

The server sends $a^{v_a}$ and

```math
T_1 = H(a^{v_a}) \oplus c^0 \oplus (v_a \cdot r \cdot \Delta)
```
s.t. (according to GRR3) $c^0 = H(a^0)$ and $\text{LSB}(\Delta) = 1$.

- If $v_a$, $T_1$ is made of zero bytes and $E$ can retrieve $c^0 = c^{v_a \land r}$ as $H(a^0)$.
- Otherwise, E can retrieve $c^{v_a \land r}$ as $H(a^1) \oplus T_1$, which equals
```math
c^0 \oplus r \cdot \Delta =
\begin{cases}
c^0 &r = 0\\
c^0 \oplus \Delta = c^1 &r = 1
\end{cases}
```

We can then calculate $\text{LSB}(c^{v_a \land r})$ and get $v_c' = c^0_0 \oplus (v_a \land r)$, since $\text{LSB}(\Delta) = 1$.

### Evaluator Gate

The server sends $v_a, b^{v_b}$ and
```math
T_2 = H(a^1) \oplus c^0 \oplus b^r
```

s.t. $\text{LSB}(b^0) = r$.
- If $v_a = 0$, we can just compute $c^0$ as $H(a^0)$.
- Otherwise, we compute $H(a^1) \oplus b^{v_b} \oplus T_1$, which equals
 ```math
c^0 \oplus b^r \oplus b^{v_b} =
\begin{cases}
c^0 &r = v_b\\
c^0 \oplus \Delta = c^1 &r \not = v_b
\end{cases}
```

Note that

```math
r = v_b \Leftrightarrow r \oplus v_b = 0\\
r \not= v_b \Leftrightarrow r \oplus v_b = 1
```

So we got $c^{v_a \land (r \oplus v_b)}$. We can now calculate $\text{LSB}(c^{v_a \land (r \oplus v_b)})$ and get $v_c'' = c^0_0 \oplus (v_a \land (r \oplus v_b))$.

We can finally compute $v_c = v_c' \oplus v_c''$ and be able to decrypt the flag.