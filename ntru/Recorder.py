#!/usr/bin/env python3
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

def timeRecord(a):
    Times.append(a)
    print(Times)


'''
hello[
    string size = 5 bytes
    N = 167
    keygen : 1.6
    enc : 0.15
    dec : 0.22
]
'''

BitSize = [8, 16, 24, 32, 40]
keySize = [1413, 1745, 2800, 3200, 3800]
TimesEnc = [0.155, 0.154, 0.15, 0.14, 0.15]
TimesDec = [0.21, 0.21, 0.22, 0.21, 0.22]
Timekeygen = [1.5, 3.5, 15, 25.7, 35]

values = ['8bit', '16bit', '24bit', '32bit','40bit']

plt.figure(figsize=(16,8))

plt.subplot(2, 2, 1)
plt.plot(BitSize, TimesEnc)
plt.title("Encryption")
plt.ylabel("Time(s)") # y label
plt.xticks(BitSize, values)
plt.yticks([0,0.1,0.2,0.3,0.4])


plt.subplot(2, 2, 2)
plt.plot(BitSize, TimesDec)
plt.title("Decryption")
plt.ylabel("Time(s)") # y label
plt.xticks(BitSize, values)
plt.yticks([0,0.1,0.2,0.3,0.4])

plt.subplot(2, 2, 3)
plt.plot(keySize, Timekeygen)
plt.title("Keygen")
plt.xlabel("Key Size(bytes)") 
plt.ylabel("Time(s)") 


plt.savefig('result.png')
plt.show()
