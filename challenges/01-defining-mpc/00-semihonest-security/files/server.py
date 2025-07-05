from pwn import *
from utils import pwn_input, pwn_print
from party1 import Party1
from party2 import Party2

PORT = 1338
with open("flag.txt") as f:
    FLAG = f.read().strip().encode().hex()

def functionality(conn):
    party1 = Party1()
    party2 = Party2()

    in1 = party1.int1()
    in2 = party2.int1()
    if in2 == [1, 1]:
        in2 = [0, 0]

    pwn_print(conn, "|".join(map(str, in2)))
    
    in11 = in1[in2[0] + 2 * in2[1]]
    in12 = list(in1[3:])
    in12.pop(in2[0] + 2 * in2[1])
    in3 = [in11] + in12

    pwn_print(conn, "|".join(map(str, in3)))

    guess = int(pwn_input(conn, "Insert the product of the coefficients a, b and c: "))
    p = in1[0] * in1[1] * in1[2]

    if guess == p:
        pwn_print(conn, FLAG)

def main():
    server = listen(PORT)
    print(f"Server listening on port {PORT}")
    functionality(server)
    server.close()

if __name__ == "__main__":
    main()