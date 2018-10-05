import defs
import socket

from time import sleep

class NodeComm():
    def __init__(self):
        self.tx_host = defs.TX_HOST
        self.tx_port = defs.TX_PORT

        self.rx_host = defs.RX_HOST
        self.rx_port = defs.RX_PORT

        return

    def log(self, message):
        print("[NodeComm] {}".format(message))
        return

    def send(self, message):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.rx_host, self.rx_port))
            s.sendall(message.encode())

            s.shutdown(socket.SHUT_RDWR)
            s.close()

        return

    def receive(self):
        message = b''

        # Note: Partially copied from:
        #   https://docs.python.org/3/library/socket.html#example
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.rx_host, self.rx_port))
            s.listen(1)
            
            conn, addr = s.accept()
            with conn:
                self.log("Connected: {}".format(addr))
                while True:
                    data = conn.recv(defs.MAX_MSG_BUF)
                    if not data: break
                    message += data

            s.shutdown(socket.SHUT_RDWR)
            s.close()

        return message.decode()

