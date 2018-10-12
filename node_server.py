import time

import defs
from lwcp import LWCommProtocol
from node import Node

class NodeServer(Node):
    def __init__(self, enc_mode=defs.ENC_MODE_DEFAULT):
        Node.__init__(self, enc_mode)
        self.log_id = 'NodeServer'

        return

    def run(self):
        # Initialize Encryption Engine
        self.init_crypto_engine(use_old_keys=True)

        # Initialize Comms
        cx = LWCommProtocol()
        cx.listen()

        start_time = time.time()
        # Wait for and receive data
        msg = cx.receive()
        # self.print_message(msg)

        # Store the sample data
        data = self.extract_content(msg)

        # Send storage acknowledgement
        cx.send(str({ 'code' : defs.RESP_ACK }))

        if self.encryption_mode == defs.ENC_MODE_FHE:
            # (FHE Mode/) Receive request
            msg = cx.receive()
            request = self.extract_content(msg)
            if request == None:
                self.log("Error: Content is empty")
                cx.close()
                return

            self.log("Decoding request [{}]...".format(request['code']))
            if request['code'] == defs.REQ_AVG_DATA:
                lower_idx = request['params']['lower_idx']
                higher_idx = request['params']['higher_idx']

                result = self.crypto_engine.evaluate( data, lower_idx=lower_idx, higher_idx=higher_idx)
                response = { 'code' : defs.RESP_DATA,
                             'data' : [ result ] }

                # Transmit back raw sample data
                cx.send(str(response))

            # TODO (FHE Mode) Operate on the sample data
            # TODO (FHE Mode) Transmit Result
            pass

        elif self.encryption_mode == defs.ENC_MODE_RSA:
            msg = cx.receive()
            request = self.extract_content(msg)
            if request == None:
                self.log("Error: Content is empty")
                cx.close()
                return

            self.log("Decoding request [{}]...".format(request['code']))
            if request['code'] == defs.REQ_GET_DATA:
                lower_idx = request['params']['lower_idx']
                higher_idx = request['params']['higher_idx']
                # self.log("  Params:")
                # self.log("    Lower Index: {}".format(lower_idx))
                # self.log("    Higher Index: {}".format(higher_idx))

                response = { 'code' : defs.RESP_DATA,
                             'data' : data[lower_idx:higher_idx] }

                # Transmit back raw sample data
                cx.send(str(response))
            

        end_time = time.time()

        # Show result and benchmark
        self.log("   Time Elapsed: {}".format(end_time - start_time))

        # Close comms
        cx.close()

        return

