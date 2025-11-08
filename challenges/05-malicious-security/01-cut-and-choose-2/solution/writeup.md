# Cut And Choose 2

**Challenge name**: Cut And Choose 2\
**Category**: Malicious Security\
**Author**: Lorenzo Bunaj

## Challenge

This challenge implements a Cut-and-Choose prototype, where the player needs to send $128$ commitments.

The server then ask to open all of them + the merkle root to fully check the honesty of the player. If any of them is not matching with the previously sent commit or the seed is "FLAG", the protocol is interrupted.

After the server made sure the player is honest, he asks them to send the seed he wants to use.

$S$ checks the seed is among the ones already submitted, and, if this is true, it used to evaluate the circuit $C$, which outputs the flag if $\mathrm{seed} = \mathrm{FLAG}$ and $H(\mathrm{seed})$ otherwise.

## Solution

The vulnerability lies in the fact that the hash function $H$ to derive the leaf tag from the seed is truncated on the first $3$ bytes and the check for $\mathrm{FLAG}$ is not being made on the leafs, but on the seeds.

We can therefore first compute $H(\mathrm{FLAG})$ and then find a seed $s$ s.t. $H(s) = H(\mathrm{FLAG})$. This is easily done, since $H$ is not collision resistant.

We will use $s$, together with other $127$ random seeds, for the whole protocol, until the final step, so that the server will not abort.

Once $S$ asks to choose a $\mathrm{seed}$ to use, we can send $\mathrm{FLAG}$. This will in fact result as an already submitted leaf, equal to $H(s)$ and will be evaluated by the server, which will finally print the flag.