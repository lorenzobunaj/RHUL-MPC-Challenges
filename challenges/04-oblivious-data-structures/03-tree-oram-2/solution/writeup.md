# Oblivious RAM 2

**Challenge name**: Oblivious RAM 2\
**Category**: Oblivious Data Structures\
**Author**: Lorenzo Bunaj

## Challenge

The flag is encrypted using a 16-bytes secret $\text{secret}$.

This challenge implements a Tree-Based Oblivious RAM very similar to the one of Oblivious RAM 1. However, the previous vulnerabilities are patched and it mostly follows a standard implementation.

The only custom feature is the $\text{ORAM.Remap}$ function, which, instead of mapping the block to a new random position, behaves like follows:
- If called inside $\text{ORAM.Write}$, generates the new position as $p_k = p_0^{s^{\text{cnt}}}$.
- If called inside $\text{ORAM.Read}$, increments $\text{cnt}$ and generates the new position as $p_k = p_0^{s^{\text{cnt}}}$.

$\text{cnt}$ is a global attribute and is initialized at 0, while $p_0$ is the block's original position, assigned randomly during the $\text{OKVS}$ initialization. All the exponentiation operations are over $\mathbb{Z}_N$, where $N$ is the $\text{OKVS}$ size.

The server provides an oracle to the user, which allows him to:
- Read the content of a block.
- Dump the positions map.
- Reset the $\text{OKVS}$ structure.

The $\text{OKVS.Reset}$ operation reinitialize the memory as the start, with $N$ brand new blocks (inserted through new $N$ write operations). Every time the reset oracle is called, also $s$ is updated. On the $n$-th reset operation
```math
s_n = \text{secret}_{2n - 1}|\text{secret}_{2n}
```
Since the length of $\text{secret}$ is 16, the memory has a limit of 8 reset operations.

## Solution

Let's refer to $s_1$ as $s$ and let's just focus on retrieving it. If we know how to retrieve a 2-byte piece of $\text{secret}$, we can retrieve all the other by just resetting the memory.

It's also important to notice that $N = 65537 \in \mathbb{P}$, so the exponentiation operations are over $\mathbb{Z}_N^*$.

Another important observation is that, if we convert $s$ into an integer (as the server does to be able to use it as an exponent), we have $s < 2^{16} \Rightarrow s \in \mathbb{Z}_N^*$. So, every time the server computes $p^{s^\text{cnt}}$, is doing operations over $\mathbb{Z}_N^*$.

Let's now dive into the actual solution.

To start, we can dump the positions map $\text{pm}$ and select a block id $t$ such that $\text{pm}[t]$ has multiplicative order $N - 1$ modulo $N$. Let's call $\text{pm}[\text{bid}] = g$ and the chosen block id $t$.

If we now execute a read operation (without caring about the block data), using $t$ as input, the next dump we will be able to get $\text{pm}[t] = g^s$.

If we iterate this process (read block $t$ and dump), at the $d$-th iteration we can retrieve $g^{s^d}$. If we chose $d$ s.t. $d \mid p - 1$ (as instance $d = 2^5$), we can use the [Cheon's Algorithm](https://www.math.snu.ac.kr/~jhcheon/publications/2006/Eurocrypt_Cheon_LNCS.pdf) to efficiently compute $s$ from triples in the form
```math
\left(g, g^s, g^{s^d}\right) \space:\space s, d \in \langle g \rangle, d \mid p - 1
```
Remember we accurately choosed $g$ to be a generator for $\mathbb{Z}_N^*$, so our parameters meet the requirements.