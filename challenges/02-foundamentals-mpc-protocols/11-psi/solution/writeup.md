# PSI Protocol

**Challenge name**: PSI Protocol\
**Category**: Foundamentals MPC Protocols\
**Author**: Lorenzo Bunaj

## Challenge

This challenge implements a Private Set Intersection using two main primitives: Cuckoo Hashing and OPRF.

For the goal of the challenge, we don't really care about the internal details of these two primitives, but only about their behaviors.

A Cuckoo Hashing technique works in the following way:
- When hashing a value $x$, we calculate $b_1 = h_1(x), b_2 = h_2(x), b_3 = h_3(x)$, where $h_1, h_2, h_3$ are three different hash functions.
- If at least one position in the Hash Table is free among $b_1, b_2$ and $b_3$, the value $x$ is stored there.
- If none of the positions is free, we pick a random $b_i$, where is stored $x'$ and we store $x$ there.
- We start again from step 1, by using $x = x'$.

Since, theoretically, this chain could continue forever, during the creation of the Cuckoo Hash Table we need to specify a threshold for the number of iterations of the steps, after which $x$ is stored in a special container called stash.

An OPRF Function $F : \mathcal{K} \times X \rightarrow Y$ takes a key $k$ and a value $x$ as inputs and outputs a pseudorandom outputs. This is supposed to happen obliviously, but since the server, which facilitates the computation, is considered to be a secure party, we don't need to encrypt the data before sending them to it.

The server encrypts the flag using a secret generated as the concatenation of $8$ different values $x_1||1, \dots, x_8||8$. It then proceeds to generate other $32$ values $x_9||r_1, \dots, x_{40}||r_{32}$, which are indistinguishable from the previous  (since $r_i \in_R [1,8]$), and initialize the set $S_0 = \{x_i\}_{i \in [40]}$. Finally, the server stores $\{F_k(x_i)\}_{i \in [40]}$ in a Cuckoo Table.

In parallel, the server also generate, in a similar way, the set $S_1 = \{x_1||1, \dots, x_8||8, y_1||r_1', \dots, y_{32}||r_{32}'\}$, shuffle it and send it to the user.

The user has now four options:
- Compute $F_k(x)$ for a given input $x$.
- Check if an element is contained in the Cuckoo Table.
- Get the stash.
- Try to decrypt the flag by sending a secret key value.

The user can do every operation as many times he wants, except the decryption step, for which he has only one chance.

## Solution

We can compute the OPRF corresponding value for every element $z_i||s_i \in S_1$ and we can refer to it as $f_i = F_k(z_i||s_i)$.

Now, let's retrieve the stash $S$

For $i=1\dots40$
- If $f_i \in S$, then we now $z_i$ is a piece of the secret, since $z_i||s_i$ belongs to the intersection between $S_0$ and $S_1$.
- If $f_i \not \in S$ but $\text{CuckooTable}.\text{contains}(f_i) = 1$, we can still say that $z_i||s_i$ belongs to the intersection between $S_0$ and $S_1$ and therefore $z_i$ is a piece of the secret.

Once we got all the pieces of the secret, we can order them based on the ascending order of $s_i$ and reconstruct the secret in the correct order.

By sending the right secret to the server, it will print the flag for us.