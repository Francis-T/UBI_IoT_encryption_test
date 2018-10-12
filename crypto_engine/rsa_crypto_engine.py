import defs
from crypto_engine import CryptoEngine

import struct
import base64
import os

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

class RSACryptoEngine(CryptoEngine):
    def __init__(self):
        CryptoEngine.__init__(self, defs.ENC_MODE_RSA)
        self.log_id = 'RSACryptoEngine'
        return

    def load_keys(self):
        # Load the private key file
        pk_file = open(defs.FN_RSA_PRIVATE_KEY, "rb")
        key_text = pk_file.read()
        self.private_key = RSA.importKey(key_text)
        pk_file.close()

        # Load the public key file
        pk_file = open(defs.FN_RSA_PUBLIC_KEY, "rb")
        key_text = pk_file.read()
        self.public_key = RSA.importKey(key_text)
        pk_file.close()
        
        return True

    def generate_keys(self):
        # Generate the key
        self.log("Generating keys...")
        new_key = RSA.generate(4096, e=65537)

        # Export the private key
        self.log("Writing private key...")
        file_priv_key = open(defs.FN_RSA_PRIVATE_KEY, "wb")
        file_priv_key.write(new_key.exportKey("PEM"))
        file_priv_key.close()

        self.private_key = new_key

        # Export the public key
        self.log("Writing public key...")
        file_pub_key = open(defs.FN_RSA_PUBLIC_KEY, "wb")
        file_pub_key.write(new_key.publickey().exportKey("PEM"))
        file_pub_key.close()

        self.public_key = new_key.publickey()

        return True

    def initialize(self, use_old_keys=False):
        # Check if the public key file exists
        if os.path.isfile(defs.FN_RSA_PUBLIC_KEY) and \
           os.path.isfile(defs.FN_RSA_PRIVATE_KEY) and \
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

        rsa_key = self.public_key
        rsa_key = PKCS1_OAEP.new(rsa_key)

        enc_data = []
        for d in data:
            # self.log("Data Part: {}".format(d))
            ciphertext = rsa_key.encrypt(struct.pack('d',d))
            enc_data.append(base64.b64encode(ciphertext))

        return enc_data

    def decrypt(self, raw_data):
        if not self.initialized:
            self.log("Not initialized")
            return False

        rsa_key = self.private_key
        rsa_key = PKCS1_OAEP.new(rsa_key)

        decrypted_data = []
        for raw in raw_data:
            enc_data = base64.b64decode(raw)
            decrypted_data.append( struct.unpack('d', rsa_key.decrypt(enc_data))[0] )

        return decrypted_data

