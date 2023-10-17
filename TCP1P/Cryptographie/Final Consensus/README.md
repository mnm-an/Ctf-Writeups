# Challenge Name: Final Consensus
## Category: Cryptography

In the `Final Consensus` challenge, it was part of an online Capture The Flag (CTF) competition. Participants were provided with the source code of a Python program that used the AES encryption algorithm in ECB (Electronic Codebook) mode. This source code was hosted on a Netcat server, allowing participants to both observe Alice's encrypted message and provide their own input for encryption. The goal was to decrypt **Alice's message**, which contained the hidden flag. Here is the source code :

```python
from Crypto.Cipher import AES
import random
from Crypto.Util.Padding import pad

a = b""
b = b""
FLAG = b"TCP1P{REDACTED}"

def generateKey():
	global a, b
	a = (str(random.randint(0, 999999)).zfill(6)*4)[:16].encode()
	b = (str(random.randint(0, 999999)).zfill(6)*4)[:16].encode()

def encrypt(plaintext, a, b):
	cipher = AES.new(a, mode=AES.MODE_ECB)
	ct = cipher.encrypt(pad(plaintext, 16))
	cipher = AES.new(b, mode=AES.MODE_ECB)
	ct = cipher.encrypt(ct)
	return ct.hex()

def main():
	generateKey()
	print("Alice: My message", encrypt(FLAG, a, b))
	print("Alice: Now give me yours!")
	plain = input(">> ")
	print("Steve: ", encrypt(plain.encode(), a, b))
	print("Alice: Agree.")


if __name__ == '__main__':
	main()

```

The encryption method uses **AES encryption with ECB mode**. It generates random keys **a** and **b**, encrypt the FLAG, and print it as Alice's message, along with requesting an input from the user, which is also encrypted and printed as **Steve's message**.

Here is a image how **ECB Encryption And Decryption** Work :

![ECB-mode-encryption-and-decryption](https://github.com/mnm-an/Ctf-Writeups/assets/65871533/c461c1e0-2fc9-4e90-b409-550804de673a)


**In ECB encryption, each plaintext block is independently encrypted with the same key. The encryption process involves dividing the input into fixed-size blocks (e.g., 128 bits), and each block is encrypted separately, producing its corresponding ciphertext block. This means that identical plaintext blocks will result in identical ciphertext blocks**.

### Decryption Approach :

To reveal the flag, you need to perform a **Meet-in-the-Middle (MITM) attack** .
the Meet-in-the-Middle (MITM) attack involves finding the correct combination of keys **a** and **b** used for encrypting **my_input**. You can input any message, and it's encrypted first with **a** and then with **b**, resulting the output **my_input_encrypted**.

To discover **a** and **b** : 

1 - you encrypt your plaintext with all possible keys and store the results in **encrypted{}**.  

2 - you decrypt **my_input_encrypted**  with all possible keys and store the results in **decrypted{}**.

```encrypted{}``` and ```decrypted{}``` are dictionaries that store ciphertexts alongside the corresponding encryption or decryption keys, serving as key-value pairs for convenient data storage and retrieval during the Meet-in-the-Middle (MITM) attack.

If a match is found, it reveals the **MITM value**, leading to the discovery of keys **a** and **b**.

Decryption Code is provided for this MITM attack, where the keys are systematically tested to find the matching pair that decrypts **my_input_encrypted** to reveal **Alice's message (The Flag)**.
```python
from Crypto.Cipher import AES
from pwn import xor
import binascii

my_input_encrypted = b'0b3b31271629057f41ec84263b656eb97cb525dbc37ea0b73c520abd1949f9ae'
ct = binascii.unhexlify(my_input_encrypted[:32])
my_input = b'aaaaaaaaaaaaaaaa'
alice_message = '99d547aa5610289788e1766deedb6aef28f05196b96e10fa5819dcb35a3d5181d9cf1d49606d035f00588e845a3b519fcb58f20ed877dd68ee955a29344a55ce26cf27f881e48ed122ad5288185037c9'

keys = []
for i in range(1000000):
        keys.append((str(i).zfill(6)*4)[:16].encode())

def decrypt(ct, a, b):
	cipher = AES.new(b, mode=AES.MODE_ECB)
	ct = cipher.decrypt(ct)
	cipher = AES.new(a, mode=AES.MODE_ECB)
	ct = cipher.decrypt(ct)
	return ct

encrypted = {}
for i in range(len(keys)) :
        cipher = AES.new(keys[i], mode=AES.MODE_ECB)
        encrypted[cipher.encrypt(my_input).hex()] = i


for key in keys:
        cipher = AES.new(key, mode=AES.MODE_ECB)
        x = cipher.decrypt(ct).hex()
        if x in encrypted:
                b = key
                a = keys[encrypted[x]]
                print("[+] Key Founds ! a = ",a," \n b = ",b)
                print("[+]mitm Value : ",x)
                break


print("FLAG is : ",decrypt(binascii.unhexlify(alice_message),a,b))

```
FLAG is : ```b'TCP1P{nothing_ever_lasts_forever_everybody_wants_to_rule_the_world}'```



