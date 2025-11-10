from pwn import *

HOST = "localhost" # change to the actual host
PORT = 1367 # change to the actual port

def main():
    conn = remote(HOST, PORT)

    k = 1

    conn.recvuntil(b"c2: ")
    c2 = int(conn.recvline().strip().decode())

    conn.sendline(str(-c2 + k).encode())
    conn.sendline(str(-k).encode())
    conn.recvlines(2)

    flag = conn.recvline().strip().decode()
    print(flag)

    conn.close()

if __name__ == "__main__":
    main()