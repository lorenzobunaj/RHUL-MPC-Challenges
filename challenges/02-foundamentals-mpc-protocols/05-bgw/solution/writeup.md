# BGW Protocol

**Challenge name**: BGW Protocol\
**Category**: Foundamentals MPC Protocols\
**Author**: Lorenzo Bunaj

## Challenge

The flag is encrypted using a secret generated as the output of $F : (x, y, z) \mapsto \text{secret}$, with $x, y, z \in_R \mathbb{Z}_p$, with $p = 2^{61} - 1$ and secret defined as.

```math
\text{secret} = (x + y) \cdot (y + z) \cdot (z + x)
```

We can't compute secret directly, since only the value of $z$, but we can participate in a 3-party BGW protocol, where the other two parties $P_1, P_2$ use as inputs respectively $x, y$.

$F(x, y, z)$ is computed through the BGW protocol, using the standard BGW ADD and MUL gates.

## Solution

The server publishes the input $z$, which the user can use to participate in the protocol and evaluate $F(x, y, z)$ via BGW.

The user has:
- Compute the shares of the sums in local.
- Generate the MUL shares and send them to the other parties, according to the BGW logic.
- Implement a Lagrange Interpolation algorithm to reconstruct the output of the MUL gates from the received MUL shares.

Once the user successfully got the secret, they can send it to the server, which will use it to decrypt the flag. If the secret is wrong, random bytes will be printed.

An example of Python code which implements the Lagrange Interpolation:
```python
def modinv(a, p):
    return pow(a, -1, p)

def lagrange_coeffs(x_s, p):
    coeffs = []
    for j, xj in enumerate(x_s):
        num = 1
        denom = 1
        for m, xm in enumerate(x_s):
            if m != j:
                num = (num * (-xm)) % p
                denom = (denom * (xj - xm)) % p
        lambda_j = (num * modinv(denom, p)) % p
        coeffs.append(lambda_j)
    return coeffs

def lagrange_interpolation(self, shares):
    coeffs = lagrange_coeffs([i+1 for i in range(3)], self.p)
    s = 0
    for i in range(3):
        s += shares[i] * coeffs[i]

    return s % self.p
```