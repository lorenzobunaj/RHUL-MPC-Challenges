def generate_product_share(a_share, b_share, c_share, d, e, p):
    prod_share = d * e + d * b_share + a_share * e + c_share

    return prod_share % p

def modinv(a, p):
    return pow(a, -1, p)

def lagrange_coeffs(x_s, p):
    coeffs = []
    for j, xj in enumerate(x_s):
        num = 1
        denom = 1
        for m, xm in enumerate(x_s):
            if m != j:
                num = (num * (-xm)) % p
                denom = (denom * (xj - xm)) % p
        lambda_j = (num * modinv(denom, p)) % p
        coeffs.append(lambda_j)
    return coeffs

def lagrange_interpolation(shares, p, n):
    coeffs = lagrange_coeffs([i+1 for i in range(n)], p)
    s = 0
    for i in range(n):
        s += shares[i] * coeffs[i]

    return s % p