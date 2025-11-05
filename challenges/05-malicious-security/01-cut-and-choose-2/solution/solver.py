from pwn import *
import hashlib

HOST = "localhost" # change to the actual host
PORT = 1365 # change to the actual port

CIRCUITS_NUM = 128
T = 3

def H(x, t):
    return hashlib.sha256(x).digest()[:t]

def find_collision(guess, target, inc, l):
    if len(guess) != 0 and H(guess, T) == H(target, T):
        return guess
    
    if inc == l:
        return bytes([0])

    for b in range(255):
        res = find_collision(guess + bytes([b]), target, inc + 1, l)
        if res != bytes([0]):
            return res
        
    return bytes([0])

def calculate_root(leafs):
    if len(leafs) == 2:
        return H(leafs[0] + leafs[1], T)
    
    l = len(leafs) // 2
    return H(calculate_root(leafs[:l]) + calculate_root(leafs[l:]), T)

def main():
    conn = remote(HOST, PORT)
    target = b"FLAG"
    l = 10
    guess = find_collision(b"", target, 0, l)
    print(guess)

    leafs = [H(guess, T) for _ in range(CIRCUITS_NUM)]
    R = calculate_root(leafs)
    print(R.hex().encode())

    conn.sendline(R.hex().encode())
    for _ in range(CIRCUITS_NUM):
        conn.sendline(H(guess, T).hex().encode())
    for _ in range(CIRCUITS_NUM):
        conn.sendline(guess.hex().encode())
    
    conn.sendline(target.hex().encode())
    conn.recvuntil(b"Enter the seed that you want to use:")

    flag = conn.recvline().strip().decode()
    print(flag)

if __name__ == "__main__":
    main()

