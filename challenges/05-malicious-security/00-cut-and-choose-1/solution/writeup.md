# Cut And Choose 1

**Challenge name**: Cut And Choose 1\
**Category**: Malicious Security\
**Author**: Lorenzo Bunaj

## Challenge

This challenge implements a basic protocol where the user can send 20 elements $a_1, \dots, a_{20}$. The server choose only 10 of these (according the the cut-and-choose technique) and feed them to be checked to $P_1$. $P_1$ compares each chosen element $a'_i + f_j$ to the its modulo 256 reduction, where $f_j$ is the $j$-th of the $P_1$'s input setup, which is the flag, if they are not the same, aborts.

## Solution

The protocol is not secure against selective abort attacks, the user $P_2$ will therefore need to exploit this vulnerability.

For the generic flag byte $f_j$, $P_2$ can send 20 equal elements $a_k^*, \dots, a_k^*$, where $k$ indicates the iteration, starting from $a^*_1 = 0$. Thus, by checking if the protocol aborted at each step, we can find $w$ s.t.

```math
a^*_w \rightarrow \text{protocol works}\\
a^*_{w+1} \rightarrow \text{protocol aborts}
```

that means $f_j + a^*_{w+1} = f_j + w + 2 = 0 \mod 256 \Rightarrow f_j + w + 2 = 256 \Rightarrow f_j = 254 - w$, and we can retrieve $f_j$.

By making sure our solver flow is always aligned with the server one, we can apply this technique to retrieve the entire flag $f$.
