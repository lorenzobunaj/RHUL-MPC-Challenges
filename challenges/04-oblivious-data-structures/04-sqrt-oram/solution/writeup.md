# Square-Root ORAM

**Challenge name**: Square-Root ORAM\
**Category**: Oblivious Data Structures\
**Author**: Lorenzo Bunaj

## Challenge

This challenge implements an Oblivious RAM based on the Square-Root model, where the size of the internal memory is $N + \sqrt{N}$, divided into the actual data array (size $N$), for which the access is $\mathcal{O}(1)$, and the stash (size $\mathcal{O}(\sqrt{N})$), which is scanned linearly.

According to the standard implementation, at every read operation:
- The whole stash is scanned, if the block id is included in it is returned only at the end of the linear search
- If the block id is not in stash
    - It is taken from the data array as $\text{Array}[\pi(\text{bid})]$, where $\pi$ is the mapping function, to keep the accesses oblivious
    - The block is added to the stash
    - If the stash is storing $\lceil{\sqrt{N}}\rceil$, it is emptied and the mapping function $\pi$ is updated

The server provides the user with an oracle, which can be used to:
- Perform a read operation to get $\text{flag}[i]$, where $i$ is the user's input, but the byte is not printed.
- Perform a read operation to get $d \leftarrow \text{ORAM}.\text{Read}(i)$, where $i$ is the user's input and $d$ is printed.

## Solution

The vulnerability of the ORAM construction has to be found in the $\text{ORAM}.\text{Read}$ implementation.

In fact, instead of scanning the whole stash, the data is returned as soon as it's found. Additionally, a 0.2 seconds delay is added at each entry scan, to make this flaw exploitable through side-channels.

The procedure would therefore be to first read the first 4 bytes of the flag, which will occupy the first 4 entries of the stash. Then, read the block $1, 2, 3, 4$, if one of this blocks corresponds to a flag byte, the delay will be smaller and, based on it, we would be able to understand at which index of the flag corresponds

### Example

We read the flag bytes $f_1, f_2, f_3, f_4$, corresponding to the blocks:
```math
\begin{cases}
b_1 = (45, f_1)\\
b_2 = (32, f_2)\\
b_3 = (2, f_3)\\
b_4 = (24, f_4)
\end{cases}
```
so the stash is now:
```math
[b_1, b_2, b_3, b_4]
```
Therefore, when we try to read in sequence the blocks $1, 2, 3, 4$, we would get the following delays:
```math
\begin{cases}
\text{delay}_1 = 0.8\\
\text{delay}_2 = 0.4\\
\text{delay}_3 = 1\\
\text{delay}_4 = 1.2
\end{cases}
```
we can see the chain broke at the second block (we expected $1$ but we got $0.4$), so we deduce the block $2$ is in the third position in the stash, hence its corresponding data is the third byte of the flag.

The choice to use exactly half of the stash for the flag bytes and the other half for the guess blocks it's not random, it is made to maximize the probability of guessing one of the read flag bytes using a limited amount of block ids.