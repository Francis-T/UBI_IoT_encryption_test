import defs

class CryptoEngine():
    def __init__(self, enc_mode):
        self.encryption_mode = enc_mode
        self.initialized = False
        self.public_key = None
        self.private_key = None
        self.log_id = 'CryptoEngine'

        return

    def log(self, message):
        print("[{}] {}".format(self.log_id, message))
        return

    def initialize(self, use_old_keys=False):
        return

    def encrypt(self, data):
        return data

    def decrypt(self, data):
        return data

