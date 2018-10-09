import time
import struct

import defs
from lwcp import LWCommProtocol
from node import Node

class NodeClient(Node):
    def __init__(self, enc_mode=defs.ENC_MODE_DEFAULT):
        Node.__init__(self, enc_mode)
        self.log_id = 'NodeClient'

        return

    def log(self, message):
        print("[NodeClient] {}".format(message))
        return

    def run(self):
        # Initialize Comms
        cx = LWCommProtocol()
        cx.connect()

        # Create the sample data
        sample_data = self.generate_data()

        start_time = time.time()

        # Encrypt the sample data
        encrypted_sample_data = self.encrypt_data(sample_data)

        # Transmit the sample data
        cx.send(str(encrypted_sample_data))

        # Receive server acknowledge
        msg = cx.receive()
        response = self.extract_content(msg)
        if response == None:
            self.log("Error: Node Server ACK not received!")
            cx.close()
            return

        if response['code'] != defs.RESP_ACK:
            self.log("Error: Node Server ACK not received!")
            cx.close()
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
            response = self.extract_content(msg)
            if response['code'] == defs.RESP_DATA:
                server_data = response['data']

            # Decrypt received data
            received_data = self.decrypt_data(response['data'])

            # TODO Operate on the sample data
            for i in range(0, len(received_data)):
                received_data[i] = struct.unpack('d', received_data[i])[0]

            # self.log("Retrieved data: {}".format(received_data))

        end_time = time.time()


        # Show result and benchmark
        # self.log("Sample data: {}".format(sample_data))
        # self.log("Retrieved data: {}".format(received_data))
        self.log("Comparing Results:")
        self.log("Sample Data                    Received Data")
        for i in range(0, len(received_data)):
            match = 'O' if sample_data[i] == received_data[i] else 'X'
            self.log("{} : {:11.9f}                {:11.9f}".format(match, sample_data[i], received_data[i]))

        self.log("   Time Elapsed: {}".format(end_time - start_time))

        # Close comms
        cx.close()

        return

