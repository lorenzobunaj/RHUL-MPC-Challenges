from pwn import *

HOST = "localhost" # change to the actual host
PORT = 1352 # change to the actual port

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
    
    print(x)

    conn.close()

if __name__ == "__main__":
    main()