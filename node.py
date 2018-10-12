import ast
import random

import defs
from crypto_engine import CryptoEngine, RSACryptoEngine, FHECryptoEngine

class Node():
    def __init__(self, enc_mode=defs.ENC_MODE_DEFAULT):
        self.encryption_mode = enc_mode
        self.crypto_engine = None
        self.log_id = 'Node'
        return

    def log(self, message):
        print("[{}] {}".format(self.log_id, message))
        return

    def extract_content(self, raw_message):
        # Disallow attempts to decode blank messages
        if raw_message == None:
            return ''

        self.log("RAW MESSAGE : {}".format(str(raw_message)))

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

    def init_crypto_engine(self, use_old_keys=False):
        if self.encryption_mode == defs.ENC_MODE_RSA:
            self.crypto_engine = RSACryptoEngine()

        elif self.encryption_mode == defs.ENC_MODE_FHE:
            self.crypto_engine = FHECryptoEngine()

        else:
            self.crypto_engine = CryptoEngine()

        self.crypto_engine.initialize(use_old_keys=use_old_keys)

        return

