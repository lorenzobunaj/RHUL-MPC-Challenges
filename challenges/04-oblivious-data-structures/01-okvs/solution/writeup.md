# OKVS

**Challenge name**: OKVS\
**Category**: Oblivious Data Structures\
**Author**: Lorenzo Bunaj

## Challenge

This challenge implements an OKVS construction which is used by the server $S$ to store some random values $v_0, \dots, v_{9}$ and the secret $x$ used to encrypt the flag.

Before the communication starts, the server sends the encrypted flag and the necessary parameters to decrypt it, except $x$.

After that, the computation by $S$ continues as follows:

- for $i = 0\dots9$:
    - $k_i = \text{bytes}(i, \dots , i)$
    - $\text{OKVS.Enc}(v_i, k_i)$
- $\text{OKVS.Enc}(b, h(x))$, $b \in_R \{0, 255\}^{16}$
- $SV =\text{Shuffle}(\{v_0, \dots, v_9\})$
- Send $\text{OKVS}$ and $SV$ to the user.

Where $x_1'x_2'x_3'x_4' \leftarrow h(x_1x_2x_3x_4)$ is computed as:
```math
\begin{cases}
x_1' = x_4 \oplus x_1\\
x_2' = x_1' \oplus x_2\\
x_3' = x_2' \oplus x_3\\
x_4' = x_3' \oplus x_4
\end{cases}
```

Where, referring as $A$ to the internal $\text{OKVS}$ array, $\text{OKVS.Enc}(v, k)$ is such that:

```math
A[p_i] = A[p_i] \oplus k
```

with

```math
\{p_1, p_2, p_3\} \leftarrow H(v)
```

s.t. $H$ samples 3 random indices over $[10]$, using $v$ as the Mersenne Twister seed.

## Solution

The vulnerability is that the key generation logic is predictable, so, having the original values array, we can recreate the $\text{OKVS}$ without the secret $x$ and XOR each entry. The entries different from all zero bytes will be equal to $h(x)$, which is invertible.

Let's go step by step.

First, we need to find the right permutation of the values array. The only way to do it is to check all the possible permutations, finish the flag decryption and check, at the end, if the flag starts with "RHUL". So let's assume we are in the round corresponding to the right permutation $V$.

We can recreate the $\text{OKVS}$ without the flag as

- for $i = 0\dots9$:
    - $k_i = \text{bytes}(i, \dots , i)$
    - $\text{OKVS.Enc}(V[i], k_i)$

We can now take $S$'s $\text{OKVS}$ internal array $A$ and our's $\text{OKVS}$ internal array $B$ and XOR them together entry by entry, to get

```math
A[i] \oplus B[i] =
\begin{cases}
0 &\text{if } i \not \in H(x)\\
h(x) &\text{if } i \in H(x)\\
\end{cases}
```

With high probability, $h(x) \not = 0$, so we can recognize it and invert the computation of the hash by applying $h^{-1}$ defined as
```math
h^{-1}(x_1'x_2'x_3'x_4') \rightarrow x_1x_2x_3x_4
```
such that
```math
\begin{cases}
x_1 = x_4 \oplus x_1'\\
x_2 = x_1' \oplus x_2'\\
x_3 = x_2' \oplus x_3'\\
x_4 = x_3' \oplus x_4'
\end{cases}
```

So, once we got $x$, we can retrieve the flag by just decrypting the ciphertext initially sent by $S$.