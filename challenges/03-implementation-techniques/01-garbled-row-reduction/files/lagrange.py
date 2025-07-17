from sympy import Matrix

def solve_lagrange(xs, ys):
    A = Matrix([
        [1, xs[0], xs[0]**2],
        [1, xs[1], xs[1]**2],
        [1, xs[2], xs[2]**2]
    ])

    b = Matrix(ys)
    coeffs = A.inv_mod(257) * b

    return tuple(int(c) % 256 for c in coeffs)

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
        y0.append((c0[byte_index] + c1[byte_index] * x0 + c2[byte_index] * (x0 ** 2)) % 256)

    return bytes(y0)