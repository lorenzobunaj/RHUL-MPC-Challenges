# OT Protocol

**Challenge name**: OT Protocol\
**Category**: Foundamentals MPC Protocols\
**Author**: Lorenzo Bunaj

## Challenge

This challenge implements a simple RSA-based Oblivious Transfer Protocol. The server keeps two messages $m_1, m_2$:
- The first one is made of random bytes
- The other is the flag

It receive from the user two public pairs $(n_1, k_1), (n_2, k_2)$. If the number of bits of $n_i$ is less than 512 or the number of bits of $k_i$ is less then 9 or $k_1 = k_2$, the protocol is interrupted.

Finally, the server computes $\{c_i\}_{i\in[2]}$ and sends it to the user, where

```math
c_i = m_i^{k_i} \mod n_i
```

## Solution

We can simply compute two set of parameters $(d_i, e_i, n_i)$ for RSA s.t. $e_1 \not = e_2$ and the number of bits of $n_i$ is greater than 512.

We will send $(e_1, e_2)$ to the server and decrypt the flag as

```math
\text{flag} = c_2^{d_2} \mod n_2
```