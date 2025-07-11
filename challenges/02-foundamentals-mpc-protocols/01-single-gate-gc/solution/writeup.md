# Garbled Gates

**Challenge name**: Garbled Gates\
**Category**: Foundamentals MPC Protocols\
**Author**: Lorenzo Bunaj

## Challenge

This challenge implements an AND GG (garbled gate), where the secret used to encrypt the flag is encrypted as the label $L_{\text{out}}^1$.

## Solution

The server publishes, together with the needed parameters to decrypt the flag via AES-CBC, the wires

```math 
W_A = \{(L_A^{v_0}, p_A^{v_0}), (L_A^{v_1}, p_A^{v_1})\}\\
W_B = \{(L_B^{v_0}, p_B^{v_0}), (L_B^{v_1}, p_B^{v_1})\}
```

we therefore have the data to potentially decrypt the whole GG.

We can then calculate $L_{\text{out}}^1$ and use it to decrypt the flag. We will additionally need to include the flag in "RHUL{" and "}".