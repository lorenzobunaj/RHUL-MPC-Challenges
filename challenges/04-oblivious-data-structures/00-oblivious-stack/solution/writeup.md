# Intro to Obliv-C

**Challenge name**: Oblivious Stack\
**Category**: Oblivious Stack\
**Author**: Lorenzo Bunaj

## Challenge

This challenge implements an Oblivious Stack Data Structure in Python and provides an interface to the user which can be used to either conditional push an element or normally pop one from the stack.

To store the elements is used an array $m$ of length $2*c$, where $c$ is the capacity of the stack. In particular, the first half of the array is used to actually store the elements. The second half is used to store only those elements for which the conditional bit $p = 1$ and all those that the user try to push while the stack is full.

An important feature is that the first half of the internal array behaves correctly like a stack, while the second half behaves like a queue.

The operations are implemented in the following way, where $\text{size}$ is initialized as $0$:
- $\text{CondPush}(v)$:
    - Sample $p \in_R \{0, 1\}$
    - If $\text{size} < c$:
        - $m.\text{append}((v, p))$
        - If $p = 1$: $m[c:].\text{QueuePush}(v)$
        - $\text{size} = \text{size} + 1$
    - Else:
        - $m[c:].\text{QueuePush}(v)$
- $\text{Pop}()$:
    - $\text{size} = \text{size} - 1$
    - Return $m[\text{size} + 1]$

The stack is initialized by the server by pushing $100$ random elements (between $0$ and $255$, so they can be interpreted as bytes) and then the $16$ bytes of $\text{secret}$, used to encrypt the flag. After this operations, it empty the first half of the array.

The last limitation is that we can only $\text{Pop}$ an initial limit of 16 elements and after each $\text{Push}$ operation this limit increases to an upper bound of $48$.

## Solution

The vulnerability is in the implementation of $\text{Pop}$, which as two problems:
- It's not implemented in a conditional way (like $\text{Push}$), so it will act in the same way to the elements with $p = 0$ and to those with $p = 1$
- It doesn't check if the first half of the array is empty, so we can use it to retrieve the elements of the second half by using $\text{Pop}$ on empty $m$.

Let's take a look to the content of the stack right after the server initialization:
```math
\text{32 empty cells} \space|\space \text{16 secret bytes} \space|\space \text{16 random bytes} 
```

If the push wasn't conditional, we could push 48 zeros bytes to have
```math
0 \dots 0 \space|\space \text{16 secret bytes}
```

and retrieve the secret by applying $\text{Pop}$ 48 times.

However, since likely not all the elements we will push will have $p = 1$, not all of them will also be pushed on the second half of the array to make the secret bytes shift. So we need to push more elements to have $p = 1$ a number of times $\ge 16$. At the same time, we need to choose carefully the number of push operations, to also have $\le 16$ times $p = 1$.

$p$ it's always choosen randomly, so the best approach we can use is to apply the push operation the number of times which maximize the probability of having $p = 1$ exactly 16 times. So, according to the Binomial Distribution, we need to push $32$ zeros bytes.

With good probability, the last 16 entries of the second half the array will contain 15 out of 16 secret bytes. Once we now these, we can bruteforce 512 bytes (256 options before and 256 after), to retrieve the correct $\text{secret}$.