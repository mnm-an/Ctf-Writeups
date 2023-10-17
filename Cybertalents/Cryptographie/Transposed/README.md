# Challenge Name: Transposed
## Category: Cryptography
### [Challenge Link](https://cybertalents.com/challenges/cryptography/transposed)

In the "Transposed" challenge, you are provided with two files: `encrypt.py` and `decrypt.py`. The objective is to decrypt the message encoded by the encryption script and recover the hidden flag.

#### `encrypt.py`:

```python
# -*- coding:utf-8 -*-

import random

W = 7
perm = range(W)
random.shuffle(perm)

msg = open("flag.txt").read().strip()
while len(msg) % (2 * W):
    msg += "."

for i in range(100):
    msg = msg[1:] + msg[:1]
    msg = msg[0::2] + msg[1::2]
    msg = msg[1:] + msg[:1]
    res = ""
    for j in range(0, len(msg), W):
        for k in range(W):
            res += msg[j:j + W][perm[k]]
    msg = res

print(msg)
```
### Output: L{NTP#AGLCSF.#OAR4A#STOL11__}PYCCTO1N#RS.S
The encryption algorithm shuffles a tuple of numbers from 0 to 6 **(range(7))** and uses this shuffled tuple to encrypt the flag after shuffling the flag itself.

#### `decrypt.py`:
```python
import itertools

a = [0, 1, 2, 3, 4, 5, 6]  # range(7)
W = 7
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
        msg = ''.join([msg[i // 2] if i % 2 == 0 else msg[len(msg) // 2 + i // 2] for i in range len(msg)])
        msg = msg[-1] + msg[:-1]

    if 'FLAG{' in msg:
        print("[+] FLAG FOUND! : ", msg)
        break
```
The decryption script tries all possible permutations of the shuffled tuple and uses the reverse encryption algorithm to find the flag, which starts with "FLAG{". When the flag is found, it prints the result.

Good luck with the challenge!
