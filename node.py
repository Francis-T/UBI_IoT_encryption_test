import ast
import random

import defs
from attrdict import AttrDict
from crypto_engine import CryptoEngine, RSACryptoEngine, FHECryptoEngine

class Node():
    def __init__(self, enc_mode=defs.ENC_MODE_DEFAULT, 
                       max_buf_size=defs.MAX_MSG_BUF,
                       data_size=defs.DEFAULT_DATA_SIZE):

        self.encryption_mode = enc_mode
        self.crypto_engine = None
        self.log_id = 'Node'
        self.data_size = data_size
        self.max_buf_size = max_buf_size

        self.ts = {
            'overall'       : { 'start' : None, 'end' : None },
            'evaluate'      : { 'start' : None, 'end' : None },
            'transmit'      : { 'start' : None, 'end' : None },
            'transmit_xtr'  : { 'start' : None, 'end' : None },
            'transmit_rcv'  : { 'start' : None, 'end' : None },
            'transmit_ack'  : { 'start' : None, 'end' : None },
            'req_result'    : { 'start' : None, 'end' : None },
            'encrypt'       : { 'start' : None, 'end' : None },
            'decrypt'       : { 'start' : None, 'end' : None },
        }

        return

    def log(self, message):
        print("[{}] {}".format(self.log_id, message))
        return

    def print_timestamps(self):
        self.log("Timestamps:")
        for key in self.ts.keys():
            if (self.ts[key]["start"] == None) or \
               (self.ts[key]["end"] == None): 
                continue

            self.log("    {} {:11.9f} millisecs".format(key, (self.ts[key]["end"] - self.ts[key]["start"]) * 1000.0))

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
        for i in range(0, self.data_size):
            data.append( random.random() * 100.0 )

        return data

    def init_crypto_engine(self, use_old_keys=False):
        if self.encryption_mode == defs.ENC_MODE_RSA:
            self.crypto_engine = RSACryptoEngine()

        elif self.encryption_mode == defs.ENC_MODE_FHE:
            self.crypto_engine = FHECryptoEngine()

        else:
            self.crypto_engine = CryptoEngine(defs.ENC_MODE_DEFAULT)

        self.crypto_engine.initialize(use_old_keys=use_old_keys)

        return

