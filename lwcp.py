import time
import ast

import defs
from comms import NodeComm

class LWCommProtocol(NodeComm):
    def __init__(self, enc_mode=defs.ENC_MODE_DEFAULT,
                       max_buf_size=defs.MAX_MSG_BUF):

        NodeComm.__init__(self, max_buf_size=max_buf_size)
        self.encryption_mode = enc_mode

        return

    def send(self, message):
        header  = None
        # TODO Always check if the message being sent is valid
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
        if raw_message == None or len(raw_message) <= 0:
            return None

        protocol_message = ast.literal_eval(raw_message)

        return protocol_message


