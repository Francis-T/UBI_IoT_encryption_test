import defs
from crypto_engine import CryptoEngine

import struct
import base64
import os

import seal
from seal import EncryptionParameters, \
                 SEALContext, \
                 KeyGenerator, \
                 PublicKey, \
                 SecretKey

class FHECryptoEngine(CryptoEngine):
    def __init__(self):
        CryptoEngine.__init__(self, defs.ENC_MODE_FHE)
        self.log_id = 'FHECryptoEngine'
        self.encrypt_params = None
        self.context = None

        return

    def load_keys(self):
        self.private_key = SecretKey()
        self.private_key.load(defs.FN_FHE_PRIVATE_KEY)

        self.public_key = PublicKey()
        self.public_key.load(defs.FN_FHE_PUBLIC_KEY)
        
        return True

    def generate_keys(self):
        if self.encrypt_params == None or \
           self.context == None:
            self.init_encrypt_params()

        keygen = KeyGenerator(self.context)

        # Generate the private key
        self.private_key = keygen.secret_key()
        self.private_key.save(defs.FN_FHE_PRIVATE_KEY)

        # Generate the public key
        self.public_key = keygen.public_key()
        self.public_key.save(defs.FN_FHE_PUBLIC_KEY)

        return True

    def init_encrypt_params(self):
        self.encrypt_params = EncryptionParameters()
        self.encrypt_params.set_poly_modulus("1x^2048 + 1")
        self.encrypt_params.set_coeff_modulus(seal.coeff_modulus_128(2048))
        self.encrypt_params.set_plain_modulus(1 << 8)

        self.context = SEALContext(self.encrypt_params)

        return

    def initialize(self, use_old_keys=False):
        # Initialize encryption params
        self.init_encrypt_params()

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

