from pwn import *
from Crypto.PublicKey import RSA

HOST = "localhost" # change to the actual host
PORT = 1347 # change to the actual port

def main():
    conn = remote(HOST, PORT)

    k1 = RSA.generate(1024)
    k2 = RSA.generate(1024, e = 257)

    conn.sendline(str(k1.n).encode())
    conn.sendline(str(k1.e).encode())
    conn.sendline(str(k2.n).encode())
    conn.sendline(str(k2.e).encode())

    conn.recvuntil(b"c2: ")
    c2 = int(conn.recvline().strip().decode())

    flag = pow(c2, k2.d, k2.n).to_bytes(46, "big")
    print(flag)

    conn.close()

if __name__ == "__main__":
    main()