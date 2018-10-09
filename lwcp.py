import time
import ast

import defs
from comms import NodeComm

class LWCommProtocol(NodeComm):
    def __init__(self, enc_mode=defs.ENC_MODE_DEFAULT):
        NodeComm.__init__(self)
        self.encryption_mode = enc_mode
        return

    def send(self, message):
        header  = None
        content = None
        if self.encryption_mode != defs.ENC_MODE_NONE:
            # If an encryption mode was set, then we have to encrypt
            #   the message first before we send it out
            # TODO
            content = message
        else:
            content = message

        # Create the header
        header = { 'ts' : time.time(), 
                   'enc' : self.encryption_mode,
                   'content_len' : len(content) }

        # Create the message
        protocol_message = { 'head' : header, 'content' : content.encode() }

        # Send the message
        NodeComm.send(self, str(protocol_message))

    def receive(self):
        raw_message = NodeComm.receive(self)
        # self.log("Raw Message: [{}]({})".format(raw_message, len(raw_message)))
        if raw_message == None or len(raw_message) <= 0:
            return None

        protocol_message = ast.literal_eval(raw_message)

        return protocol_message


