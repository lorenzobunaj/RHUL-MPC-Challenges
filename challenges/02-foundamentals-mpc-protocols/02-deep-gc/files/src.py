from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad
from utils import xor, H

with open("flag.txt") as f:
    FLAG = f.read().strip()

secret = get_random_bytes(16)
iv = get_random_bytes(16)

cipher = AES.new(secret, AES.MODE_CBC, iv)
ct = cipher.encrypt(pad(FLAG.encode(), AES.block_size))

operations = ['AND', 'NOR']
def compute(a, b, op):
    if op == 'AND':
        return a * b
    elif op == 'NOR':
        return (1-a) * (1-b)

def garble_gate(Wa, Wb, x, y):
    op = operations[(x + y) % 2]

    Lc = [get_random_bytes(32), bytes([0] * 31 + [secret[4 * x + y]])]

    table = [None] * 4
    for a in [0, 1]:
        for b in [0, 1]:
            La, pa = Wa[a]
            Lb, pb = Wb[b]

            pc = compute(pa, pb, op)
            ct = xor(H(La, Lb), Lc[pc])
            table[2*a + b] = (ct, pc)

    return table

def garble_circuit(wires):
    gates = []

    for x in range(4):
        for y in range(4):
            gates.append(garble_gate(wires[y], wires[(y+1) % 4], x, y))

        for y in range(4):
            w0 = None
            w1 = None
            for ct, p in gates[4 * x + y]:
                if w0 is not None and w1 is not None:
                    break
                if p == 0 and w0 is None:
                    w0 = (ct, 0)
                elif p == 1 and w1 is None:
                    w1 = (ct, 1)
            
            wires[y] = [w0, w1]

    return gates
        

def protocol():
    wires = []
    for _ in range(4):
        wires.append([
            (get_random_bytes(32), 0),
            (get_random_bytes(32), 1)
        ])
    
    gates = garble_circuit(wires)

    print("wires:\n" + str(wires))
    print("gates:\n" + str(gates))
    print(f"iv: {iv.hex()}")
    print(f"ciphertext: {ct.hex()}")

def main():
    protocol()

if __name__ == "__main__":
    main()