## Challenge

The flag is encrypted using a secret generated as the output of $C : (x, y) \mapsto \text{secret}$, with $x, y \in_R [0, 255]^{16 \cdot 4}$ and secret defined as.

```math
\text{secret} = (t_1 \land t_2) \oplus (t_3 \oplus t_4)
```

where $t_i = x_i \oplus y_i$ if $i \not = 4$ and $t_4 = x_4 \land y_4$, s.t.

```math
x_i = x[16i : 16(i+1)] \\
y_i = y[16i : 16(i+1)]
```

After the encryption, the server participates in a GMW protocol with the user where $C$ is evaluated using shares and GMW XOR, NOT and AND gates, using $x$ and $y$ as inputs.
The shares are defined as:
```math
\begin{cases}
    x = s_x \oplus r_x \\
    y = s_y \oplus r_y
\end{cases}
```
with $r_i \in_R [0, 255]^{16}$.

At the end of the protocol, the server takes the final share from the user and XORs it with its final share, and use the result to decrypt the encrypted flag.

If the two shares are correct, the server will output the original flag.

## Vulnerability

The server publishes the input shares $r_x, s_y$, which the user can use to evaluate $C$ via GMW.

The user has to evaluate the XOR and NOT gates in local and participate in the communication with the server to evaluate the AND gates. Finally, he will obtain the secret share to send to the server to execute the decryption correctly.