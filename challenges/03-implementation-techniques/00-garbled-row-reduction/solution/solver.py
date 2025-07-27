import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from sympy import Matrix

Wa = [b'\x10u\xdf\x97\x01\xeee\xb9\xf7\x1e\x1f*\xaetZ\\e\x8fM\xe6\xae\xa4\xac\x7f$i\x9cD\xe6A\xe4\x17', b'\xbe-o,\x1df\xbd\x8d\x1e\xffi\xd5-P\x7fRp6$\x04\xa8\x9dP\x06\\\xca9\xbe\xbd\xda?3']
Wb = [b'\x7f\xcb;\xed\x95\xae*\xf4\x03"c\xd2` w\x8a\xf9\x99}\x9f\xb9\xe7$\x88L\\\xedZ}>\xba\xbc', b'\xcc\xc3\x85h\x1c&2\x93\x19\xc1\xe3f\xed\x85\xbe\x1d\xe7\x9f\x17@5P\xf8\xc9\xb1\x14\xd0\xf2\r\xe4\xb3\x0c']
s = [b'A&\xf47\xc0\xb8\x91\xad2te\xa48CE\x9a\xe5\xbb\xb4t]/n\x159\xe6\x1e\xa0\x9e(\xdfX', b'\xb1o\x1a\x99\xf2\x8e7\x82\xbd\x02\xba|\xc2\x03d\xe1\x86\xa1\xd4\xf2\x9c\x9f\x88\x98\xe5*\xee^Ys\x84\xe8']
iv = b'q\xe2\xe2\x18\x8b\x8a\x0e\xf9\n*Vl\xe6\xaa\xcd\x81'
ct = b'<\x7f\xed\x9c\xd8BK33\xe0!\xc9q\xac\x16\xdd\x13\x9c\x862\xf7\x05\xa7\x1a\xc2\xb9D8\x87\xe6\xbfW\x1d\xe5\xe1\xf2=\x14"\x0e\xee/s\xfb\xba\x11\xdb\xa1'

def H(label1: bytes, label2: bytes) -> bytes:
    return hashlib.sha256(label1 + label2).digest()

def decrypt(ct, secret, iv):
    cipher = AES.new(secret, AES.MODE_CBC, iv)

    return cipher.decrypt(ct)

def compute_H_points(Wa, Wb):
    points = {}
    for la, i in Wa:
        for lb, j in Wb:
            x = 1 + i*2 + j
            h = H(la, lb)
            points[(i, j)] = (x, h)

    return points

def solve_lagrange(xs, ys):
    A = Matrix([
        [1, xs[0], xs[0]**2],
        [1, xs[1], xs[1]**2],
        [1, xs[2], xs[2]**2]
    ])

    b = Matrix(ys)
    coeffs = A.inv_mod(251) * b

    return tuple(int(c) % 251 for c in coeffs)

def interpolate_poly(points):
    assert len(points) == 3

    xs = [x for x, _ in points]
    ys = [y for _, y in points]

    coeffs = []

    for byte_index in range(32):
        y_vals = [y[byte_index] for y in ys]
        c0, c1, c2 = solve_lagrange(xs, y_vals)
        coeffs.append(bytes([c0, c1, c2]))

    # c0(x^0), c1(x^1), c2(x^2)
    c0 = bytes([b[0] for b in coeffs])
    c1 = bytes([b[1] for b in coeffs])
    c2 = bytes([b[2] for b in coeffs])
    return [c0, c1, c2]

def eval_poly(coeffs, x0):
    [c0, c1, c2] = coeffs

    y0 = []
    for byte_index in range(32): 
        y0.append((c0[byte_index] + c1[byte_index] * x0 + c2[byte_index] * (x0 ** 2)) % 251)

    return bytes(y0)

def has_equal_values(h, n):
    for i in range(len(h)):
        cnt = 0
        for j in range(len(h)):
            if i != j and h[i] == h[j]:
                cnt += 1
        if cnt == n-1:
            return True 
        
    return False

def main():
    for i in range(2):
        for j in range(2):
            wa = [(Wa[0], i), (Wa[1], 1-i)]
            wb = [(Wb[0], j), (Wb[1], 1-j)]

            points = compute_H_points(wa, wb)

            h = [[], []]
            for s_index in range(2):
                for k in range(2):
                    for q in range(2):
                        h[s_index].append(eval_poly(interpolate_poly([points[(k, q)], (5, s[s_index]), (6, s[1-s_index])]), 0))
        
                if has_equal_values(h[s_index], 3):
                    Lc0 = h[s_index][0]
                    for l in h[s_index]:
                        if l != Lc0:
                            Lc1 = l
                            break 

                    print(decrypt(ct, H(Lc0, Lc1)[:16], iv))
                    print(decrypt(ct, H(Lc1, Lc0)[:16], iv))

if __name__ == "__main__":
    main()