import defs
import subprocess
from time import sleep

from node_runner import NodeRunner
from crypto_engine import CryptoEngine, RSACryptoEngine, FHECryptoEngine

class EncryptedCommsTest():
    def __init__(self):
        self.encryption_mode = defs.ENC_MODE_FHE
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
                                    defs.NODE_SERVER, self.encryption_mode])

        sleep(2.0)

        subprocess.Popen(["python3", "node_runner.py", 
                                    defs.NODE_CLIENT, self.encryption_mode])

        return

if __name__ == "__main__":
    EncryptedCommsTest().run()

print("======================")
print("   Program Finished   ")
print("======================")

