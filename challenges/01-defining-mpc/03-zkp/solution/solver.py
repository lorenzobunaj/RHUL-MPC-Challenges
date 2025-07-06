from pwn import *
import secrets

HOST = "localhost" # change to the actual host
PORT = 1341 # change to the actual port

def main():
    conn = remote(HOST, PORT)

    g = int(conn.recvline().strip().decode())
    p = int(conn.recvline().strip().decode())
    y = int(conn.recvline().strip().decode())

    s = secrets.randbits(128)
    r = (pow(g, s, p) * pow(y, -1, p)) % p

    conn.recvline()
    conn.sendline(str(r).encode())
    conn.recvline()
    conn.sendline(str(s).encode())
    

    flag = conn.recvline().strip().decode()
    print(flag)

    conn.close()

if __name__ == "__main__":
    main()