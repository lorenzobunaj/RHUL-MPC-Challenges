## Protocol
You are $P_B$ and have to interact with $P_A$, with the intermediation of a trusted party $\mathcal{F}$.

1) $P_A$ sends $\{(m_0^0, m_1^0), (m_0^1, m_1^1), \dots, (m_0^n, m_1^n)\}$ to $\mathcal{F}$.

    Considering the pair $(m_0^k, m_1^k)$, one is the $k$-th character of the flag and other one is just a random byte, with the following logic:

    ```math
    m_{1 - \sin(k\pi/2)}^k = \text{flag}[k]
    ```

2) $P_B$ sends $\{b_0, b_1, \dots, b_n\}$ to $\mathcal{F}$.

3) $\mathcal{F}$ sends $\{m^0_{b_0}, m^1_{b_1}, \dots, m^n_{b_n}\}$ to $P_B$.

## Vulnerability

The vulnerability lies in the fact that we know, for all the pairs $(m_0^k, m_1^k)$, the position of the flag character based on $k$.

We can therefore build our input as:
```math
b_k' = 1 - \sin(k\pi/2) \space \forall k \in [n]
```
to reconstruct the flag.