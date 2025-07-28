# Garbled Row Reduction

**Challenge name**: Garbled Row Reduction\
**Category**: Implementation Techniques\
**Author**: Lorenzo Bunaj

## Challenge

This protocol implements a variant of the GRR3 AND Garbled Gate, which reduces the number of entries of the Garbled Table to 2, instead of 3.

This is made possible thanks to the introduction of two additional shares, which becomes the actual entries of the table.

The protocol performs a Lagrange Interpolation by using the three points

```math
(x_1, H(W_A^0, W_B^0)), (x_2, H(W_A^0, W_B^1)), (x_3, H(W_A^1, W_B^0))
```

with $x_1, x_2, x_3 \in \{1, 2, 3\}, x_i \not = x_j$.
The output of the interpolation is the polynomial $p_0$, which is used to find the values of the shares $s_1, s_2$ as $s_1 = p_0(5), s_2 = p_0(6)$.

Then, we use again the Lagrange Interpolation to find the coefficients of the polynomial $p_1$, by interpolating

```math
(4, H(W_A^1, W_B^1)), (5, s_1), (6, s_2)
```

So, now we have to polynomials $p_0, p_1$ s.t. $p_{b_C}$ interpolates the points corresponding to the hashes of the labels $W_A^{b_A}, W_B^{b_B}$ for which $b_A \land b_B = b_C$.

We can therefore define the output labels $W_C^{b_C} = p_{b_C}(0)$ and publish the shares $s_1, s_2$.

The parties can therefore compute $H(W_A, W_B)$ and compute the corresponding output label by interpolating the hash with the shares and evaluating the resulting polynomial in $0$.

However, there is an issue, the user doesn't know which is the correct coordinate $x$ to use in the interpolation for $(x, H(W_A, W_B))$.

The flag is encrypted using $H(W_C^0, W_C^1)$ as the secret key and in the output we have (besides the parameters used to encrypt the flag and the encrypted flag itself), the shares $s_1, s_2$ and the shuffled tuples $(W_A^0, W_A^1), (W_B^0, W_B^1)$.

## Solution

Since the tuples $(W_A^0, W_A^1), (W_B^0, W_B^1)$ are shuffled, we don't know in prior how to correctly to the interpolation to retrieve the output label. We can therefore try all the combination and check if the combination is the correct one only once we decrypted the flag and checked that it starts with "RHUL".

So let's now assume we picked the right combination and have the tuples $(W_A^0, W_A^1), (W_B^0, W_B^1)$ (not shuffled).

The server, before sending the shares $s_1, s_2$, shuffles them too. We can therefore do the same thing we did before and try all the combination.

Overall, the possible path are now 8, which is computationally doable. So let's assume we are guessed all the right combinations and continue with the challenge.

Once we know all the labels (with the corrisponding indices) and the shares. The only thing remaining is applying the same operations of the server to get both the output labels (we can do it since we have all the labels).

Once we got $W_C^0, W_C^1$, we can decrypt the flag using the first $16$ bytes of $H(W_C^0, W_C^1)$ as the key