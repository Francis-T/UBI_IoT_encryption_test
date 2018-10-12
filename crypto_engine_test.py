import sys
import time
from crypto_engine import FHECryptoEngine, RSACryptoEngine

def test(ce):
    start_time = time.time()
    ce.initialize(True)

    raw_data = [ 1.0, 3.0, 2345423535.0, 54.245 ]
    encrypted_data = ce.encrypt(raw_data)

    for d in encrypted_data:
        print("{} : {}".format(len(d), d[0:30]))

    decrypted_data = ce.decrypt(encrypted_data)

    for d in decrypted_data:
        print("{} : {}".format(sys.getsizeof(d), d))
    
    end_time = time.time()

    print("Execution Time: {}".format(str(end_time - start_time)))

def test_eval(ce):
    start_time = time.time()
    ce.initialize(True)

    raw_data = [ 1.0, 3.0, 2345423535.0, 54.245 ]
    encrypted_data = ce.encrypt(raw_data)

    result = ce.evaluate(encrypted_data)

    decrypted_data = ce.decrypt([result])

    for d in decrypted_data:
        print("{} : {}".format(sys.getsizeof(d), d))
    
    end_time = time.time()

    print("Execution Time: {}".format(str(end_time - start_time)))
    ave = 0.0
    for d in raw_data: ave += d
    ave = ave / len(raw_data)

    print("Expected Result: {}".format(ave))


# test(FHECryptoEngine())
test_eval(FHECryptoEngine())

# test(RSACryptoEngine())


