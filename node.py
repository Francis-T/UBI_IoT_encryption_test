import time
import ast

import defs
from lwcp import LWCommProtocol

class NodeServer():
    def __init__(self, enc_mode=defs.ENC_MODE_DEFAULT):
        self.encryption_mode = enc_mode
        return

    def log(self, message):
        print("[NodeServer] {}".format(message))
        return

    def print_message(self, message):
        self.log("Header:")
        self.log(" +-Timestamp: {}".format(message['head']['ts']))
        self.log(" +-Encryption: {}".format(message['head']['enc']))
        self.log(" +-ContentLength: {}".format(message['head']['content_len']))
        self.log("Contents:")
        self.log(" +-{}".format(message['content']))
        return

    def run(self):
        # Initialize Comms
        cx = LWCommProtocol()

        start_time = time.time()
        # Wait for and receive data
        msg = cx.receive()
        self.print_message(msg)

        # Store the sample data
        data = ast.literal_eval(msg['content'].decode())

        # Send storage acknowledgement
        cx.send(str({ 'code' : defs.RESP_ACK }))

        if self.encryption_mode == defs.ENC_MODE_FHE:
            # TODO (FHE Mode/) Receive request
            # TODO (FHE Mode) Operate on the sample data
            # TODO (FHE Mode) Transmit Result
            pass

        elif self.encryption_mode == defs.ENC_MODE_RSA:
            msg = cx.receive()
            request = ast.literal_eval(msg['content'].decode())
            self.log("Decoding request [{}]...".format(request['code']))
            if request['code'] == defs.REQ_GET_DATA:
                lower_idx = request['params']['lower_idx']
                higher_idx = request['params']['higher_idx']
                self.log("  Params:")
                self.log("    Lower Index: {}".format(lower_idx))
                self.log("    Higher Index: {}".format(higher_idx))

                response = { 'code' : defs.RESP_DATA,
                             'data' : data[lower_idx:higher_idx] }

                # Transmit back raw sample data
                cx.send(str(response))
            

        end_time = time.time()

        # TODO Show result and benchmark
        self.log("   Time Elapsed: {}".format(end_time - start_time))

        return

class NodeClient():
    def __init__(self, enc_mode=defs.ENC_MODE_DEFAULT):
        self.encryption_mode = enc_mode
        return

    def log(self, message):
        print("[NodeClient] {}".format(message))
        return

    def run(self):
        # TODO Initialize Comms
        cx = LWCommProtocol()

        # TODO Create the sample data
        start_time = time.time()
        # TODO Encrypt the sample data
        # TODO Transmit the sample data
        cx.send(str([1, 2, 3, 4, 5, 6, 7, 8]))

        # Receive server acknowledge
        msg = cx.receive()
        response = ast.literal_eval(msg['content'].decode())
        if response['code'] != defs.RESP_ACK:
            self.log("Error: Node Server ACK not received!")
            return

        if self.encryption_mode == defs.ENC_MODE_FHE:
            # TODO (FHE Mode) Encrypt operation for sample data
            # TODO (FHE Mode) Transmit operation for sample data
            # TODO (FHE Mode) Receive result from server node
            pass

        elif self.encryption_mode == defs.ENC_MODE_RSA:
            # Request sample data from server node
            request = { 'code' : defs.REQ_GET_DATA,
                        'params' : { 'lower_idx' : 0, 
                                     'higher_idx' : 7 } }
            cx.send(str(request))

            # Receive data from server node
            server_data = None

            msg = cx.receive()
            response = ast.literal_eval(msg['content'].decode())
            if response['code'] == defs.RESP_DATA:
                server_data = response['data']

            # TODO Decrypt received data

            # TODO Operate on the sample data
            self.log("Retrieved data: {}".format(server_data))

        end_time = time.time()

        # TODO Show result and benchmark
        self.log("   Time Elapsed: {}".format(end_time - start_time))

        return

