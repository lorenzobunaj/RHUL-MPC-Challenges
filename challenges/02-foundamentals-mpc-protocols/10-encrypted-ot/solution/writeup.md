# Encrypted OT

**Challenge name**: Encrypted OT\
**Category**: Foundamentals MPC Protocols\
**Author**: Lorenzo Bunaj

## Challenge

This challenge implements a protocol very similar to the one of the challenge "Optimized OT", with a small (but game-changing) added feature.

The user doesn't have to send the $T, U$ columns, but the rows instead. This is because the server, before computing the matrix $Q$ and passing it to $S$, performs same cryptographic operations on the rows of $T$.

For each row $\bold{t}_j$ of $T$, the server parse $r \in_R \mathbb{Z}_{256}^{16}$ and performs:

```math
\bold{t}_j \leftarrow \text{Enc}_k(\bold{t}_j \oplus r)
````

and then

```math
\bold{t}_j \leftarrow 
\begin{cases}
    \text{Dec}_k(\bold{t}_j) \oplus r &\text{if } \bold{t}_j[0] < 50\\
    \text{Enc}_k(\bold{t}_j) \oplus r &\text{otherwise}
\end{cases}
```

which corresponds to the following assignment

```math
\bold{t}_j \leftarrow 
\begin{cases}
    \bold{t}_j &\text{if } \text{Enc}_k(\bold{t}_j)[0] < 50\\
    \text{Enc}_k(\text{Enc}_k(\bold{t}_j \oplus r)) \oplus r &\text{otherwise}
\end{cases}
```

Where the key $k$ for each row is chosen by the user and the encryption protocol used is DES is ECB mode.

## Solution

We will just focus on the new encryption step, while ignoring the rest of the protocol, since the solution was already illustrated in the writeup for the challenge "Optimized OT".

Looking at encryption output, if, for some kind of luck, the $\text{Dec}$ and $\text{Enc}$ had the same behavior (which means $\text{Enc}$ would be its own inverse function) we would have

```math
\text{Enc}_k(\text{Enc}_k(\bold{t}_j \oplus r)) \oplus r = (\bold{t}_j \oplus r) \oplus r = \bold{t}_j
```

Let's now pay attention on the type of encryption used: DES (Data Encryption Standard). It's well know that for this protocol exists some key values for which the property $\text{Enc} = \text{Dec}$ holds. As example

```math
k = \text{0x0101010101010101}
```

We can therefore send the same weak key for each row and make the protocol have the same behavior of a standard IKNP OT, which we already discussed about in the previous challenge.