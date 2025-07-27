# FreeXOR

**Challenge name**: FreeXOR\
**Category**: Implementation Techniques\
**Author**: Lorenzo Bunaj

## Challenge

The server implements an AND Garbled Gate using FreeXOR Technique (e.g. $W_c^1 = W_c^0 \oplus \Delta$).

You can interact twice with the server to get the garbled table defined as
```math
H(W_A^0, W_B^0) \oplus W_c^0\\
H(W_A^0, W_B^1) \oplus W_c^0\\
H(W_A^1, W_B^0) \oplus W_c^0\\
H(W_A^1, W_B^1) \oplus W_c^1
```

Where $W_A$ is your input, while $W_B$ is generated server-side (simulates a second party).

The flag is encrypted using $\text{secret} = H(h, \Delta)$ as secret key, where
```math
h = H(W_{A, \text{round 1}}^1, W_{B, \text{round 1}}^1) \oplus H(W_{A, \text{round 2}}^0, W_{B, \text{round 2}}^0)

```

The only restriction in the user input is that every label sent in the first round has to be different from each label sent in the second round.

## Solution

For simplicity, let's send equal labels (since there is not a proper check on this option) every round, while changing between a round and another. Let's refer as $L_A^1$ to the labels sent in the first round and as $L_A^0$ to the ones sent in the second round. And let's define
```math
H(L_A^i, L_B^j) = H_{ij}
```

Note that, with this notation, we have
```math
\text{secret} = H(H_{00} \oplus H_{11}, \Delta)
```

And the tables obtained are
```math
T_0^0 = H_{10} \oplus W_c^0 \\
T_1^0 = H_{11} \oplus W_c^0\\
T_2^0 = H_{10} \oplus W_c^0\\
T_3^0 = H_{11} \oplus W_c^1
```

and
```math
T_0^1 = H_{00} \oplus W_c^0 \\
T_1^1 = H_{01} \oplus W_c^0\\
T_2^1 = H_{00} \oplus W_c^0\\
T_3^1 = H_{01} \oplus W_c^1
```

And we can therefore get $h = T_1^0 \oplus T_0^1$ and $\Delta = T_1^0 \oplus T_3^0$, to obtain the secret key and decrypt the flag.