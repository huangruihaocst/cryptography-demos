from hashlib import sha256
from os import urandom

SHA256_LENGTH = 32


def xor(x, y):  # x, y are bytes
    length = max(len(x), len(y))
    x = int.from_bytes(x, byteorder='big')
    y = int.from_bytes(y, byteorder='big')
    return (x ^ y).to_bytes(length, byteorder='big')


class OAEP:

    def __init__(self, k0, k1):
        self.k0 = k0
        self.k1 = k1

    def encode(self, m):
        r = urandom(self.k1)
        x = xor(m + bytes(self.k0), sha256(r).digest())
        y = xor(sha256(x).digest(), r)
        # print(len(x))
        # print(len(y))
        return x + y

    def decode(self, c):
        length = len(c)
        x = c[0: length - max(SHA256_LENGTH, self.k1)]
        y = c[length - max(SHA256_LENGTH, self.k1): length]
        r = xor(y, sha256(x).digest())
        m = xor(x, sha256(r).digest())
        m = m[0: len(m) - self.k0]
        return m


if __name__ == '__main__':
    def test_oaep():
        l, k0, k1 = 64, 16, 32  # the value of k0 and k1 must follow some certain rules, or the scheme will not work
        times = 10
        oaep = OAEP(k0, k1)
        for t in range(0, times):
            m = urandom(l)
            assert oaep.decode(oaep.encode(m)) == m

    test_oaep()
