import defs
import subprocess
from time import sleep
from sys import argv

from node_runner import NodeRunner
from crypto_engine import CryptoEngine, RSACryptoEngine, FHECryptoEngine

class EncryptedCommsTest():
    def __init__(self, max_buf_size=defs.MAX_MSG_BUF,
                       data_size=defs.DEFAULT_DATA_SIZE):

        self.encryption_mode = defs.ENC_MODE_FHE
        self.max_buf_size = int(max_buf_size)
        self.data_size = int(data_size)

        return

    def log(self, message):
        print("[Main] {}".format(message))
        return

    def generate_encrypt_keys(self):
        if self.encryption_mode == defs.ENC_MODE_RSA:
            RSACryptoEngine().generate_keys()

        elif self.encryption_mode == defs.ENC_MODE_FHE:
            FHECryptoEngine().generate_keys()

        return

    def run(self):
        # Pre-generate the encryption keys
        self.generate_encrypt_keys()

        # Start Node Runner Subprocesses
        subprocess.Popen(["python3", "node_runner.py", 
                                    defs.NODE_SERVER, 
                                    self.encryption_mode, 
                                    str(self.data_size),
                                    str(self.max_buf_size)])

        sleep(2.0)

        subprocess.Popen(["python3", "node_runner.py", 
                                    defs.NODE_CLIENT,
                                    self.encryption_mode, 
                                    str(self.data_size),
                                    str(self.max_buf_size)])

        return

if __name__ == "__main__":
    data_size = argv[1] if len(argv) >= 2 else str(defs.DEFAULT_DATA_SIZE)
    buf_size  = argv[2] if len(argv) >= 3 else str(defs.MAX_MSG_BUF)
    print(data_size + " " + buf_size)
    EncryptedCommsTest(max_buf_size=buf_size, data_size=data_size).run()

print("======================")
print("   Program Finished   ")
print("======================")

