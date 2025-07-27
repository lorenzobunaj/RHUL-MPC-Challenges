# Oblivious Permutation

**Challenge name**: Oblivious Permutation\
**Category**: Implementation Techniques\
**Author**: Lorenzo Bunaj

## Challenge

This challenge implements a custom Oblivious Permutation Protocol, where the server behaves like the permutator. Let's refer to us as $R$ and to the server as $S$.

The protocol works in the following way:
- $R$ sends his guess $g$ for the next value of $s$.
- $S$ generates a random seed $s \in \{0,1\}^{32}$. If $g = s$, $S$ prints the flag.
- $R$ sends a sequence $A = \{a_i\}_{i \in [32]}$.
- $S$ does as follows.
    - Generates a permutation keys pair $(k_1, k_2) = (\prod_{i=1}^{16} p_i^{s_i}, \prod_{i=17}^{32} p_i^{s_i})$, where $p_i$ is the $i$-th prime.
    - For $i = 1,2$
        - For $j = 32, \dots, 51$:
            - $A^j_i = \{a_1, \dots, a_{32}, \empty, \dots, \empty\}$, with $j - 32$ empty entries.
            - Shift all the elements of $A^j_i$ to the right of $k_i$ positions.
            - Publish $A^j_i$


## Solution

Let's divide the solution into two steps:
- Retrieve the seeds.
- Foresee the next seed.

### Retrieve the seeds
For a set $A_i^j$, in general holds $A^j_{i,(w + k_i) \% j} = A_{i, w}$, where $\%$ represents the modulo operator. Therefore, by sending all different element in the sequence and keeping track of the position of the first element, we get the following equivalence:

```math
k_i \equiv m_{i,j} \mod j
```

So, by applying this for each value of $j$, we get the system

```math
\begin{cases}
k_i \equiv m_{i,32} \mod 32\\
\vdots\\
k_i \equiv m_{i,51} \mod 51\\
\end{cases}
```

Which we can solve with CRT to calculate the unique solution $k_i \equiv m_i \mod L$, where $L= 32 \cdot 33\cdot ...  \cdot 51$.

We also know that $k_i$ has the following properties
- It is square free (its prime factors have all exponent equal or smaller than 1)
- Its prime factors are all smaller that $p_{16}$.
- Following from the second property, it has to be smaller than $\prod_{i=1}^{16} p_i = k_{\text{max}}$.

With high probability, the only integer for which this properties are true and whose form is
```math
m_i + tL, \space t \in \mathbb{N}
```
is exactly $k_i$.

Once we got $k_i$, we can compute $s_i$ as $s_{i,1} ||\dots || s_{i,16}$, where
```math
s_{i,j} =
\begin{cases}
1 & \text{if } p_j | k_i \\
0 & \text{otherwise}
\end{cases}
```

And finally compute $s = s_1 || s_2$.

## Foresee the next seed

If each seed was actually random, there wouldn't be any way of foreseeing its next value.

If we take a look at the source code, we can see how the seed is generated:

```python
seed = random.getrandbits(32)
```

So $S$ is using the built-in function `random.getrandbits`, that relies on Mersenne-Twister Algorithm, which is not cryptographically secure.

It's infact well known that 624 32-bits words subsequently generated are enough to break this PRG. We can therefore execute the protocol 624 times and retrieve 624 subsequent seeds, which we can then feed to an Untwister (algorithm that breaks Mersenne-Twister), to foresee the upcoming seed and have the flag printed by $S$.