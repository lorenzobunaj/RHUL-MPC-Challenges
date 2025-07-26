# Semi-Honest Security

**Challenge name**: Semi-Honest Security\
**Category**: Defining MPC\
**Author**: Lorenzo Bunaj

## Challenge

The challenge implements the following protocol and shares $P_B$'s view to the user (the server acts as the trusted party, which facilitates the computation):
1) $P_A$ sends $a, b, c, x, y, z$ to a trusted party $\mathcal{F}$. Where

    ```math
        \begin{cases}
        ax + by + cz = 325207 \\
        -ax + by + cz = 145609 \\
        -2ax - 3by + 2cz = -110749
        \end{cases}
    ```

    and $a, b, c \in _R [2^9, 2^{11}]$

2) $P_B$ samples $s_0, s_1 \in _R \{0, 1\}$ and send them to $\mathcal{F}$, which acts on them in order to set $s_0 = s_1 = 0$, if $s_0 = s_1 = 1$.

3) $\mathcal{F}$ sends the $n$-th value chosen between $\{a, b, c\}, where $n = s_0 + 2s_1$. And \{x, y, z\} except the $n$-th value (the order is based on the position).

## Solution

To get the flag, we need to compute $abc$.

The vulnerability lies in the fact that we know two out of three of $\{x, y, z\}$ and the coefficient associated to the remaining unknown. So we can solve the same linear system to get all the coefficients and unknowns.

### Example

From the protocol, we get $a = a_0$ and $y = y_0, z = z_0$, then we can retrieve $b, c, x$ by solving the linear system

```math
    \begin{cases}
    a_0x + by_0 + cz_0 = 325207 \\
    -a_0x + by_0 + cz_0 = 145609 \\
    -2a_0x - 3by_0 + 2cz_0 = -110749
    \end{cases}
```

Likely $y_0, z_0$ won't be integers, so we need to consider the approximated values of $b, c, x$ to the nearest integer for the solution.

Once we got $b, c$, computing $abc$ and sending it to the server is trivial.