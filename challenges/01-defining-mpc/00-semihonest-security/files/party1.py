from random import randint
import numpy as np

class Party1:
    def __init__(self):
        self.a = randint(pow(2, 9), pow(2, 11))
        self.b = randint(pow(2, 9), pow(2, 11))
        self.c = randint(pow(2, 9), pow(2, 11))

    def int1(self):
        A = np.array([
            [self.a, self.b, self.c],
            [-self.a, self.b, self.c],
            [-2*self.a, -3*self.b, 2*self.c]
        ])
        b = np.array([325207, 145609, -110749])

        [x, y, z] = np.linalg.solve(A, b)

        return [self.a, self.b, self.c, x, y, z]