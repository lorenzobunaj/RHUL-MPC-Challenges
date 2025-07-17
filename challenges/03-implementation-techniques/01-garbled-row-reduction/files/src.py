from Crypto.Random import get_random_bytes
from random import randint, shuffle
from utils import *
from lagrange import interpolate_poly, eval_poly

# with open("flag.txt") as f:
#     FLAG = f.read().strip()
FLAG = "RHUL{7w0_1s_b3773r_7h4n_7hr33_zpWin}"

def generate_wire_labels():
    b = randint(0,1)
    return [(get_random_bytes(32), b), (get_random_bytes(32), 1-b)]

def compute_H_points(Wa, Wb):
    points = {}
    for la, i in Wa:
        for lb, j in Wb:
            x = 1 + i*2 + j
            h = H(la, lb)
            points[(i, j)] = (x, h)

    return points

def garble_gate(points):
    Lc = [None] * 2

    out0_pts = [points[(0,0)], points[(0,1)], points[(1,0)]]
    p0 = interpolate_poly(out0_pts)
    Lc[0] = eval_poly(p0, 0)

    x_vals = [5, 6]
    shared_pts = []
    for x in x_vals:
        shared_pts.append((x, eval_poly(p0, x)))

    out1_pts = [points[(1,1)]]
    p1 = interpolate_poly(out1_pts + shared_pts)
    Lc[1] = eval_poly(p1, 0)

    shuffle(shared_pts)

    return shared_pts, Lc

def protocol():
    Wa = generate_wire_labels()
    Wb = generate_wire_labels()
    
    points = compute_H_points(Wa, Wb)

    shared_pts, Lc = garble_gate(points)

    secret = H(Lc[0], Lc[1])[:16]
    iv = get_random_bytes(16)
    ct = encrypt(FLAG.encode(), secret, iv)

    [(la1, _), (la2, _)] = Wa
    [(lb1, _), (lb2, _)] = Wb
    print(f"Wa: {la1}, {la2}")
    print(f"Wb: {lb1}, {lb2}")

    print("Shared points:")
    for _, y in shared_pts:
        print(y)

    print(f"iv: {iv}")
    print(f"ciphertext: {ct}")

def main():
    protocol()

if __name__ == "__main__":
    main()