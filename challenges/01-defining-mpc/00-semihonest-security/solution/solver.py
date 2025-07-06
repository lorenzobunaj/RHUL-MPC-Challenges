import numpy as np

def main():
    # example of inputs (in2 = [0, 0])
    a = 1577
    y = 77.07900287631831
    z = 127.1653814602133
    A = np.array([
        [a, y, z],
        [-a, y, z],
        [-2*a, -3*y, 2*z]
    ])
    b = np.array([325207, 145609, -110749])
    [x, b, c] = np.linalg.solve(A, b)

    print(a * b * c)

if __name__ == "__main__":
    main()