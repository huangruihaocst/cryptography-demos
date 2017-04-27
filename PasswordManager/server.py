from Crypto.PublicKey import RSA
import struct
from os import urandom
from hashlib import sha256
from Crypto.Cipher import AES
import json

BACKLOG = 5
BUFFER_SIZE = 1024
KEY_LENGTH = 1024
SALT_LENGTH = 32
BLOCK_SIZE = 16
AES_KEY_LENGTH = 32  # AES-256, 32 bytes = 256 bits
NONCE_LENGTH = 32
TOKEN_LENGTH = 32


def list_to_bytes(l):
    return b''.join(map(lambda x: x.to_bytes(1, byteorder='big'), l))


def get_k(username, mpw):
    with open('users.json') as f:
        users = json.load(f)
    ke = sha256(list_to_bytes(users[username]['se']) + mpw.encode()).digest()
    cipher = users[username]['ae']
    iv = list_to_bytes(cipher[:BLOCK_SIZE])
    cipher = list_to_bytes(cipher[BLOCK_SIZE:])
    decryption_suite = AES.new(ke, AES.MODE_CBC, iv)  # AES-256
    k = decryption_suite.decrypt(cipher)
    return k


class Server:

    def __init__(self):
        self.__nonce = b''
        # random_generator = Random.new().read
        self.__private_key = RSA.generate(KEY_LENGTH)
        self.__public_key = self.__private_key.publickey()
        self.__tokens = {}

    def create_account(self, username, cipher):
        # get existing users
        with open('users.json') as f:
            users = json.load(f)

        # check if the user exists
        if username in users:
            print('user exists')
            return False

        # decrypt cipher and get mpw
        mpw = self.__private_key.decrypt(cipher)

        # save user info into user list
        sa = urandom(SALT_LENGTH)
        se = urandom(SALT_LENGTH)
        p = sha256(sa + mpw).digest()
        ke = sha256(se + mpw).digest()
        iv = urandom(BLOCK_SIZE)
        encryption_suite = AES.new(ke, AES.MODE_CBC, iv)  # AES-256
        k = urandom(AES_KEY_LENGTH)
        ae = encryption_suite.encrypt(k)
        user = dict()
        # json cannot serialize bytes
        user['sa'] = list(sa)
        user['se'] = list(se)
        user['p'] = list(p)
        user['ae'] = list(iv + ae)
        users[username] = user
        with open('users.json', 'w') as f:
            f.write(json.dumps(users))
        return True

    def generate_nonce(self):
        self.__nonce = urandom(NONCE_LENGTH)
        return self.__nonce

    def get_public_key(self):
        return self.__public_key.exportKey('DER')

    def authenticate_account(self, username, cipher):
        plain = self.__private_key.decrypt(cipher)
        nonce = plain[:NONCE_LENGTH]
        mpw = plain[NONCE_LENGTH:]
        if nonce == self.__nonce:
            # check if user exists and if p == H(sa||mpw)
            with open('users.json') as f:
                users = json.load(f)
            if username in users:
                if list_to_bytes(users[username]['p']) == sha256(list_to_bytes(users[username]['sa']) + mpw).digest():
                    print('success')
                    token = urandom(TOKEN_LENGTH)
                    self.__tokens[username] = token
                    return True, token
                else:
                    print('master password wrong')
                    return False, None
            else:
                print('user does not exist')
                return False, None
        else:
            print('nonce fault')
            return False, None

    def __check_token(self, username, token):
        if username not in self.__tokens:
            print('user not authenticated')
            return False
        if self.__tokens[username] != token:
            print('token has expired')
            return False
        return True

    def add(self, username, mpw, cipher):
        plain = self.__private_key.decrypt(cipher)
        token = plain[:TOKEN_LENGTH]
        if not self.__check_token(username, token):
            return False, None
        website, password = plain[TOKEN_LENGTH:].decode('utf-8').split(' ')
        k = get_k(username, mpw)
        with open('passwords.json') as f:
            passwords = json.load(f)
        if username not in passwords:
            passwords[username] = dict()
        iv = urandom(BLOCK_SIZE)
        encryption_suite = AES.new(k, AES.MODE_CBC, iv)
        if website not in passwords[username]:
            passwords[username][website] = list(iv + encryption_suite.encrypt(struct.pack('16s', password.encode())))
        else:
            print('website exists')
            return False, None
        with open('passwords.json', 'w') as f:
            f.write(json.dumps(passwords))
        new_token = urandom(TOKEN_LENGTH)
        self.__tokens[username] = new_token
        return True, new_token

    def read(self, username, mpw, cipher):
        plain = self.__private_key.decrypt(cipher)
        token = plain[:TOKEN_LENGTH]
        if not self.__check_token(username, token):
            return None, None
        website = plain[TOKEN_LENGTH:].decode('utf-8')
        k = get_k(username, mpw)
        with open('passwords.json') as f:
            passwords = json.load(f)
        if username not in passwords or website not in passwords[username]:
            print('website does not exist')
            return None, None
        iv = passwords[username][website][:BLOCK_SIZE]
        decryption_suite = AES.new(k, AES.MODE_CBC, list_to_bytes(iv))
        password = decryption_suite.decrypt(list_to_bytes(passwords[username][website][BLOCK_SIZE:])).rstrip(b'\x00')\
            .decode('utf-8')
        new_token = urandom(TOKEN_LENGTH)
        self.__tokens[username] = new_token
        return password, new_token

    def update(self, username, mpw, cipher):
        plain = self.__private_key.decrypt(cipher)
        token = plain[:TOKEN_LENGTH]
        if not self.__check_token(username, token):
            return False, None
        website, password = plain[TOKEN_LENGTH:].decode('utf-8').split(' ')
        k = get_k(username, mpw)
        with open('passwords.json') as f:
            passwords = json.load(f)
        if username not in passwords:
            passwords[username] = dict()
        if website not in passwords[username]:
            print('website does not exist')
            return False, None
        iv = urandom(BLOCK_SIZE)
        encryption_suite = AES.new(k, AES.MODE_CBC, iv)
        passwords[username][website] = list(iv + encryption_suite.encrypt(struct.pack('16s', password.encode())))
        with open('passwords.json', 'w') as f:
            f.write(json.dumps(passwords))
        new_token = urandom(TOKEN_LENGTH)
        self.__tokens[username] = new_token
        return True, new_token

    def remove(self, username, cipher):
        plain = self.__private_key.decrypt(cipher)
        token = plain[:TOKEN_LENGTH]
        if not self.__check_token(username, token):
            return None, None
        website = plain[TOKEN_LENGTH:].decode('utf-8')
        with open('passwords.json') as f:
            passwords = json.load(f)
        if username not in passwords or website not in passwords[username]:
            print('website does not exist')
            return None, None
        del passwords[username][website]
        with open('passwords.json', 'w') as f:
            f.write(json.dumps(passwords))
        new_token = urandom(TOKEN_LENGTH)
        self.__tokens[username] = new_token
        return True, new_token

    def log_out(self, username):
        del self.__tokens[username]
        return True

    def change_mpw(self, username, mpw, new_mpw):
        k = get_k(username, mpw)
        new_sa = urandom(SALT_LENGTH)
        new_se = urandom(SALT_LENGTH)
        new_ke = sha256(new_se + new_mpw.encode()).digest()
        iv = urandom(BLOCK_SIZE)
        encryption_suite = AES.new(new_ke, AES.MODE_CBC, iv)  # AES-256
        new_ae = encryption_suite.encrypt(k)
        new_p = sha256(new_sa + new_mpw.encode()).digest()
        # new user info
        user = dict()
        user['sa'] = list(new_sa)
        user['se'] = list(new_se)
        user['p'] = list(new_p)
        user['ae'] = list(iv + new_ae)
        with open('users.json') as f:
            users = json.load(f)
        users[username] = user
        with open('users.json', 'w') as f:
            f.write(json.dumps(users))
            new_token = urandom(TOKEN_LENGTH)
            self.__tokens[username] = new_token
        return True, new_token

