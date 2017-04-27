# import socket
import getpass
from Crypto.PublicKey import RSA
import server


class Client:

    def __init__(self):
        self.server = server.Server()
        self.__username = None
        self.__mpw = None
        self.__token = None

    def create_account(self, username, mpw):
        public_key = self.server.get_public_key()  # server public key
        return self.server.create_account(username, RSA.importKey(public_key).encrypt(mpw.encode(), 32)[0])

    def authenticate_account(self, username, mpw):
        self.__username = username
        public_key = self.server.get_public_key()
        nonce = self.server.generate_nonce()
        res, token = self.server.authenticate_account(username,
                                                      RSA.importKey(public_key).encrypt(nonce + mpw.encode(), 32)[0])
        if res:
            self.__token = token
            self.__mpw = mpw
        return res

    def add(self, website, password):
        if self.__token is None:
            print('user not authenticated')
            return False
        public_key = self.server.get_public_key()
        res, new_token = self.server.add(self.__username, self.__mpw, RSA.importKey(public_key)
                                         .encrypt(self.__token + (website + ' ' + password).encode(), 32)[0])
        if res:
            self.__token = new_token
            return res

    # return None if failed
    def read(self, website):
        if self.__token is None:
            print('user not authenticated')
            return None
        public_key = self.server.get_public_key()
        password, new_token = self.server.read(self.__username, self.__mpw, RSA.importKey(public_key)
                                               .encrypt(self.__token + website.encode(), 32)[0])
        if password is not None:
            self.__token = new_token
        return password

    def update(self, website, password):
        if self.__token is None:
            print('user not authenticated')
            return False
        public_key = self.server.get_public_key()
        res, new_token = self.server.update(self.__username, self.__mpw, RSA.importKey(public_key)
                                            .encrypt(self.__token + (website + ' ' + password).encode(), 32)[0])
        if res:
            self.__token = new_token
        return res

    def remove(self, website):
        if self.__token is None:
            print('user not authenticated')
            return False
        public_key = self.server.get_public_key()
        res, new_token = self.server.remove(self.__username, RSA.importKey(public_key)
                                            .encrypt(self.__token + website.encode(), 32)[0])
        if res:
            self.__token = new_token
        return res

    def log_out(self):
        if self.__token is None:
            print('user not authenticated')
            return False
        res = self.server.log_out(self.__username)
        if res:
            self.__username = None
            self.__mpw = None
            self.__token = None
            return True
        return res

    def change_mpw(self, new_mpw):
        if self.__token is None:
            print('user not authenticated')
            return False
        res, token = self.server.change_mpw(self.__username, self.__mpw, new_mpw)
        if res:
            self.__mpw = new_mpw
            self.__token = token
        return res


