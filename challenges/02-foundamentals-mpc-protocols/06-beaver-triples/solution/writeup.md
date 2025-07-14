# Beaver Triples

**Challenge name**: Beaver Triples\
**Category**: Foundamentals MPC Protocols\
**Author**: Lorenzo Bunaj

## Challenge

You are party $P_1$ in a protocol where the server plays the role of party $P_2$. Precisely, the server  knows all the parameters and could run the protocol just by itself, but from the user perspective, this is unsignificant, since the server behaves like it knows just the view of $P_2$.

First, the parameters $x, y, a, b \in_R \mathbb{Z}_p$ s.t. $p = 65537$ and $c$ is computed as $c = ab$.

The flag is encrypted as $\text{Enc}_{\text{key}}(\text{flag})$, where the key is rapresented by the first 16 bytes of $\text{Sha256}(xy)$.

Then, the server generates the shares for all the parameters ($(a_1, a_2), (b_1, b_2), \dots$) using the same algorithm used in GMW, where are generated $1$-degree random polynomials $r$ s.t. $r(0) = \text{share}$.

Each share is then again divided into 15 XOR-shares, the XOR-shares generated from $\lambda_2$ (we will refer to a generic parameter using $\lambda$ for simplicity) are kept by $P_2$.

$P_1$ (the user) receives

```math
\text{Shuffle}(\{R\} \cup \{(a_{1,i}, b_{1,i}, c_{1,i}, x_{1,i}, y_{1,i})\}_{i \in [15]})
````
where $\lambda_{i,1}$ is the $i$-th XOR-share of $\lambda_1$ and $R \in_R \mathbb{Z}_p^5$.

$P_2$ then reconstruct each $\lambda_2$ from the XOR-shares, calculates its own shares of $d$ and $e$ as $d_2 = x_2 - a_2$ and $e_2 = y_2 - b_2$ and send them to $P_1$.

He awaits for $P_1$'s shares $d_1, e_1$ and use them to reconstruct the original $d, e$ using Lagrange Interpolation (since the shares generation is following the GMW logic).

Once $P_2$ got $d$ and $e$, he can use them to compute its share of $xy$, using Beaver Algorithm, and send it to $P_1$.

$P_1$ has to compute the original value of $xy$ and use it to get the secret, which will have to send to the server to decrypt the flag.

For each new $(d, e)$, $P_1$ has 10 possibilities to decrypt the flag using different inputs.

## Solution

First, we need to find the right shares $\lambda_1$ starting from the XOR-shares sent by $P_2$. This is mostly a matter of luck, since the list of XOR-shares is shuffled with a random tuple, so, for each try, we have $1/15$ possibilities of guessing the right list of shares. Considering we have $10$ possibilities to decrypt the flag, for every execution of the solver, we have probability of $2/3$ of getting the flag.

This said, let's assume we guessed the right list of XOR-shares and successfully retrieved $(a_1, b_1, c_1, x_1, y_1)$.

We can calculate $d_1 = x_1 - a_1$ and $e_1 = y_1 - b_1$ and, using the values $d_2, e_2$ received from $P_2$, compute

```math
d = \text{LagrangeInterpolate}(d_1, d_2)\\
e = \text{LagrangeInterpolate}(e_1, e_2)
```

where $\text{LagrangeInterpolate}$ executes the Lagrange Interpolation on two shares.

Once we got $d, e$, we can use them to calculate our share of $xy$ using the Beaver Algorithm:

```math
(xy)_1 = de + db_1 + ea_1 + c_1
```

Finally, we can compute the final product as $xy = \text{LagrangeInterpolate}((xy)_1, (xy)_2)$.

Being finally able to get the secret and send it to the server to decrypt the flag.