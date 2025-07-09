from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad
from random import randint
from utils import xor, H

with open("flag.txt") as f:
    FLAG_CONTENT = f.read().strip()
FLAG = "RHUL{" + FLAG_CONTENT + "}"

secret = get_random_bytes(16)
iv = get_random_bytes(16)

cipher = AES.new(secret, AES.MODE_CBC, iv)
ct = cipher.encrypt(pad(FLAG_CONTENT.encode(), AES.block_size))

operations = ['AND', 'NOR', 'NAND', 'XOR']
def compute(a, b, op):
    res = None
    if op == 'AND':
        res = a & b
    elif op == 'NOR':
        res = not (a | b)
    elif op == 'NAND':
        res = not (a & b)
    elif op == 'XOR':
        res = a ^ b

    return int(res)

def garble_gate(Wa, Wb, x, y):
    Lc = [get_random_bytes(32), bytes([0] * 31 + [secret[4 * x + y]])]
    op = operations[(x + y) % 4]

    table = [None] * 4
    for a in [0, 1]:
        for b in [0, 1]:
            La, pa = Wa[a]
            Lb, pb = Wb[b]

            pc = compute(pa, pb, op)
            ct = xor(H(La, Lb), Lc[pc])
        
            table[2 * pa + pb] = ct

    return Lc, table

def garble_circuit(ws):
    wires = ws
    gates = []

    new_wires = None
    for x in range(4):
        gates.append([])
        new_wires = []
        for y in range(4):
            Lc, table = garble_gate(wires[y], wires[(y+1) % 4], x, y)

            gates[x].append(table)
            new_wires.append([
                (Lc[0], 0),
                (Lc[1], 1)
            ])

        wires = [w for w in new_wires]

    return gates

def protocol():
    wires = []
    for _ in range(4):
        b = randint(0,1)
        wires.append([
            (get_random_bytes(32), b),
            (get_random_bytes(32), 1-b)
        ])
    
    gates = garble_circuit(wires)

    print("wires:\n" + str(wires) + "\n")
    print("gates:\n" + str(gates) + "\n")
    print(f"iv: {iv.hex()}\n")
    print(f"ciphertext: {ct.hex()}\n")

def main():
    protocol()

if __name__ == "__main__":
    main()