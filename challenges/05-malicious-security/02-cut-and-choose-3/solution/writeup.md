# Cut And Choose 3

**Challenge name**: Cut And Choose 3\
**Category**: Malicious Security\
**Author**: Lorenzo Bunaj

## Challenge

This challenge implements an evaluation protocol of a Garbled AND gate, with Cut-And-Choose security optimization.

The server $S$ has an input $s \in \{0, 1\}^{64}$.

It samples $96$ garbled circuits and sends their commitments $C_i = \mathrm{PRG}(\mathrm{seed}_i) \oplus \mu_i$, the player $P$ can pick up to $32$ GCs and ask $S$ to open them. $S$ does this by sending $\mathrm{seed}_i$ for every choosen circuit.

After $P$ has verified the server is honest, can send their input $y$. The evaluation of the AND gate is made bit-a-bit over the first $64$ available closed circuits.

For every evaluation $s_i \wedge y_i = z_i$, $P$ receives:
* The corresponding label $L_i^{z_i}$
* The $L_i'$ label, which is the bases from which the two labels are derived, in particular
```math
\begin{aligned}
    L_i^0 &= L_i' \oplus \mu_i \\
    L_i^1 &= L_i' \oplus \mu_i \oplus \Delta
\end{aligned}
```

After the first round of evaluations, $S$ asks for another value $x$, if $s \oplus x = 0$ ($x = s$), the flag is printed.

## Solution

The goal is to retrieve $s$. 

We could do it during the first round of evaluations if we could guess if $L_i^{z_i} =^? L_i^0$ or $L_i^{z_i} =^? L_i^1$, for every $i$. We have $L_i'$, so the previous request can be translated into $L_i^{z_i} \oplus L_i' =^? \mu_i$, if yes, then we know that $z_i = 0$, otherwise $z_i = 1$.

By sending $y_i$ everytime, we have that
```math
\begin{aligned}
    L_i^{z_i} \oplus L_i' &= \mu_i \Rightarrow s_i = 0 \\
    L_i^{z_i} \oplus L_i' &\not= \mu_i \Rightarrow s_i = 1 \\
\end{aligned}
```
This way we fabricated for the bits of $s$.

By checking the code carefully, we can notice that $\mu_i$ is not a random masking, but $\mu_i = F(i)$ for some random sampled $32$-degree polynomial. If therefore we ask to open $32$ circuits (without less of generality, let's assume we picked the first $32$), we can compute $p_i = \mathrm{PRG}(\mathrm{seed}_i)$ for everyone of them and retrieve
```math
\begin{aligned}
    \mu_1 &= C_1 \oplus p_1\\
    \mu_2 &= C_2 \oplus p_2\\
    \vdots \\
    \mu_{32} &= C_{32} \oplus p_{32}\\
\end{aligned}
```

Now, we can feed the points $(0, \mu_1), (1, \mu_2), \dots, (31, \mu_{32})$ to a Lagrange Interpolation algorithm and recover $F$. Finally, we can compute $\mu_i = F(i)$ for all the missing masks and make the oracle work.