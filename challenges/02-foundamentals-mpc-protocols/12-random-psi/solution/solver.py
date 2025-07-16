from pwn import *
from sympy import gcd

HOST = "localhost" # change to the actual host
PORT = 1353 # change to the actual port

def compute_secret(x):
    secret = b""
    t = []
    s = []

    for i in range(len(x) - 1):
        t.append(x[i+1] - x[i])

    for i in range(len(x) - 2):
        s.append(t[i]*t[i-2] - pow(t[i], 2))

    n = s[0]
    for i in range(len(s)):
        n = gcd(n, s[i])

    a = ((x[2] - x[1]) * pow(x[1] - x[0], -1, n)) % n

    b = (x[1] - a * x[0]) % n

    x = x[-1]
    for _ in range(16):
        x = (a*x + b) % n
        secret += bytes([x % 256])

    return secret


def main():
    conn = remote(HOST, PORT)

    s1 = []
    conn.recvuntil(b"S1:\n")
    for _ in range(40):
        s1.append(conn.recvline().strip())

    stash = []
    conn.sendline(b"3")
    conn.recvuntil(b"Your choice: \n")
    
    sl = int(conn.recvline().strip().decode())
    for _ in range(sl):
        stash.append(conn.recvline().strip())

    public_bits = []
    for b in s1:
        conn.sendline(b"1")
        conn.recvuntil(b"Your input: \n")
        conn.sendline(b)
        b_oprf = conn.recvline().strip()

        if b_oprf in stash:
            public_bits.append(1)
            continue
        
        conn.sendline(b"2")
        conn.recvuntil(b"Your input: \n")
        conn.sendline(b_oprf)
        
        if conn.recvline().strip() == b'found':
            public_bits.append(1)
            continue
        
        public_bits.append(0)

    public_frames = []
    for i in range(len(public_bits)):
        if public_bits[i] == 1:
            public_frames.append(s1[i])

    public_frames.sort(key=lambda el: el[-1])
    public_frames = [sf[:-1] for sf in public_frames]

    public = b""
    for sf in public_frames:
        public += sf

    public = bytes.fromhex(public.decode())
    x = [public[i] + 256*public[i+1] for i in range(0, 16, 2)]
    
    secret = compute_secret(x)
    

    conn.close()

if __name__ == "__main__":
    main()