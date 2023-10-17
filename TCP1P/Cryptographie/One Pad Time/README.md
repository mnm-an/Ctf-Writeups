# Challenge Name: One Time Pad
## Category: Cryptography

In the `One Pad Time` challenge, you are provided with two essential files: encrypt.py and output. Your objective is to decrypt the ct and get the flag.

#### `encrypt.py`:

```python
import os
import binascii
from pwn import xor
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

key = os.urandom(16)
iv = os.urandom(16)

cipher = AES.new(key, AES.MODE_CBC, iv)

pt = open("flag.txt", "rb").read()
ct = pad(cipher.encrypt(pt), 16)
ct = xor(ct,key)

print(f"{iv = }")
print(f"{ct = }")
```

#### `output`:

```
iv = b'\xf5\x8e\x85ye\xc8j(%\xc4K\xc1g#\x86\x1a'
ct = b'h\x08\xafmDV\xaa\xcd\xea\xe9C\xdd7/\x1fF\xe2?\xcb\xb0\x1d F\xcc\xe5\xa6\x9dTJ\\\xd1\x90\xac\xe0\x1c\x891}\x83*\x86\xee\xc4~\xa0\x18\xa8\x06\xea"{|\x0b\x92[\x9a[\x91\xc8\x19\xb7FK\x01\xb5\xf98\x80\x9bR)2\x84`\xb3E\t\xd5\xe5\xf0[\x83\xc6\x19\x82\r\x7f\xfaGF\xdb\xcb\xab\xd5~\x95\t\xdd\xb5E>F\xdd\xa9\xa6\x82\x86\xee"\x99\xd9\xcc\xaf\xce\xf0\'\xb3\xf4~\xcf\xdb\xc8\xbd3\x01\xd0,}]\xd5V\xd3?\xb0\xe7\xb4[4\x8a\xa2[\xa1TV\xd16\x1f\xbd"\xc8\xa2\\K\x16I%\xdaL\xc6\xfb\xb7f.\x98\xc3\xf4J\x1b\xe9TT\x83-\x98BO\xb4\x00~\xb5w\xcf7m\xa1\xea\xa9\xf6\xa6\xee\x00Y\xdfE\x9c7\xe3\xa3\xa2\x1f=.\x85\x08l\xacN\xfb2\x89\x8bB\x7f\x94\x91p\x10ep\x9b\x06oz\x87&U]J\x019\x12W\xce<\xc8\xa8\xb4v\xaf,\xb1n\x8b\xf5\xfe\xf8\r\xa7:r\xe8\xe0fvKN\\\xea\xe0\xa1\xe3\x99\xcc\xfd\x1a\x99Q\x90\xdf}\xae\xad'

```

The program use **AES-CBC mode**, in AES-CBC mode, data is divided into blocks, with each block XORed with the previous ciphertext before encryption. This chaining adds security by preventing patterns and enhancing data integrity during decryption.

Here is a image how **CBC Encryption And Decryption** Work :

![CBC-mode-encryption-and-decryption](https://github.com/mnm-an/Ctf-Writeups/assets/65871533/8c993cc0-a310-4978-bbba-a24655f49696)

**The script use a AES encryption in CBC (Cipher Block Chaining) mode, with random keys and initialization vectors (IVs). The plaintext is read from a flag file and encrypted. However, after analyzing the file, the vulnerability appears in the line** ```ct = pad(cipher.encrypt(pt), 16)```, **where padding is added. After encrypting the ciphertext, the program adds a 16-byte block of padding, which is** ```b'\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10'```. **Since the key size is 16 bytes, we can XOR it back to recover the key.**

### Solution : 

```python
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad,unpad
from pwn import xor

iv = b'\xf5\x8e\x85ye\xc8j(%\xc4K\xc1g#\x86\x1a'
ctxored = b'h\x08\xafmDV\xaa\xcd\xea\xe9C\xdd7/\x1fF\xe2?\xcb\xb0\x1d F\xcc\xe5\xa6\x9dTJ\\\xd1\x90\xac\xe0\x1c\x891}\x83*\x86\xee\xc4~\xa0\x18\xa8\x06\xea"{|\x0b\x92[\x9a[\x91\xc8\x19\xb7FK\x01\xb5\xf98\x80\x9bR)2\x84`\xb3E\t\xd5\xe5\xf0[\x83\xc6\x19\x82\r\x7f\xfaGF\xdb\xcb\xab\xd5~\x95\t\xdd\xb5E>F\xdd\xa9\xa6\x82\x86\xee"\x99\xd9\xcc\xaf\xce\xf0\'\xb3\xf4~\xcf\xdb\xc8\xbd3\x01\xd0,}]\xd5V\xd3?\xb0\xe7\xb4[4\x8a\xa2[\xa1TV\xd16\x1f\xbd"\xc8\xa2\\K\x16I%\xdaL\xc6\xfb\xb7f.\x98\xc3\xf4J\x1b\xe9TT\x83-\x98BO\xb4\x00~\xb5w\xcf7m\xa1\xea\xa9\xf6\xa6\xee\x00Y\xdfE\x9c7\xe3\xa3\xa2\x1f=.\x85\x08l\xacN\xfb2\x89\x8bB\x7f\x94\x91p\x10ep\x9b\x06oz\x87&U]J\x019\x12W\xce<\xc8\xa8\xb4v\xaf,\xb1n\x8b\xf5\xfe\xf8\r\xa7:r\xe8\xe0fvKN\\\xea\xe0\xa1\xe3\x99\xcc\xfd\x1a\x99Q\x90\xdf}\xae\xad'

paded = pad(b'',16)

key = xor(ctxored[len(ctxored)-16:len(ctxored)],paded)

cipher = AES.new(key,AES.MODE_CBC,iv)

ciphertext = xor(ctxored,key)
ciphertext = unpad(ciphertext,16)

plaintext = cipher.decrypt(ciphertext)

print("[+] FLAG FOUND : ",plaintext)

```

FLAG is :```b'TCP1P{why_did_the_chicken_cross_the_road?To_ponder_the_meaning_of_life_on_the_other_side_only_to_realize_that_the_road_itself_was_an_arbitrary_construct_with_no_inherent_purpose_and_that_true_enlightenment_could_only_be_found_within_its_own_existence_1234}'```

