import defs
import socket

import time
from time import sleep

class NodeComm():
    def __init__(self, max_buf_size=defs.MAX_MSG_BUF):
        self.tx_host = defs.TX_HOST
        self.tx_port = defs.TX_PORT

        self.rx_host = defs.RX_HOST
        self.rx_port = defs.RX_PORT
        
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn = None
        self.conn_addr = None
        self.role = defs.ROLE_UNKNOWN
        
        self.max_buf_size = max_buf_size

        self.max_rx_msg_size = 0
        self.max_tx_msg_size = 0
    
        return

    def log(self, message):
        print("[NodeComm] {}".format(message))
        return

    def get_max_received_message_size(self):
        return self.max_rx_msg_size

    def get_max_sent_message_size(self):
        return self.max_tx_msg_size

    def listen(self):
        # Note: Partially copied from:
        #   https://docs.python.org/3/library/socket.html#example
        self.role = defs.ROLE_SERVER
        self.sock.bind((self.rx_host, self.rx_port))
        self.sock.listen(1)
        self.conn, self.conn_addr = self.sock.accept()
        # self.log("Connected: {}".format(self.conn_addr))

        return
    
    def connect(self):
        self.role = defs.ROLE_CLIENT
        self.sock.connect((self.rx_host, self.rx_port))

        return

    def send(self, message):
        send_func = None
        if self.role == defs.ROLE_CLIENT:
            send_func = self.sock.send

        elif self.role == defs.ROLE_SERVER:
            send_func = self.conn.send

        else:
            self.log("Warning: Invalid role for send")
            self.log("Send failed")
            return

        buf = message.encode()
        bytes_sent = 0
        bytes_next = 0

        start_time = time.time()
        while bytes_sent < len(buf) - 1:
            if ((bytes_sent + self.max_buf_size) >= len(buf)):
                bytes_next = len(buf)
            else:
                bytes_next = bytes_sent + self.max_buf_size

            bytes_sent += send_func( buf[bytes_sent:bytes_next])
            # self.log("Time Elapsed: {}".format(time.time() - start_time))
            # self.log("Bytes Sent: {}".format(bytes_sent))

        message_size = len(buf) / 1000
        elapsed_time = (time.time() - start_time)

        self.log("Stats:")
        self.log("    Tx Rate: {:5.2f} kb/sec".format(message_size / elapsed_time))
        self.log("    Message Size: {} kb".format(message_size))
        self.log("    Elapsed Time: {} sec".format(elapsed_time))

        if self.max_tx_msg_size < message_size:
            self.max_tx_msg_size = message_size

        return

    def receive(self):
        recv_func = None
        if self.role == defs.ROLE_CLIENT:
            recv_func = self.sock.recv

        elif self.role == defs.ROLE_SERVER:
            recv_func = self.conn.recv

        else:
            self.log("Warning: Invalid role for receive")
            self.log("Receive failed")
            return

        message = b''

        start_time = time.time()
        while True:
            data = recv_func(self.max_buf_size)
            if not data: 
                self.log("No data received")
                break

            message += data

            if len(data) < self.max_buf_size: 
                self.log("Length is less than max")
                break

            # self.log("Time Elapsed: {}".format(time.time() - start_time))
            # self.log("Bytes Received: {}".format(len(data)))

        message_size = len(message) / 1000
        elapsed_time = (time.time() - start_time)

        self.log("Stats:")
        self.log("    Rx Rate: {:5.2f} kb/sec".format(message_size / elapsed_time))
        self.log("    Message Size: {} kb".format(message_size))
        self.log("    Elapsed Time: {} sec".format(elapsed_time))

        if self.max_rx_msg_size < message_size:
            self.max_rx_msg_size = message_size

        return message.decode()

    def close(self):
        # If server side, notify clients of shutdown
        if self.role == defs.ROLE_SERVER:
            msg = self.receive()
            self.log(msg)
            self.sock.shutdown(socket.SHUT_RDWR)

        else:
            self.sock.shutdown(socket.SHUT_RDWR)

        self.log("Closing socket...")
        self.sock.close()
        self.log("Done")

        return

