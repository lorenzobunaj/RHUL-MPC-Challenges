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

    secret_bits = []
    for b in s1:
        conn.sendline(b"1")
        conn.recvuntil(b"Your input: \n")
        conn.sendline(b)
        b_oprf = conn.recvline().strip()

        if b_oprf in stash:
            secret_bits.append(1)
            continue
        
        conn.sendline(b"2")
        conn.recvuntil(b"Your input: \n")
        conn.sendline(b_oprf)
        
        if conn.recvline().strip() == b'found':
            secret_bits.append(1)
            continue
        
        secret_bits.append(0)

    secret_frames = []
    for i in range(len(secret_bits)):
        if secret_bits[i] == 1:
            secret_frames.append(s1[i])

    secret_frames.sort(key=lambda el: el[-1])
    secret_frames = [sf[:-1] for sf in secret_frames]

    secret = b""
    for sf in secret_frames:
        secret += sf

    conn.sendline(b"4")
    conn.sendline(secret)

    conn.recvuntil(b"Flag: ")

    flag = bytes.fromhex(conn.recvline().strip().decode())
    print(flag)

    conn.close()

if __name__ == "__main__":
    main()