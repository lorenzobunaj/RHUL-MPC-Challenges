from pwn import *
from Crypto.Random import get_random_bytes
from party import Party
from utils import *

PORT = 1345
with open("flag.txt") as f:
    FLAG = f.read().strip()

def prodsum(x : int, y : int, z : int, p : int) -> int:
    return ((x + y) * (y + z) * (x + z)) % p

def challenge(conn):
    p = pow(2, 61) - 1
    inputs = [randint(1, p), randint(1, p), randint(1, p)]
    secret = prodsum(inputs[0], inputs[1], inputs[2], p).to_bytes(16, byteorder='big')

    iv = get_random_bytes(16)
    ct = encrypt(FLAG.encode(), secret, iv)

    party1 = Party(p)
    party2 = Party(p)

    input_shares = [
        party1.generate_shares(inputs[0], 3),
        party2.generate_shares(inputs[1], 3),
        []
    ]
    for i in range(3):
        input_shares[2].append(int(pwn_input(conn, f"Share for party {i+1}: ")))
    for i in range(3):
        pwn_print(conn, f"Your share from party {i+1}: {input_shares[i][2]}")

    add_shares = [
        [party1.mul_gate(input_shares[0][i % 2], input_shares[0][(i+1) % 2]) for i in range(2)],
        [party2.add_gate(input_shares[1][i % 2], input_shares[1][(i+1) % 2]) for i in range(2)]
    ]

    mul1_public_shares = [
        [party1.public_mul_gate(add_shares[0][0], add_shares[0][1], 3)],
        [party2.public_mul_gate(add_shares[1][0], add_shares[1][1], 3)],
        []
    ]
    for i in range(3):
        mul1_public_shares[2].append(int(pwn_input(conn, f"Share for party {i+1}: ")))
    for i in range(3):
        pwn_print(conn, f"Your share from party {i+1}: {mul1_public_shares[i][2]}")
    
    mul1_shares = [
        party1.mul_gate([mul1_public_shares[i][0] for i in range(2)]),
        party1.mul_gate([mul1_public_shares[i][0] for i in range(2)])
    ]

    mul2_public_shares = [
        [party1.public_mul_gate(mul1_shares[0], add_shares[0][2], 3)],
        [party1.public_mul_gate(mul1_shares[1], add_shares[1][2], 3)],
        []
    ]
    for i in range(3):
        mul2_public_shares[2].append(int(pwn_input(conn, f"Share for party {i+1}: ")))
    for i in range(3):
        pwn_print(conn, f"Your share from party {i+1}: {mul2_public_shares[i][2]}")
    
    mul2_shares = [
        party1.mul_gate([mul2_public_shares[i][0] for i in range(2)]),
        party1.mul_gate([mul2_public_shares[i][1] for i in range(2)])
    ]
    for i in range(2):
        pwn_print(conn, f"Your share from party {i+1}: {mul2_shares[i]}")

    secret_guess = int(pwn_input(conn, "The secret: "))

    secret_guess = secret_guess.to_bytes(16, byteorder='big')
    pt = decrypt(ct, secret_guess, iv)

    print(pt)

    conn.close()

def main():
    server = listen(PORT)
    print(f"Server listening on port {PORT}")
    challenge(server)

if __name__ == "__main__":
    main()