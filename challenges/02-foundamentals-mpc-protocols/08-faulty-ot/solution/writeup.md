# Faulty OT

**Challenge name**: Faulty OT\
**Category**: Foundamentals MPC Protocols\
**Author**: Lorenzo Bunaj

## Challenge

The OT protocol implemented in this challenge is very similar to the one of "Intro OT", since the foundamental idea is still a RSA-Based OT. Things are bit more complicated due to the introduction of a faulty feature.

As before, user can send the public keys and the modulo, however the modulo sent is only used for the encryptiono of $m_0$. During the encryption of $m_1$ (the flag), the server uses another modulo, chosen between a set of hardcoded moduli $[n_1, n_2, n_3]$.

The protocol is executed three times, and every time the user can send a different input.

The goal is to manage to decrypt the flag, even while not having direct control on $n$ for $m_1$.

## Solution

First, let's use the same small exponent for all the rounds, $e = 3$.

We can see that $\text{gcd}(n_1, n_2) = \text{gcd}(n_1, n_3) = \text{gcd}(n_2, n_3) = 1$. So, since we have three equations in the form

```math
\begin{cases}
    m_1^3 = c_1 \mod n_1\\
    m_1^3 = c_2 \mod n_2\\
    m_1^3 = c_3 \mod n_3
\end{cases}
```

Using the CRT theorem we can calculate the solution

```math
x = m_1^3 \mod n_1n_2n_3
````

However, as we can notice, $m_1 < n_i \space \forall i$, so $m_1^3 < n_1n_2n_3$, and therefore

```math
x = m_1^3
````

thus, we can retrieve $m_1$ (the flag) as $\sqrt[3]{x}$.

This is generally known as Hastad’s Broadcast Attack.
