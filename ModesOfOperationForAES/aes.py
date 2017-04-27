import os
from Crypto.Cipher import AES
from Crypto.Util import Counter

L = 10  # block count
BLOCK_SIZE_BYTES = 16  # 16 bytes = 128 bits
TIMES = 10  # test 10 times

plains = []
keys = []

# generate plaintexts and keys
for i in range(0, TIMES):
    plains.append(os.urandom(L * BLOCK_SIZE_BYTES))
    keys.append(os.urandom(BLOCK_SIZE_BYTES))


# len(bytes1) == len(bytes2)
def block_xor(bytes1, bytes2):
    return bytes([byte1 ^ byte2 for (byte1, byte2) in zip(bytes1, bytes2)])


def cbc_encrypt(plain, key, iv):
    block_aes = AES.new(key)  # block encryption uses AES, block size = BLOCK_SIZE_BYTES
    blocks = [plain[l: l + BLOCK_SIZE_BYTES] for l in range(0, len(plain), BLOCK_SIZE_BYTES)]
    cipher_blocks = []
    for l in range(0, L):
        if l == 0:
            cipher_blocks.append(block_aes.encrypt(block_xor(blocks[l], iv)))
        else:
            cipher_blocks.append(block_aes.encrypt(block_xor(blocks[l], cipher_blocks[l - 1])))
    return b''.join(cipher_blocks)


def cbc_decrypt(cipher, key, iv):
    block_aes = AES.new(key)
    blocks = [cipher[l: l + BLOCK_SIZE_BYTES] for l in range(0, len(cipher), BLOCK_SIZE_BYTES)]
    plain_blocks = []
    for l in range(0, L):
        if l == 0:
            plain_blocks.append(block_xor(block_aes.decrypt(blocks[l]), iv))
        else:
            plain_blocks.append(block_xor(block_aes.decrypt(blocks[l]), blocks[l - 1]))
    return b''.join(plain_blocks)


def ctr_encrypt_decrypt(text, key, ctr):
    block_aes = AES.new(key)  # block encryption/decryption uses AES, block size = BLOCK_SIZE_BYTES
    blocks = [text[l: l + BLOCK_SIZE_BYTES] for l in range(0, len(text), BLOCK_SIZE_BYTES)]
    new_text_blocks = []
    for l in range(0, L):
        new_text_blocks.append(block_xor(block_aes.encrypt(ctr()), blocks[l]))
    return b''.join(new_text_blocks)


for j in range(0, TIMES):
    iv = os.urandom(BLOCK_SIZE_BYTES)

    cbc_suite = AES.new(keys[j], AES.MODE_CBC, iv)
    lib_cipher_cbc = cbc_suite.encrypt(plains[j])
    my_cipher_cbc = cbc_encrypt(plains[j], keys[j], iv)
    assert lib_cipher_cbc == my_cipher_cbc

    cbc_suite = AES.new(keys[j], AES.MODE_CBC, iv)
    lib_plain_cbc = cbc_suite.decrypt(lib_cipher_cbc)
    my_plain_cbc = cbc_decrypt(my_cipher_cbc, keys[j], iv)
    assert lib_plain_cbc == my_plain_cbc == plains[j]

# test
for k in range(0, TIMES):
    counter = Counter.new(BLOCK_SIZE_BYTES * 8)  # 1 Byte = 8 bits

    ctr_suite = AES.new(keys[k], AES.MODE_CTR, counter=counter)
    lib_cipher_ctr = ctr_suite.encrypt(plains[k])
    counter = Counter.new(BLOCK_SIZE_BYTES * 8)  # counter is stateful, needs refresh
    my_cipher_ctr = ctr_encrypt_decrypt(plains[k], keys[k], counter)
    assert lib_cipher_ctr == my_cipher_ctr

    counter = Counter.new(BLOCK_SIZE_BYTES * 8)  # counter is stateful, needs refresh
    ctr_suite = AES.new(keys[k], AES.MODE_CTR, counter=counter)
    lib_plain_ctr = ctr_suite.decrypt(lib_cipher_ctr)
    counter = Counter.new(BLOCK_SIZE_BYTES * 8)  # counter is stateful, needs refresh
    my_plain_ctr = ctr_encrypt_decrypt( my_cipher_ctr, keys[k], counter)
    assert lib_plain_ctr == my_plain_ctr == plains[k]
