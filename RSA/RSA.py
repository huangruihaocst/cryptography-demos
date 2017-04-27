import prime
from random import randint, getrandbits
from math import gcd
import sys

often_used_public_key = 65537
recursion_limit = 2000

sys.setrecursionlimit(recursion_limit)


# reference: https://zh.wikipedia.org/wiki/%E6%89%A9%E5%B1%95%E6%AC%A7%E5%87%A0%E9%87%8C%E5%BE%97%E7%AE%97%E6%B3%95
def ext_euclid(a, b):
    if b == 0:
        return 1, 0, a
    else:
        x, y, q = ext_euclid(b, a % b)
        x, y = y, (x - (a // b) * y)
        return x, y, q


def generate_x(rsa_n):
    while True:
        x = randint(0, rsa_n - 1)
        if gcd(x, rsa_n) == 1:
            return x


class RSA:

    def __init__(self, l):  # l is the length of p and q
        self.l = l
        self.p = 0
        self.q = 0
        self.N = 0
        self.public_key = 0
        self.secret_key = 0

    def gen(self, fixed_public_key=False):
        self.p = prime.generate_prime(self.l)
        self.q = prime.generate_prime(self.l)
        self.N = self.p * self.q
        phi = (self.p - 1) * (self.q - 1)  # φ(N) = (p - 1) * (q - 1)
        if fixed_public_key:  # using often used public key will cut the time of computation sharply
            e = often_used_public_key
            self.public_key = e
        else:  # also supports generating a new public key
            while True:
                e = randint(2, phi - 1)
                if gcd(e, phi) == 1:
                    self.public_key = e
                    break
        d = ext_euclid(e, phi)[0]
        while d <= 0:
            d += phi
        self.secret_key = d

    def trap_door(self, x):
        return prime.exp_mod(x, self.public_key, self.N)

    def inverse(self, y):
        return prime.exp_mod(y, self.secret_key, self.N)

if __name__ == '__main__':
    from time import time

    # problem 1 b
    def test_rsa():
        l = 1024
        times = 10
        rsa = RSA(l)
        for t in range(0, times):
            rsa.gen(bool(getrandbits(1)))
            x = generate_x(rsa.N)
            y = rsa.trap_door(x)
            assert x == rsa.inverse(y)


    start = time()
    test_rsa()
    print(time() - start)
