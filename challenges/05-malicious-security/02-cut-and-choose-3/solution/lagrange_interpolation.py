P = (1 << 127) - 1

def modinv(a, p=P):
    return pow(a % p, p - 2, p)

def poly_mul(A, B, p=P):
    C = [0] * (len(A) + len(B) - 1)
    for i, a in enumerate(A):
        if a == 0: 
            continue
        for j, b in enumerate(B):
            C[i+j] = (C[i+j] + a*b) % p
    return C

def poly_synthetic_divide_by_linear(A, r, p=P):
    n = len(A) - 1
    Q = [0] * n
    Q[-1] = A[-1]
    for k in range(n-2, -1, -1):
        Q[k] = (A[k+1] + r * Q[k+1]) % p
    return Q

def lagrange_coefficients(xs, ys, p=P):
    n = len(xs)
    assert n == len(ys) and n >= 1
    xs = [x % p for x in xs]
    ys = [y % p for y in ys]

    V = [1]
    for x in xs:
        V = poly_mul(V, [(-x) % p, 1], p)

    denoms = []
    for j in range(n):
        dj = 1
        xj = xs[j]
        for m in range(n):
            if m == j: 
                continue
            dj = (dj * (xj - xs[m])) % p
        denoms.append(dj)

    coeffs = [0] * n
    for j in range(n):
        xj, yj = xs[j], ys[j]
        Qj = poly_synthetic_divide_by_linear(V, xj, p)
        scale = (yj * modinv(denoms[j], p)) % p
        for k in range(n):
            coeffs[k] = (coeffs[k] + scale * Qj[k]) % p
    return coeffs