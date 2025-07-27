# Mixed Protocols

**Challenge name**: Mixed Protocols\
**Category**: Implementation Techniques\
**Author**: Lorenzo Bunaj

## Challenge

This challenge implements a 2-party mixed protocol, which put together additional homomorphic encryption (AHE) and Yao garbled circuits (GC). We will refer to the server as $P_2$ and to the player as $P_1$.
The intended protocol logic is the following:
- $P_1$ compute $(sk, pk) \leftarrow \text{Pailler.GenKeys}()$ and send $pk$ to $P_2$.
- $P_2$ generates a secret $k$ and a random word $r$. Encrypt them both using $\text{Pailler.Enc}_{pk}$ and send the sum $s_{\text{enc}} = \text{Pailler.Enc}_{pk}(k) + \text{Pailler.Enc}_{pk}(r)$ to $P_1$.
- $P_1$ decrypt $s_{\text{enc}}$ using $\text{Pailler.Enc}_{sk}$ and gets $s$.

If the player followed the intended flow, now $P_1$ holds $s = k + r$ and $P_2$ holds $r$.

The two parties can now interact in a GMW protocol to compute $k$ as $s - r$.

At the end of it, $P_2$ publishes its share of $k$ ($k_2$) and $P_1$ can compute $k = k_1 \oplus k_2$.

The flag is encrypted by the server using $k$ as the secret key, and the encryption parameters, together with the ciphertext, are public. So, once the player knows $k$, he can decrypt the flag correctly.

## Solution

There are no real vulnerabilites in the protocol, since the player can get the flag by just following the intended logic.

The challenge is therefore just to understand which the correct flow is and be able to send the correct inputs to the server.

In the first place, infact, the player needs to understand the properties of $\text{Pailler}$ algorithm and understand that $\text{Pailler.Enc}_{pk}(k) + \text{Pailler.Enc}_{pk}(r) = \text{Pailler.Enc}_{pk}(k + r)$ (since it's an AHE algorithm), so, once he got $s_{\text{enc}}$, he can compute $k + r$ using directly $\text{Pailler.Dec}_{pk}(s)$.

Once each party has its own correct input for the GC protocol. The player needs to:
- Send its shares of $k + r$ and receive the shares of $r$
- Apply a correct buffer, since the summation could have created an overflow, so we need to patch the shares to $17$ bytes instead of the original $16$.
- Compute the negated share of $r$, since we need to substract it but the GMW NOT gate is not originally implemented by the server.
- Implement the logic to evaluate the sum of $k+r$ and $-r$ via Ripple-Carry Adder circuit.

At the end of the protocol, if the logic was implemented as intended, you will get the correct share $k_2$ from the server and you will have computed the correct share $k_1$, being able to calculate $k = k_1 \oplus k_2$ and decrypt the flag.

An example of GMW Ripple-Carry Adder implementation in Python 3.12 is
```python
def gmw_and(conn, a, b):
    for i in range(4):
        sx = i // 2
        ry = i % 2
        conn.sendline(str(0 ^ ((sx ^ a) & (ry ^ b))).encode())

def gmw_full_adder(conn, a, b, cin):
    s = a ^ b ^ cin
    cout = 0
    gmw_and(conn, a, b)
    gmw_and(conn, a, cin)
    gmw_and(conn, b, cin)

    return s, cout

res = []
cin = 0
for i in range(len(sy_bits) - 1, -1, -1):
    s, cin = gmw_full_adder(conn, rx_bits[i], sy_bits[i], cin)
    res.insert(0, s)
```