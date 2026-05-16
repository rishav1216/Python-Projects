def euclidean_algorithm(num1: int, num2: int, steps: int = 0) -> int:
    """Perform the Euclidean algorithm to find the greatest common divisor of num1, num2
    Returns (gcd, number of steps in the Euclidean algorithm) where number of steps is the
    number of divisions with remainder performed.

    Print steps along the way
    """

    a = max(num1, num2)
    b = min(num1, num2)

    if b == 0:
        return (a, steps)
    else:
        r = a % b
        q = a // b # Defined so a = bq + r

        print('Step ' + str(steps + 1))
        print(str(a) + ' = ' + str(b) + ' * ' + str(q) + ' + ' + str(r))
        return euclidean_algorithm(b, r, steps + 1)

class DivisionWithRemainder:
    """Contains equations of the form a = b * q + r"""

    def __init__(self, a: int, b: int, q: int, r: int):
        if a == q * b + r:
            self.a = a
            self.b = b
            self.q = q
            self.r = r
        else:
            raise ValueError("a =/= q * b + r")

    def __str__(self):
        return(str(self.a) + ' = ' + str(self.q) + ' * ' + str(self.b) + ' + ' + str(self.r))


if __name__ == "__main__":

    print(euclidean_algorithm(1044, 512))
