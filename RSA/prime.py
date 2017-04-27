import math
from random import randint


# calculate b ^ e mod m
# reference: http://www.cnblogs.com/7hat/p/3398394.html
def exp_mod(b, e, m):
    result = 1
    while e != 0:
        if e & 1 == 1:
            result = (result * b) % m
        e >>= 1
        b = (b * b) % m
    return result


def decompose(n):
    assert n != 1
    n -= 1
    r = 0
    while n % 2 == 0:
        r += 1
        n >>= 1
    return r, n


# check if n is composite with a
# returns true if n is composite, false if cannot decide
def check_composite(a, r, u, n):
    if exp_mod(a, u, n) == 1:
        return False
    for i in range(0, r):
        if exp_mod(a, (2 ** i) * u, n) == n - 1:
            return False
    return True


# returns true if n is prime using Miller–Rabin algorithm
def is_prime_mr(n, t=10):
    assert n > 0
    if n > 2 and n % 2 == 0:
        return False
    r, u = decompose(n)
    for j in range(0, t):
        a = randint(1, n - 1)
        if check_composite(a, r, u, n):
            return False
    return True


# returns true if n is prime using naive algorithm
def is_prime_naive(n):
    assert n > 0
    if n == 1:
        return False
    if n <= 3:
        return True
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True


# generate prime with the length of l
def generate_prime(l):
    while True:
        p = randint(0, 2 ** (l - 1) - 1)
        p |= 1 << (l - 1)
        if is_prime_mr(p):
            return p

if __name__ == '__main__':
    from time import time

    # Problem 1 a
    def test_mr():
        l = 20  # the length of the prime
        times = 10  # number of times of checking correctness
        for t in range(0, times):
            p = generate_prime(l)
            print(p)
            assert is_prime_naive(p)


    start = time()
    test_mr()
    print(time() - start)
