import defs
import subprocess
import os

from Crypto.PublicKey import RSA
from time import sleep
from node_runner import NodeRunner

class EncryptedCommsTest():
    def __init__(self):
        self.encryption_mode = defs.ENC_MODE_DEFAULT
        return

    def log(self, message):
        print("[Main] {}".format(message))
        return

    def init_encryption_keys(self):
        # Check if the public key file exists
        if os.path.isfile('public.key') == True and os.path.isfile('private.key'):
            self.log("Keys already exist. Reusing them instead.")
            return

        # Generate the key
        self.log("Generating keys...")
        new_key = RSA.generate(4096, e=65537)

        # Export the public key
        self.log("Writing public key...")
        file_pub_key = open("public.key", "wb")
        file_pub_key.write(new_key.public_key().exportKey("PEM"))
        file_pub_key.close()

        # Export the private key
        self.log("Writing private key...")
        file_priv_key = open("private.key", "wb")
        file_priv_key.write(new_key.export_key("PEM"))
        file_priv_key.close()

        return

    def run(self):
        # Initialize the encryption keys
        if self.encryption_mode == defs.ENC_MODE_RSA:
            self.init_rsa_encryption_keys()

        # Start Node Runner Subprocesses
        subprocess.Popen(["python3", "node_runner.py", 
                                    defs.NODE_SERVER, self.encryption_mode])

        sleep(1.0)
        subprocess.Popen(["python3", "node_runner.py", 
                                    defs.NODE_CLIENT, self.encryption_mode])

        return

if __name__ == "__main__":
    EncryptedCommsTest().run()

print("======================")
print("   Program Finished   ")
print("======================")

