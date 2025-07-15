# Optimized OT

**Challenge name**: Optimized OT\
**Category**: Foundamentals MPC Protocols\
**Author**: Lorenzo Bunaj

## Challenge

The challenge implements $m$ $1$-out-of-$2$ OT Protocol using the IKNP model.

The server encrypts the flag using the key $\text{secret}$ s.t.

```math
\text{secret}[i] =
\begin{cases}
    m_1[i] &\text{if } 2 \mid i\\
    m_2[i] &\text{otherwise}
\end{cases}
```

where $(m_1[i], m_2[i])$ is the pair of message used in the $i$-th OT Protocol.

The user plays the role of the receiver $R$. The interaction between $R$ and $S$ is facilitated by the server, which plays the role of a secure third-party.

The rest of the protocol strictly follows the standard IKNP Protocol of Kolesnikov and Kumaresan, with $m = k = 16$ and where the single entries of the matrices $T, U, Q$ are single bytes.

## Solution

To get the $\text{secret}$ to send to the server to decrypt the flag, we can generate the choice bits $r$ as

```math
r_i =
\begin{cases}
    0 &\text{if } 2 \mid i\\
    1 &\text{otherwise}
\end{cases}
```

to correctly participate in the protocol, we also need to initialize $T, U \in \{0, 255\}^{16\times16}$. We need the following properties to be always valid:

```math
\bold{t}_j \oplus \bold{u}_j = r_j \cdot \bold{1}^{16} =
\begin{cases}
    \bold{1}^{16} &\text{if } r_j = 1\\
    \bold{0}^{16} &\text{if } r_j = 0
\end{cases}
```

where $\bold{t}_j, \bold{u}_j$ are the rows of $T, U$.

So, we can first initialize the rows of $T$ as $\bold{t}_j \in_R \{0, 255\}^{16}$, and then calculate the rows of $U$ as $\bold{u}_j = \bold{t}_j \oplus (r_j \cdot \bold{1}^{16})$, in order for the above property to be always respected.

Now that we got all the parameters needed to participate in the protocol, the only thing remained is sending the correct data in the required format and await for the server to print us the flag.