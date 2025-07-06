from pwn import *
from utils import pwn_input, pwn_print
from party1 import Party1

PORT = 1340
with open("flag.txt") as f:
    FLAG = f.read().strip()

def ot_functionality(conn):
    party1 = Party1(FLAG)

    messages = party1.generateMessages()

    choice_bits = []
    for _ in range(len(messages)):
        bit = int(pwn_input(conn, "Enter the next choice bit: "))
        if bit not in [0,1]:
            return
        choice_bits.append(bit)

    for (i, b) in enumerate(choice_bits):
        pwn_print(conn, str(messages[i][b]))

    conn.close()

def main():
    server = listen(PORT)
    print(f"Server listening on port {PORT}")
    ot_functionality(server)

if __name__ == "__main__":
    main()