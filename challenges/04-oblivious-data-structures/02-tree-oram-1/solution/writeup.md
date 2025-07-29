# Oblivious RAM 1

**Challenge name**: Oblivious RAM 1\
**Category**: Oblivious Data Structures\
**Author**: Lorenzo Bunaj

## Challenge

This challenge implements a Tree-based ORAM Structure, which is used to store data in an oblivious way, where the user can write/read data to/from the memory but doesn't know where they are stored.

The server encrypts the flag using $\text{secret}$ as the secret key and shares all the other parameters needed to decrypt it (included the ciphertext).

It provides an oracle which allows the user to:
- Enter a block id and read the corresponding data.
- Dump the whole positions map, which maps each block to its bucket

The $\text{ORAM.Dump}$ function, other than returning the positions map, also:
- Generates a random block id $\text{bid}$
- Generates a random data block as $b_1 \dots b_{15}|s_k$, s.t. $b_i \in_R \{0, 255\}$ and $s_k = \text{secret}[\text{bid} \mod 16]$.

## Solution

The vulnerability has to be found inside the $\text{ORAM}$ construction. It infact has two main flaws:
- First, the most obvious, the writing operation inside $\text{ORAM.Dump}$, which is the main tool we have to retrieve $\text{secret}$.
- The other one, less trivial, is that there is no remapping in $\text{ORAM.Read}$, so, when we read the content of a block, the internal structure of the ORAM stays the same.

The modus operandi would therefore be
- Dump the positions map $\text{pm}_1$
- While $\text{secret}$ is not fully recovered:
    - Dump the positions map $\text{pm}_2$.
    - Find $k$ such that $\text{pm}_1[k] \not = \text{pm}_2[k]$, that is the block id wrote with the new dump operation.
    - if $(k \mod 16)$ wasn't already found:
        - Read the content of block $k$ and extract its last byte $s_k$.
        - $\text{secret}[k \mod 16] = s_k$.
    - $\text{pm}_1 \leftarrow \text{pm}_2$.

Once we fully recovered $\text{secret}$, we can use it to decrypt the flag and win.


