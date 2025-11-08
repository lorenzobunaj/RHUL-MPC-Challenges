import secrets, os
from utils import H, PRG
from polynomial import make_random_poly, random_coeffs

def gen_checkbit(label, bit):
    lb = bytearray(label)
    lb[-1] ^= bit
    return bytes(lb)

def setup(CIRCUITS_NUM):
    coeffs = make_random_poly(31)

    circuits = []
    commitments = []

    for i in range(CIRCUITS_NUM):
        seed = secrets.token_bytes(8)
        mask = random_coeffs(coeffs, i)

        preL0 = PRG(seed + b'0')
        L0_masked = bytes(a ^ b for a, b in zip(preL0, mask))
        L0 = gen_checkbit(L0_masked, 0)
        delta = secrets.token_bytes(16)
        L1 = gen_checkbit(bytes(a ^ b for a, b in zip(L0_masked, delta)), 1)

        wires = {'preL0': preL0.hex(), 'L0': L0.hex(), 'L1': L1.hex()}

        GC = {
            "index": i,
            "seed": seed.hex(),
            "mask": mask.hex(),
            "wires": wires
        }
        C = bytes(a ^ b for a, b in zip(H(seed + i.to_bytes(4, 'big')), mask))

        circuits.append(GC)
        commitments.append(C.hex())

    return circuits, commitments