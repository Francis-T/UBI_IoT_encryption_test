import time
import datetime
import os.path

import defs
from lwcp import LWCommProtocol
from node import Node

class NodeServer(Node):
    def __init__(self, enc_mode=defs.ENC_MODE_DEFAULT,
                       max_buf_size=defs.MAX_MSG_BUF,
                       data_size=defs.DEFAULT_DATA_SIZE):

        Node.__init__(self, enc_mode=enc_mode, data_size=data_size, max_buf_size=max_buf_size)
        self.log_id = 'NodeServer'
        self.max_buf_size = max_buf_size

        return

    def save_results(self):
        result_str = "{},{},{},{},{},{},{}\n".format(
                        str(datetime.datetime(1,1,1).now()),
                        self.max_buf_size,
                        self.data_size,
                        str(self.ts["overall"]["end"] - self.ts["overall"]["start"]),
                        str(self.ts["transmit_rcv"]["end"] - self.ts["transmit_rcv"]["start"]),
                        str(self.ts["transmit_xtr"]["end"] - self.ts["transmit_xtr"]["start"]),
                        str(self.ts["evaluate"]["end"] - self.ts["evaluate"]["start"]) )

        should_write_headers = False
        if not os.path.isfile(defs.FN_SERVER_LOG): 
            should_write_headers = True

        csv_file = open(defs.FN_SERVER_LOG, "a")
        if should_write_headers:
            csv_file.write("{},{},{},{},{},{},{}\n".format(
                                "ts",
                                "max_buf_size",
                                "data_size",
                                "overall",
                                "receive_data",
                                "extract_data",
                                "evaluate" ))
        csv_file.write(result_str)
        csv_file.close()
        return

    def run(self):
        # Initialize Encryption Engine
        self.init_crypto_engine(use_old_keys=True)

        # Initialize Comms
        cx = LWCommProtocol(max_buf_size=self.max_buf_size)
        cx.listen()

        self.ts["overall"]["start"] = time.time()
        # Wait for and receive data
        self.ts["transmit_rcv"]["start"] = time.time()
        msg = cx.receive()
        self.ts["transmit_rcv"]["end"] = time.time()
        # self.print_message(msg)

        # Store the sample data
        self.ts["transmit_xtr"]["start"] = time.time()
        data = self.extract_content(msg)
        self.ts["transmit_xtr"]["end"] = time.time()

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

            # self.log("Decoding request [{}]...".format(request['code']))
            if request['code'] == defs.REQ_AVG_DATA:
                lower_idx = request['params']['lower_idx']
                higher_idx = request['params']['higher_idx']

                self.ts["evaluate"]["start"] = time.time()
                result = self.crypto_engine.evaluate( data, lower_idx=lower_idx, higher_idx=higher_idx)
                self.ts["evaluate"]["end"] = time.time()
                response = { 'code' : defs.RESP_DATA,
                             'data' : [ result ] }

                # Transmit back evaluated sample data
                cx.send(str(response))

            elif request['code'] == defs.REQ_GET_DATA:
                lower_idx = request['params']['lower_idx']
                higher_idx = request['params']['higher_idx']

                response = { 'code' : defs.RESP_DATA,
                             'data' : data[lower_idx:higher_idx] }

                # Transmit back raw sample data
                cx.send(str(response))

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

                response = { 'code' : defs.RESP_DATA,
                             'data' : data[lower_idx:higher_idx] }

                # Transmit back raw sample data
                cx.send(str(response))

        self.ts["overall"]["end"] = time.time()

        # Show result and benchmark
        self.print_timestamps()
        self.save_results()

        # Close comms
        cx.close()

        return

