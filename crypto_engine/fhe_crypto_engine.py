import defs
from crypto_engine import CryptoEngine

import struct
import base64
import os

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

class FHECryptoEngine(CryptoEngine):
    def __init__(self):
        CryptoEngine.__init__(self, defs.ENC_MODE_FHE)
        self.log_id = 'FHECryptoEngine'
        return

    def load_keys(self):
        # TODO
        
        return True

    def generate_keys(self):
        # TODO

        return True

    def initialize(self, use_old_keys=False):
        # TODO
        # Check if the public key file exists
        if os.path.isfile(defs.FN_FHE_PUBLIC_KEY) and \
           os.path.isfile(defs.FN_FHE_PRIVATE_KEY) and \
           use_old_keys == True:

            self.log("Keys already exist. Reusing them instead.")

            if self.load_keys():
                self.initialized = True
                return True

            return False

        if self.generate_keys():
            self.initialized = True
            return True

        return False

    def encrypt(self, data):
        if not self.initialized:
            self.log("Not initialized")
            return False

        # TODO

        return data

    def decrypt(self, raw_data):
        if not self.initialized:
            self.log("Not initialized")
            return False
        
        # TODO

        return data

