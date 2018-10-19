import defs
from crypto_engine import CryptoEngine

import struct
import base64
import os
import pickle

import seal
from seal import EncryptionParameters, \
                 SEALContext, \
                 KeyGenerator, \
                 PublicKey, \
                 SecretKey, \
                 PublicKey, \
                 Encryptor, \
                 Decryptor, \
                 Evaluator, \
                 FractionalEncoder, \
                 Ciphertext, \
                 Plaintext

class FHECryptoEngine(CryptoEngine):
    def __init__(self):
        CryptoEngine.__init__(self, defs.ENC_MODE_FHE)
        self.log_id = 'FHECryptoEngine'
        self.encrypt_params = None
        self.context = None
        self.encryptor = None
        self.evaluator = None
        self.decryptor = None

        return

    def load_keys(self):
        self.private_key = SecretKey()
        self.private_key.load(defs.FN_FHE_PRIVATE_KEY)

        self.public_key = PublicKey()
        self.public_key.load(defs.FN_FHE_PUBLIC_KEY)
        
        return True

    def generate_keys(self):
        if self.encrypt_params == None or \
           self.context == None:
            self.init_encrypt_params()

        keygen = KeyGenerator(self.context)

        # Generate the private key
        self.private_key = keygen.secret_key()
        self.private_key.save(defs.FN_FHE_PRIVATE_KEY)

        # Generate the public key
        self.public_key = keygen.public_key()
        self.public_key.save(defs.FN_FHE_PUBLIC_KEY)

        return True

    def init_encrypt_params(self):
        self.encrypt_params = EncryptionParameters()
        self.encrypt_params.set_poly_modulus("1x^2048 + 1")
        self.encrypt_params.set_coeff_modulus(seal.coeff_modulus_128(2048))
        self.encrypt_params.set_plain_modulus(1 << 8)

        self.context = SEALContext(self.encrypt_params)

        return

    def initialize(self, use_old_keys=False):
        # Initialize encryption params
        self.init_encrypt_params()

        # Check if the public & private key files exist
        if os.path.isfile(defs.FN_FHE_PUBLIC_KEY) and \
           os.path.isfile(defs.FN_FHE_PRIVATE_KEY) and \
           use_old_keys == True:

            self.log("Keys already exist. Reusing them instead.")
            if not self.load_keys():
                self.log("Failed to load keys")
                return False

        else:
            # If not, then attempt to generate new ones
            if not self.generate_keys():
                self.log("Failed to generate keys")
                return False

        # Setup the rest of the crypto engine
        self.encryptor = Encryptor(self.context, self.public_key)
        self.evaluator = Evaluator(self.context)
        self.decryptor = Decryptor(self.context, self.private_key)

        # Set the initialized flag
        self.initialized = True

        return True

    def encrypt(self, data):
        if not self.initialized:
            self.log("Not initialized")
            return False

        # Setup the encoder
        encoder = FractionalEncoder(self.context.plain_modulus(), self.context.poly_modulus(), 64, 32, 3)

        # Create the array of encrypted data objects
        encrypted_data = []
        for raw_data in data:
            encrypted_data.append(Ciphertext(self.encrypt_params))
            self.encryptor.encrypt( encoder.encode(raw_data), encrypted_data[-1] )

        # Pickle each Ciphertext, base64 encode it, and store it in the array
        for i in range(0, len(encrypted_data)):
            encrypted_data[i].save("fhe_enc.bin")
            encrypted_data[i] = base64.b64encode( pickle.dumps(encrypted_data[i]) )

        return encrypted_data

    def evaluate(self, encrypted_data, lower_idx=0, higher_idx=-1):
        result = Ciphertext()

        # Setup the encoder
        encoder = FractionalEncoder(self.context.plain_modulus(), self.context.poly_modulus(), 64, 32, 3)

        # Unpack the data first
        unpacked_data = []
        for d in encrypted_data[lower_idx:higher_idx]:
            unpacked_data.append(pickle.loads(base64.b64decode(d)))

        # Perform operations
        self.evaluator.add_many(unpacked_data, result)
        div = encoder.encode(1/len(unpacked_data))
        self.evaluator.multiply_plain(result, div)

        # Pack the result
        result = base64.b64encode( pickle.dumps(result) )

        return result

    def decrypt(self, raw_data):
        if not self.initialized:
            self.log("Not initialized")
            return False

        # Setup the encoder
        encoder = FractionalEncoder(self.context.plain_modulus(), self.context.poly_modulus(), 64, 32, 3)
        
        # Unpickle, base64 decode, and decrypt each ciphertext result
        decrypted_data = []
        for d in raw_data:
            encrypted_data = pickle.loads( base64.b64decode(d) )
            plain_data = Plaintext()
            self.decryptor.decrypt(encrypted_data, plain_data)
            decrypted_data.append( str(encoder.decode(plain_data)) )

        return decrypted_data

