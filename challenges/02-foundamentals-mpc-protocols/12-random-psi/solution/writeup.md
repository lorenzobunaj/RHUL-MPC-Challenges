# Random PSI

**Challenge name**: Random PSI\
**Category**: Foundamentals MPC Protocols\
**Author**: Lorenzo Bunaj

## Challenge

This challenge implements the same setup as the previous challenge "PSI", by adding a feature which increases the hardness to get the secret to decrypt the flag.

In particular, we don't use the Cuckoo Hash Table to store the secret bytes anymore. Instead, we replace them with some public pairs of bytes $x_i$, s.t.
```math
\text{public} = x_1\dots x_8
```
while the secret is computed as
```math
\text{secret} = x_9'\dots x_{24}'
```
where $x_i' = x_i \mod 256$ and the sequence $X = \{x_i\}$ is generated s.t.
```math
x_{i+1} = ax_i + b \mod n
```
for some $n \in_R \mathbb{256}^2$ and $x_0, a, b \in_R \mathbb{Z}_n $.

## Solution

Using the same approach as the one used in the challenge "PSI", we can retrieve $\text{public}$ and therefore the sequence:
```math
\{y_1, \dots, y_{8}\}
```

### Retrieve $n$

We know that $x_h \equiv ax_{h-1} + b \mod n$, so
```math
n \mid x_h - (ax_{h-1} + b) = s_h
```
So we could compute $n$ as $\gcd(s_2, \dots, s_8)$ (with high probability), but we don't know $a$ nor $b$.

We can define a new sequence $T = \{t_i\}$, s.t.
```math
t_i = x_i - x_{i-1} \Rightarrow t_i = at_{i-1} \mod n
```

Note that $t_{i+1}t_{i-1} - t_i^2 = 0 \mod n$, so we can now retrieve $n$ by applying the $\gcd$ without knowing $a, b$.

### Retrieve a

Note that
```math
x_{h+2} - x_{h+1} = a(x_{h+1} - x_h)
```
So $a = (x_{h+2} - x_{h+1})(x_{h+1} - x_h)^{-1} \mod n$.

### Retrieve b

We can find $b$ by just computing $b = x_h - ax_{h-1} \mod n$.

### Retrieve secret

Once we got $n, a, b$, computing secret is trivial, since we can compute all the following $x_h$ in the sequence, starting from $x_9$, as $x_{h+1} = ax_h + b \mod n$.

$\text{secret}$ will then be the concatenation of the bytes $x_h' = x_h \mod 256$.