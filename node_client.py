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
        # Initialize Encryption Engine
        self.init_crypto_engine(use_old_keys=True)

        # Initialize Comms
        cx = LWCommProtocol()
        cx.connect()

        # Create the sample data
        sample_data = self.generate_data()

        start_time = time.time()

        # Encrypt the sample data
        encrypted_sample_data = self.crypto_engine.encrypt(sample_data)

        # Transmit the sample data
        self.log("Sending sample data...")
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

        result = 0.0
        if self.encryption_mode == defs.ENC_MODE_FHE:
            # Request averaging operation to be performed by the server node
            request = { 'code' : defs.REQ_AVG_DATA,
                        'params' : { 'lower_idx' : 0, 
                                     'higher_idx' : 7 } }

            cx.send(str(request))

            # TODO (FHE Mode) Encrypt operation for sample data
            # TODO (FHE Mode) Transmit operation for sample data

            # Receive data from server node
            server_data = None

            msg = cx.receive()
            response = self.extract_content(msg)
            if response['code'] == defs.RESP_DATA:
                server_data = response['data']

            # Decrypt received data
            received_data = self.crypto_engine.decrypt(response['data'])

            result = received_data[0]

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
            received_data = self.crypto_engine.decrypt(response['data'])

            # Perform computation
            for i in range(0, len(received_data)):
                received_data[i] = received_data[i]

            if self.encryption_mode != defs.ENC_MODE_FHE:
                for d in received_data:
                    result += d

                result = result / len(received_data)

        end_time = time.time()

        # Show result and benchmark
        self.log("Comparing Results:")
        if self.encryption_mode != defs.ENC_MODE_FHE:
            self.log("Sample Data                    Received Data")
            for i in range(0, len(received_data)):
                match = 'O' if sample_data[i] == received_data[i] else 'X'
                self.log("{} : {:11.9f}                {:11.9f}".format(match, sample_data[i], received_data[i]))

        ave = 0.0
        for d in sample_data[0:7]:
            ave += d

        ave = ave / len(sample_data[0:7])

        self.log("Final Result: {}".format(result))
        self.log("Expected Result: {}".format(ave))

        self.log("   Time Elapsed: {}".format(end_time - start_time))

        # Close comms
        cx.close()

        return

