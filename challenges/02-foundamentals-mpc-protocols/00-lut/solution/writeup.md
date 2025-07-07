## Challenge

You can interact with a server which encrypts the flag $F$ in the following way:

1. It divides $F$ in 4 parts: $F[1:10], F[11:20], \dots, F[31:40]$.
2. It generates 16 secret shares, using the Shamir secret shares protocol, for each part of $F$.
3. It stores the shares in a 8x8 LUT, where each part of the flag is associated to a quadrant (e.g. the 16 shares of the $i$-th part are stored in the 16 entries of the $i$-th quadrant).
4. In general, the share at the entry $(x,y)$ is encrypted using a custom encryption protocol, based on AES CBC, which uses the key $k_{x,y}$.

The server, finally, publishes a random 3-uple $(x, y, k_{x,y})$.

The decryption is made server side, by sending $(x_0, y_0, k_{x_0,y_0})$ to decrypt the share stored at $(x_0, y_0)$.

There is also a limitation, you cannot try to decrypt the same entry twice.

## Vulnerability

The vulnerabily is that the encryption of the different shares its not independent to the position.

In particular, with a key $k_{x,y}$, you can also decrypt the shares at

```math
(x \pm 2,y \pm 1), (x \pm 1,y \mp 2), (x \pm 1,y \pm 2), (x \pm 1,y \mp 2)
```

If we see the LUT as a chess board, we could say that, if we can decrypt the share at $(x,y)$, we can also decrypt all the shares at the entries reachable by a knight move.

The only limitation is that we can access each entry only once, so we need to create a path, starting from the entry $(x,y)$ sent by the server, which covers the whole board with just knight moves. This is a basic coding problem known as Knight Tour which can be solved with just a recursive function (or with efficient, but less trivial, algorithms).

Once we got
```math
(k_{x,y}, \text{Enc}_{k_{x,y}}(\text{share}_{x,y})) \space \forall x,y < 8
```
we can decrypt the whole LUT and recover $F$ by combining the shares.