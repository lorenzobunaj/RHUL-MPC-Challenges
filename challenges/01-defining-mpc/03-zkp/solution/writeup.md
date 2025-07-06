## Protocol
You are $P_B$ and have to interact with $P_A$, with the intermediation of a trusted party $\mathcal{F}$.

1) $P_A$ sends $y, g, p$ s.t. $y = g^x \mod p$ to $P_B$

2) $P_B$ sends $s, r$ to $P_A$.

3) If the number of bits of $s$ is at least 128 and $g^s \equiv y \cdot r \mod p$, $P_A$ will send the flag in plain.

## Vulnerability

This protocol is supposed to be a zero knowledge proof, where $P_B$ knows $x$ and wants to prove it to $P_A$ by computing

```math
r = g^k, s = k + x
```

we then want to prove we know $x$ without actually knowing it.

The vulnerability of the protocol is that in the original ZKP Protocol (Schnorr Identification Protocol), $P_B$ should first send $r$ as a commitment and then compute $s = x + k + c$, where $c$ is a random challenge sent by $P_A$. However, in this challenge, this step is skipped.

$P_B$ can therefore choose a random value $s$ (as long as its bit length is at least 128) and choose $r$ after by computing it as

```math
r = g^s \cdot y^{-1} \mod p
```

so that the identity

```math
g^s \equiv y \cdot r \mod p
```

will always hold.