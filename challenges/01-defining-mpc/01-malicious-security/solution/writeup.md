# Malicious Security

**Challenge name**: Malicious Security\
**Category**: Defining MPC\
**Author**: Lorenzo Bunaj

## Challenge
The challenge implements the following protocol, where the user acts as $P_A$:

1) $P_A$ sends $p$, with bit-length greater than 256, to the server.

2) The server computes $y = 2^x \mod p$, for some random 16-bytes $x$.

3) $P_A$ can either get $y$ or try to decrypt $\text{ct} = \text{Enc}_x(\text{flag})$. He can repeat this interaction once, so he can do both the things.

The encryption functions is based on AES-CBC and the iv and the ciphertext are kept by the server. The only thing the user can send is his guess for the secret key.

## Solution

To get the flag, we need to decrypt it using $x$, so, for sure, one of the two interactions will be used for that.

The problem is, how do we get $x$?

The computation of $x$ is reduced to solve the Discrete Logarithm problem, which is in general an hard problem. However, in this case, we can choose the modulo $p$.

We can therefore send $p = p_1p_2 \dots p_n + 1$, where $p_1, p_2, \dots, p_n$ are the first $n$ primes, and such that $p \in \mathbb{P}$. This way, the order of $\mathbb{F}(p)$ will be $\phi(p) = p - 1 = p_1p_2 \dots p_n$, which is easily factorizable.

We can then apply the Pohlig-Hellman Algorithm for Discrete Logarithm to get $x$ very fast, due to the weak Finite Field order.