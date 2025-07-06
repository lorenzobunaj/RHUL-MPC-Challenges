from pwn import *
from utils import pwn_input, pwn_print
from party1 import Party1

PORT = 1341
with open("flag.txt") as f:
    FLAG = f.read().strip()

def challenge(conn):
    party1 = Party1(FLAG)

    [g, p, y] = party1.parameters()

    pwn_print(conn, str(g))
    pwn_print(conn, str(p))
    pwn_print(conn, str(y))

    try:
        r = int(pwn_input(conn, "r: "))
        s = int(pwn_input(conn, "s: "))
    except:
        pwn_print("r, s not valid")
        conn.close()
        return 
    
    pwn_print(conn, party1.verify(r, s))

    conn.close()

def main():
    server = listen(PORT)
    print(f"Server listening on port {PORT}")
    challenge(server)

if __name__ == "__main__":
    main()