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

def garble_gate(Wa, Wb):
    Lc = [get_random_bytes(32), bytes([0] * 16) + secret]

    table = [None] * 4
    for a in [0, 1]:
        for b in [0, 1]:
            La, pa = Wa[a]
            Lb, pb = Wb[b]

            pc = pa * pb
            ct = xor(H(La, Lb), Lc[pc])
        
            table[2 * pa + pb] = ct

    return table

def protocol():
    wires = []
    for _ in range(2):
        b = randint(0,1)
        wires.append([
            (get_random_bytes(32), b),
            (get_random_bytes(32), 1-b)
        ])
    
    gate = garble_gate(wires[0], wires[1])

    with open("output.txt", "w") as f:
        f.write("wires:\n" + str(wires) + "\n")
        f.write("garbled gate:\n" + str(gate) + "\n")
        f.write(f"iv: {iv.hex()}\n")
        f.write(f"ciphertext: {ct.hex()}\n")

def main():
    protocol()

if __name__ == "__main__":
    main()