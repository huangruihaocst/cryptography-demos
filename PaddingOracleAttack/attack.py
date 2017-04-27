import os
from Crypto.Cipher import AES

BLOCK_SIZE_BYTES = 16  # 16 Bytes = 128 bits

key = os.urandom(BLOCK_SIZE_BYTES)
iv = os.urandom(BLOCK_SIZE_BYTES)

count = 0  # count is used to count query times


# cipher here includes iv (M1 M2 => IV C1 C2...)
def padding_oracle(cipher):
    global count
    count += 1
    cipher_iv = cipher[0: BLOCK_SIZE_BYTES]
    cipher_text = cipher[BLOCK_SIZE_BYTES:]
    decryption_suite = AES.new(key, AES.MODE_CBC, cipher_iv)
    plain = decryption_suite.decrypt(cipher_text)
    padding = int.from_bytes(bytes([plain[-1]]), byteorder='big')  # padding byte
    if padding > BLOCK_SIZE_BYTES:
        return False
    for index in range(-1, -1 - padding, -1):
        if plain[index] != padding:
            print(count, ": ", cipher, "\t" * 2, False)
            return False
    print(count, ": ", cipher, "\t" * 2, True)
    return True


# returns the length of the padding. 0 means invalid padding
# input must have valid padding => 0 should never be returned if it is a valid call
# cipher here includes iv (M1 M2 => IV C1 C2...)
def count_padding_length(cipher):
    second_to_last = cipher[-BLOCK_SIZE_BYTES * 2: -BLOCK_SIZE_BYTES]  # second to last block, block[-2]
    for index in range(0, BLOCK_SIZE_BYTES):
        new_byte = b'\x01' if second_to_last[index] != b'\x01' else b'\x02'  # modify the index byte of block[-2]
        new_byte_int = int.from_bytes(new_byte, byteorder='big')
        new_block_int = [second_to_last[i] if i != index else new_byte_int for i in range(0, BLOCK_SIZE_BYTES)]
        if not padding_oracle(cipher.replace(second_to_last, bytes(new_block_int))):
            return BLOCK_SIZE_BYTES - index
    return 0


# returns the last block of plaintext
# cipher here includes iv (M1 M2 => IV C1 C2...)
def padding_oracle_attack(cipher):
    padding_length = count_padding_length(cipher)
    if padding_length == BLOCK_SIZE_BYTES:  # dummy block
        return bytes([BLOCK_SIZE_BYTES]) * BLOCK_SIZE_BYTES
    guess_int = []  # guessed last block (byte in int)
    for i in range(0, BLOCK_SIZE_BYTES):
        guess_int.append(padding_length)  # the first (BLOCK_SIZE_BYTES - padding_length) items are placeholders
    second_to_last = cipher[-BLOCK_SIZE_BYTES * 2: -BLOCK_SIZE_BYTES]  # second to last block, block[-2]
    # try byte on i, change all the byte after i to form a valid padding
    for i in range(BLOCK_SIZE_BYTES - padding_length - 1, -1, -1):
        for j in range(0, BLOCK_SIZE_BYTES * BLOCK_SIZE_BYTES):  # guess plain[i] == j
            new_block_int = []
            for k in range(0, i):
                new_block_int.append(second_to_last[k])  # first i bytes remain the same
            new_block_int.append(second_to_last[i] ^ j ^ (BLOCK_SIZE_BYTES - i))  # the guessed byte
            for k in range(i + 1, BLOCK_SIZE_BYTES):
                new_block_int.append(second_to_last[k] ^ guess_int[k] ^ (BLOCK_SIZE_BYTES - i))  # valid padding
            if padding_oracle(cipher.replace(second_to_last, bytes(new_block_int))):
                guess_int[i] = j
                break
    return bytes(guess_int)


# plain here does not include iv (M1 M2 M3...)
def test(plain):
    global count
    encryption_suite = AES.new(key, AES.MODE_CBC, iv)
    cipher = encryption_suite.encrypt(plain)
    last_block = bytes(plain[-BLOCK_SIZE_BYTES:])
    last_block_guessed = padding_oracle_attack(iv + cipher)
    assert last_block == last_block_guessed
    print("total query: ", count)


test(b'\x01' * 12 + b'\x04' * 4)
test(b'\x01' * 30 + b'\x02' * 2)
