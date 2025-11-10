# SPDZ

**Challenge name**: SPDZ\
**Category**: Malicious Security\
**Author**: Lorenzo Bunaj

## Challenge

This challenge is simulating a 3-party protocol where $P_1$ is represented by the player, $P_2$ is another party the player wants a secret sharing with and $P_3 = S$ is a trusted server who is acting as the dealer of the secret parameters.

The secret sharing is computed with SPDZ authentication and the protocol works in the following way:
* $S$ computes a secret $\Delta = \Delta_1 + \Delta_2$ and sends $\Delta_1$ to $P_1$ and $\Delta_2$ to $P_2$.
* $P_2$ and $P_1$ send their inputs $x_1, x_2$ to $S$ and they both compute $x = x_1 + x_2$.
* $S$ computes $t_1, t_2$ s.t. $\Delta x = t_1 + t_2$ and sends $t_i$ to $P_i$.
* Each party $P_i$ can now compute their commitment $\Delta_i x - t_i$ and send them to each other.
* $P_2$ (server side) checks if the commitment is honest. If not, they abort the protocol.

$P_2$ then colludes with $S$ to get $t_1$ and, if the player was honest, is able to retrieve $\Delta x = (\Delta x)_2$.

Finally, the player can send a message $k$ and if $k + (\Delta x)_2 = \Delta x \mod p$, with $p \nmid k$, the flag is printed.

## Solution

To understand the vulnerability, we have to look at the code and see how $(\Delta x)_2$ is computed.

If the player is honest, his commitment $c_1 = \Delta_1 x - t_1$, and therefore $P_2$ retrieve $\Delta_x$, having $t_1$, as $c_1 + t_1 + \Delta_2 x = \Delta x$.

So, if the check was doing correctly on $c_1$, getting the flag would not be possible. However, there are two main problems in the implementation:
* The commitment $c_2$ is sent before $c_1$, so the player can use it to forge a malicious payload.
* The check on $c_1$ is only making sure that
```math
\begin{aligned}
    c_1 &\not = \Delta_1 x - t_1 + kp \ \ \ \forall k \\
    c_1 &\not = kp \ \ \ \forall k
\end{aligned}
```

So, $P_1$ can send a malicious payload $c_1' = -c_2 + k$, for some $k$ s.t. $p \nmid k$, this way $P_2$ will calculate
```math
\begin{aligned}
    (\Delta x)_2 &= \\
    &= c_1' + t_1 + \Delta_2 x \\
    &= -\Delta_2 x + t_2 + k + t_1 + \Delta_2 x \\
    &= t_1 + t_2 + k \\
    &= \Delta x + k
\end{aligned}
```

And $P_1$ can therefore send $-k$ as his message and pass the check to get the flag.