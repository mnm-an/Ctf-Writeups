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
