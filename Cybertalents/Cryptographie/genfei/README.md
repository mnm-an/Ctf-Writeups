# Challenge Name: genfei
## Category: Cryptography
### [Challenge Link](https://cybertalents.com/challenges/cryptography/genfei)

In this challenge, participants were presented with two files: encrypt.py and flag.enc. The goal was to decrypt the contents of flag.enc by reverse-engineering the encryption algorithm defined in encrypt.py.
#### `encrypt.py`:

```python
# -*- coding:utf-8 -*-

import sys
from struct import pack, unpack

def F(w):
	return ((w * 31337) ^ (w * 1337 >> 16)) % 2**32

def encrypt(block):
	a, b, c, d = unpack("<4I", block)
	for rno in xrange(32):
		a, b, c, d = b ^ F(a | F(c ^ F(d)) ^ F(a | c) ^ d), c ^ F(a ^ F(d) ^ (a | d)), d ^ F(a | F(a) ^ a), a ^ 31337
		a, b, c, d = c ^ F(d | F(b ^ F(a)) ^ F(d | b) ^ a), b ^ F(d ^ F(a) ^ (d | a)), a ^ F(d | F(d) ^ d), d ^ 1337
	return pack("<4I", a, b, c, d)

pt = open(sys.argv[1]).read()
while len(pt) % 16: pt += "#"

ct = "".join(encrypt(pt[i:i+16]) for i in xrange(0, len(pt), 16))
open(sys.argv[1] + ".enc", "w").write(ct)

```
### Analysis: 
Upon examining encrypt.py, it was discovered that the encryption algorithm involves a series of transformations applied to the input plaintext. The algorithm is iterative, executing a loop a fixed number of times, with each iteration involving a set of operations on the data. The key operations include bitwise XOR operations and modular arithmetic.

**Encryption function:**

The encryption function defined in encrypt.py accepts a block of data and applies a series of transformations to it. These transformations are controlled by a loop that iterates 32 times. Within each iteration, the block is manipulated using bitwise XOR operations and modular arithmetic operations based on the input values a, b, c, and d.

**Decryption Approach:**

To decrypt the encrypted data, a reverse-engineering approach was employed. The provided decryption function in decrypt attempts to reverse the operations applied during encryption by iteratively applying inverse operations. By carefully reversing each step of the encryption process, the original plaintext can be recovered.

    Understanding the role of the F function was crucial for decrypting the data. By analyzing the F function, which involves bitwise XOR and bit shifting operations, it was possible to devise the inverse operations required for decryption.
    Reverse-engineering the encryption algorithm required careful analysis of the operations applied at each iteration of the encryption loop. By understanding the sequence of operations, it became possible to devise a strategy for reversing these operations during decryption.

#### `decrypt.py`:
```python
from struct import pack, unpack


def F(w):
	return ((w * 31337) ^ (w * 1337 >> 16)) % 2**32

def encrypt(block):
	a, b, c, d = unpack("<4I", block)
	for rno in xrange(32):
		a, b, c, d = b ^ F(a | F(c ^ F(d)) ^ F(a | c) ^ d), c ^ F(a ^ F(d) ^ (a | d)), d ^ F(a | F(a) ^ a), a ^ 31337
		a, b, c, d = c ^ F(d | F(b ^ F(a)) ^ F(d | b) ^ a), b ^ F(d ^ F(a) ^ (d | a)), a ^ F(d | F(d) ^ d), d ^ 1337
	return pack("<4I", a, b, c, d)

def decrypt(block):
        a, b, c, d = unpack("<4I", block)
        for rno in range(32):
            d1 = d ^ 1337
            a1 = F(d1 | F(d1) ^ d1) ^ c
            b1 = b ^ F(d1 ^ F(a1) ^ (d1 | a1))
            c1 = a ^ F(d1 | F(b1 ^ F(a1)) ^ F(d1 | b1) ^ a1)        
            a = d1 ^ 31337
            d = c1 ^ F(a | F(a) ^ a)
            c = F(a ^ F(d) ^ (a | d)) ^ b1
            b = a1 ^ F(a | (F(c ^ F(d)) ^ F(a | c) ^ d))
        return pack("<4I", a, b, c, d)


ct = open("flag.enc", "rb").read()
print(ct)
pt = b"".join(decrypt(ct[i:i+16]) for i in range(0, len(ct), 16))




```


