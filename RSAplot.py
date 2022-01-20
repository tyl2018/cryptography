from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import PKCS1_OAEP
import time, sys
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

def modexp(b, e, m): # e as a string showing the binary digits
    if m==1:
        return 0;
    c=0
    d=1
    for e_i in e:
        c *= 2
        d = d*d%m
        if e_i=='1':
            c += 1
            d = d*b%m
    return d

def RSAKeyGen(keysize):
    print("\tGenerating the key")
    t = time.time()
    key = RSA.generate(keysize)
    t = time.time() - t
    publicKey = key.publickey()
    ttlsize = sys.getsizeof(key.export_key())
    sendsize = sys.getsizeof(publicKey.export_key())
    return key, publicKey, t, ttlsize, sendsize
    
def RSAEncrypt(datasize, publicKey, plaintext):
    print("\tEncrypting")
    data = plaintext[:datasize]
    t = time.time()
    cipherRSA = PKCS1_OAEP.new(publicKey)
    ciphertext = cipherRSA.encrypt(data)
    t = time.time() - t
    return ciphertext, t
    
def RSADecrypt(cipher, key):
    print("\tdecrypting")
    t = time.time()
    cipherRSA = PKCS1_OAEP.new(key)
    data = cipherRSA.decrypt(cipher)
    t = time.time() - t
    return data, t

plaintext = b'Hello'
BitSize = [8, 16, 24, 32, 40]
keySize = [1413, 1745, 2800, 3200, 3800]
values = ['8bit', '16bit', '24bit', '32bit','40bit']

# values for ntru
N_NTRU = [167, 443, 491, 593, 743]
TimesEnc_NTRU = [0.155, 0.154, 0.15, 0.14, 0.15]
TimesDec_NTRU = [0.21, 0.21, 0.22, 0.21, 0.22]
Timekeygen_NTRU = [1.5, 3.5, 15, 25.7, 35]
hPluscipher_NTRU = [1750, 2550, 3040, 3319, 3851]
TotalSize_NTRU = [3000, 4145, 5400, 6000, 7000]

# values for rsa
N_RSA = [251, 401, 443, 491, 593, 743]
keySize_N_RSA = [1024, 2048, 3072, 4096, 7680, 15360]
TimesEnc_RSA = []
TimesDec_RSA = []
Timeskeygen_RSA = []
Deliver_RSA = []
TotalSize_RSA = []

# Encrypt/Decrypt time to data size
print("Encrypt/Decrypt time to data size")
for nd in range(1, 6):
    print("size:{}".format(nd))
    key, publicKey, t_gen, ttlsize, sendsize = RSAKeyGen(2048)
    ciphertext, t_enc = RSAEncrypt(nd, publicKey, plaintext)
    data, t_dec = RSADecrypt(ciphertext, key)
    if data != plaintext[:nd]:
        raise Exception("decrypted plaintext does not match")
    TimesEnc_RSA.append(t_enc)
    TimesDec_RSA.append(t_dec)

# Key generating time to key size
print("Key generating time to key size")
for nk in keySize:
    print("size:{}".format(nk))
    key, publicKey, t_gen, ttlsize, sendsize = RSAKeyGen(nk)
    Timeskeygen_RSA.append(t_gen)

# Deliver size and key size to N
print("Deliver size and key size to N")
for nk in keySize_N_RSA:
    print("size:{}".format(nk))
    key, publicKey, t_gen, ttlsize, sendsize = RSAKeyGen(nk)
    ciphertext, t_enc = RSAEncrypt(5, publicKey, plaintext)
    Deliver_RSA.append(sendsize+sys.getsizeof(ciphertext))
    TotalSize_RSA.append(ttlsize)

plt.figure(figsize=(16,8))

plt.subplot(2, 3, 1)
plt.plot(BitSize, TimesEnc_NTRU, label="NTRU")
plt.plot(BitSize, TimesEnc_RSA, label="RSA")
plt.title("Encryption")
plt.ylabel("Time(s)") # y label
plt.xticks(BitSize, values)
plt.yticks([0,0.1,0.2,0.3,0.4])
plt.legend()

plt.subplot(2, 3, 2)
plt.plot(BitSize, TimesDec_NTRU, label="NTRU")
plt.plot(BitSize, TimesDec_RSA, label="RSA")
plt.title("Decryption")
plt.ylabel("Time(s)") # y label
plt.xticks(BitSize, values)
plt.yticks([0,0.1,0.2,0.3,0.4])
plt.legend()

plt.subplot(2, 3, 3)
plt.plot(keySize, Timekeygen_NTRU, label="NTRU")
plt.plot(keySize, Timeskeygen_RSA, label="RSA")
plt.title("Keygen")
plt.xlabel("Key Size(bytes)") 
plt.ylabel("Time(s)") 
plt.legend()

plt.subplot(2, 3, 4)
plt.plot(N_NTRU, hPluscipher_NTRU, label="NTRU")
plt.plot(N_RSA, Deliver_RSA, label="RSA")
plt.title("Delivery Cost")
plt.xlabel("N")
plt.ylabel("Size(byte)") # y label
plt.legend()

plt.subplot(2, 3, 5)
plt.plot(N_NTRU, TotalSize_NTRU, label="NTRU")
plt.plot(N_RSA, TotalSize_RSA, label="RSA")
plt.title("Total key size")
plt.xlabel("N")
plt.ylabel("Size(byte)") # y label
plt.legend()

plt.savefig('result-ntru-rsa.png')
plt.show()