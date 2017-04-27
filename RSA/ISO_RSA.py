import prime
from hashlib import sha256
from RSA import RSA, generate_x
from Crypto.Cipher import AES
from os import urandom
from random import randint, getrandbits

BLOCK_SIZE = 16  # 128 bits
TEXT_SIZE = 256  # 2048 bits


class ISO_RSA:

    def __init__(self, l):  # l is the length of p and q
        self.l = l
        self.p = 0
        self.q = 0
        self.N = 0
        self.public_key = 0
        self.secret_key = 0
        self.rsa = RSA(l)

    def gen(self, fixed_public_key=False):
        self.rsa.gen(fixed_public_key)
        self.p = self.rsa.p
        self.q = self.rsa.q
        self.N = self.rsa.N
        self.public_key = self.rsa.public_key
        self.secret_key = self.rsa.secret_key

    def enc(self, m):
        x = generate_x(self.N)
        y = prime.exp_mod(x, self.public_key, self.N)
        k = sha256(x.to_bytes(TEXT_SIZE, byteorder='big')).digest()
        iv = urandom(BLOCK_SIZE)
        encryption_suite = AES.new(k, AES.MODE_CBC, iv)
        c = encryption_suite.encrypt(m.to_bytes(TEXT_SIZE, byteorder='big'))  # using AES-256
        return y, c, iv

    def dec(self, y, c, iv):
        x = prime.exp_mod(y, self.secret_key, self.N)
        k = sha256(x.to_bytes(TEXT_SIZE, byteorder='big')).digest()
        decryption_suite = AES.new(k, AES.MODE_CBC, iv)
        return int.from_bytes(decryption_suite.decrypt(c), byteorder='big')  # using AES-256


if __name__ == '__main__':
    from time import time

    # problem 1 c
    def test_iso_rsa():
        l = 1024
        times = 10
        rsa = ISO_RSA(l)
        for t in range(0, times):
            rsa.gen(bool(getrandbits(1)))
            m = randint(0, 2 ** l - 1)
            y, c, iv = rsa.enc(m)
            assert rsa.dec(y, c, iv) == m
    start = time()
    test_iso_rsa()
    print(time() - start)
