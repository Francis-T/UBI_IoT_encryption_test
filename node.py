import ast
import random
import struct
import base64

import defs

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

class Node():
    def __init__(self, enc_mode=defs.ENC_MODE_DEFAULT):
        self.encryption_mode = enc_mode
        self.log_id = 'Node'
        return

    def log(self, message):
        print("[{}] {}".format(self.log_id, message))
        return

    def extract_content(self, raw_message):
        # Disallow attempts to decode blank messages
        if raw_message == None:
            return ''

        if len(raw_message) <= 0:
            return ''

        content = ast.literal_eval(raw_message['content'].decode())
        return content

    def print_message(self, message):
        self.log("Header:")
        self.log(" +-Timestamp: {}".format(message['head']['ts']))
        self.log(" +-Encryption: {}".format(message['head']['enc']))
        self.log(" +-ContentLength: {}".format(message['head']['content_len']))
        self.log("Contents:")
        self.log(" +-{}".format(message['content']))
        return

    def generate_data(self):
        data = []
        for i in range(0, 10):
            data.append( random.random() * 100.0 )

        return data

    def encrypt_data(self, data):
        if self.encryption_mode == defs.ENC_MODE_RSA:
            
            # Load the public key file
            pk_file = open(defs.FILENAME_PUBLIC_KEY, "rb")
            public_key = pk_file.read()
            pk_file.close()

            rsa_key = RSA.importKey(public_key)
            rsa_key = PKCS1_OAEP.new(rsa_key)

            enc_data = []
            for d in data:
                # self.log("Data Part: {}".format(d))
                ciphertext = rsa_key.encrypt(struct.pack('d',d))
                enc_data.append(base64.b64encode(ciphertext))

            return enc_data

        return data

    def decrypt_data(self, raw_data):
        if self.encryption_mode == defs.ENC_MODE_RSA:

            # Load the public key file
            pk_file = open(defs.FILENAME_PRIVATE_KEY, "rb")
            private_key = pk_file.read()
            pk_file.close()

            rsa_key = RSA.importKey(private_key)
            rsa_key = PKCS1_OAEP.new(rsa_key)

            decrypted_data = []
            for raw in raw_data:
                enc_data = base64.b64decode(raw)
                decrypted_data.append( rsa_key.decrypt(enc_data) )

            return decrypted_data

        return raw_data

