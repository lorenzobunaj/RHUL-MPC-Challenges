import os

def random_coeff(p):
    while True:
        z = int.from_bytes(os.urandom(16), "big")
        if z < p:
            return z

def make_random_poly(deg):
    p = (1 << 127) - 1
    return [random_coeff(p) for _ in range(deg + 1)]

def random_coeffs(coeffs, x):
    p = (1 << 127) - 1
    y = 0
    for a in reversed(coeffs):
        y = (y * x + a) % p
    return y.to_bytes(16, "big")