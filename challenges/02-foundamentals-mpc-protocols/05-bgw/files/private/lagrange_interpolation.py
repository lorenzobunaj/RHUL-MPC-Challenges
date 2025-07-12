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

def lagrange_interpolation(self, shares):
    coeffs = lagrange_coeffs([i+1 for i in range(3)], self.p)
    s = 0
    for i in range(3):
        s += shares[i] * coeffs[i]

    return s % self.p