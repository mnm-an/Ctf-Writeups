import itertools
import random

W = 7
a = [0,1,2,3,4,5,6]

#Encrypt
'''
msg = open("redacted.txt").read().strip()
while len(msg) % (2*W): 
    msg += "."                    # Padding with '.' , Block size = 14bytes

for i in range(100):
    msg = msg[1:] + msg[:1]
    msg = msg[0::2] + msg[1::2]
    msg = msg[1:] + msg[:1]
    res = ""
    for j in range(0, len(msg), W):
        for k in range(W):
            res += msg[j:j+W][perm[k]]
    msg = res

print(msg)
'''
#Decrypt

shuffled = list(itertools.permutations(a))            
           
for s in shuffled:
    msg = 'L{NTP#AGLCSF.#OAR4A#STOL11__}PYCCTO1N#RS.S'
    for i in range(100):
        res = ''
        for j in range(0, len(msg), W):
            for k in range(W):
                res += msg[j:j + W][s.index(k)]
        msg = res
        msg = msg[-1] + msg[:-1]
        msg = ''.join([msg[i // 2] if i % 2 == 0 else msg[len(msg) // 2 + i // 2] for i in range(len(msg))])
        msg = msg[-1] + msg[:-1]

    if 'FLAG{' in msg:
        print("[+] FLAG FOUND! : ", msg)
        break
                
