# Faulty OT

**Challenge name**: Faulty OT\
**Category**: Foundamentals MPC Protocols\
**Author**: Lorenzo Bunaj

## Challenge

The OT protocol implemented in this challenge is very similar to the one of "Intro OT", since the foundamental idea is still a RSA-Based OT. Things are bit more complicated due to the introduction of a faulty feature.

As before, user can send the public keys and the modulo, however the modulo sent is only used for the encryptiono of $m_0$. 

## Solution

We can simply compute two set of parameters $(d_i, e_i, n_i)$ for RSA s.t. $e_1 \not = e_2$ and the number of bits of $n_i$ is greater than 512.

We will send $(e_1, e_2)$ to the server and decrypt the flag as

```math
\text{flag} = c_2^{d_2} \mod n_2
```