import time
import datetime
import struct
import os.path
import sys

import defs
from lwcp import LWCommProtocol
from node import Node

LOWER_IDX = 0
HIGHER_IDX = -1

class NodeClient(Node):
    def __init__(self, enc_mode=defs.ENC_MODE_DEFAULT,
                       max_buf_size=defs.MAX_MSG_BUF,
                       data_size=defs.DEFAULT_DATA_SIZE):

        Node.__init__(self, enc_mode=enc_mode, data_size=data_size, max_buf_size=max_buf_size)
        self.log_id = 'NodeClient'
        self.ave_encrypted_data_size = 0.0

        return

    def log(self, message):
        print("[NodeClient] {}".format(message))
        return

    def save_results(self):
        for key in self.ts.keys():
            if self.ts[key]["start"] == None:
                self.ts[key]["start"] = 0

            if self.ts[key]["end"] == None:
                self.ts[key]["end"] = 0

        result_str = "{},{},{},{},{},{},{},{},{},{},{},{},{}\n".format(
                        self.encryption_mode,
                        str(datetime.datetime(1,1,1).now()),
                        self.max_buf_size,
                        self.data_size,
                        str(self.ts["overall"]["end"] - self.ts["overall"]["start"]),
                        str(self.ts["encrypt"]["end"] - self.ts["encrypt"]["start"]),
                        str(self.ts["transmit"]["end"] - self.ts["transmit"]["start"]),
                        str(self.ts["transmit_ack"]["end"] - self.ts["transmit_ack"]["start"]),
                        str(self.ts["req_result"]["end"] - self.ts["req_result"]["start"]),
                        str(self.ts["decrypt"]["end"] - self.ts["decrypt"]["start"]),
                        str(self.cx.get_max_received_message_size()),
                        str(self.cx.get_max_sent_message_size()),
                        str(self.ave_encrypted_data_size) )

        should_write_headers = False
        if not os.path.isfile(defs.FN_CLIENT_LOG): 
            should_write_headers = True

        csv_file = open(defs.FN_CLIENT_LOG, "a")
        if should_write_headers:
            csv_file.write("{},{},{},{},{},{},{},{},{},{},{},{},{}\n".format(
                                "enc_mode",
                                "ts",
                                "max_buf_size",
                                "data_size",
                                "overall",
                                "encrypt",
                                "transmit",
                                "transmit_acknowledge",
                                "request_results",
                                "decrypt",
                                "max_received_size",
                                "max_sent_size",
                                "ave_enc_data_size" ))

        csv_file.write(result_str)
        csv_file.close()
        return

    def run(self):
        # Initialize Encryption Engine
        self.init_crypto_engine(use_old_keys=True)

        # Initialize Comms
        self.cx = LWCommProtocol(max_buf_size=self.max_buf_size)
        self.cx.connect()

        # Create the sample data
        sample_data = self.generate_data()

        self.ts["overall"]["start"] = time.time()

        # Encrypt the sample data
        self.ts["encrypt"]["start"] = time.time()
        encrypted_sample_data = self.crypto_engine.encrypt(sample_data)
        self.ts["encrypt"]["end"] = time.time()

        ave = 0.0
        for enc_data in encrypted_sample_data:
            ave += sys.getsizeof(enc_data)

        self.ave_encrypted_data_size = ave / len(encrypted_sample_data)

        # Transmit the sample data
        self.log("Sending sample data...")
        self.ts["transmit"]["start"] = time.time()
        self.cx.send(str(encrypted_sample_data))
        self.ts["transmit"]["end"]   = time.time()

        # Receive server acknowledge
        self.ts["transmit_ack"]["start"] = time.time()
        msg = self.cx.receive()
        response = self.extract_content(msg)
        if response == None:
            self.log("Error: Node Server ACK not received!")
            self.cx.close()
            return

        if response['code'] != defs.RESP_ACK:
            self.log("Error: Node Server ACK not received!")
            self.cx.close()
            return

        self.ts["transmit_ack"]["end"] = time.time()

        result = 0.0
        if self.encryption_mode == defs.ENC_MODE_FHE:
            self.ts["req_result"]["start"] = time.time()
            # Request averaging operation to be performed by the server node
            request = { 'code' : defs.REQ_AVG_DATA,
                        'params' : { 'lower_idx' : LOWER_IDX, 
                                     'higher_idx' : HIGHER_IDX } }

            self.cx.send(str(request))

            # TODO (FHE Mode) Encrypt operation for sample data
            # TODO (FHE Mode) Transmit operation for sample data

            # Receive data from server node
            server_data = None

            msg = self.cx.receive()
            response = self.extract_content(msg)
            if response['code'] == defs.RESP_DATA:
                server_data = response['data']

            self.ts["req_result"]["end"] = time.time()

            # Decrypt received data
            self.ts["decrypt"]["start"] = time.time()
            received_data = self.crypto_engine.decrypt(response['data'])
            self.ts["decrypt"]["end"]   = time.time()

            result = received_data[0]

        elif self.encryption_mode == defs.ENC_MODE_RSA:
            # Request sample data from server node
            request = { 'code' : defs.REQ_GET_DATA,
                        'params' : { 'lower_idx' : LOWER_IDX, 
                                     'higher_idx' : HIGHER_IDX } }
            self.cx.send(str(request))

            # Receive data from server node
            server_data = None

            msg = self.cx.receive()
            response = self.extract_content(msg)
            if response['code'] == defs.RESP_DATA:
                server_data = response['data']

            # Decrypt received data
            self.ts["decrypt"]["start"] = time.time()
            received_data = self.crypto_engine.decrypt(response['data'])
            self.ts["decrypt"]["end"]   = time.time()

            # Perform computation
            for i in range(0, len(received_data)):
                received_data[i] = received_data[i]

            if self.encryption_mode != defs.ENC_MODE_FHE:
                for d in received_data:
                    result += d

                result = result / len(received_data)

        self.ts["overall"]["end"] = time.time()

        # Show result and benchmark
        self.log("Comparing Results:")
        if self.encryption_mode != defs.ENC_MODE_FHE:
            self.log("Sample Data                    Received Data")
            for i in range(0, len(received_data)):
                match = 'O' if sample_data[i] == received_data[i] else 'X'
                self.log("{} : {:11.9f}                {:11.9f}".format(match, sample_data[i], received_data[i]))

        # TODO Move this to a function
        ave = 0.0
        for d in sample_data[LOWER_IDX:HIGHER_IDX]:
            ave += d

        ave = ave / len(sample_data[LOWER_IDX:HIGHER_IDX])

        self.log("Final Result: {}".format(result))
        self.log("Expected Result: {}".format(ave))

        self.print_timestamps()
        self.save_results()

        # Close comms
        self.cx.close()

        return

