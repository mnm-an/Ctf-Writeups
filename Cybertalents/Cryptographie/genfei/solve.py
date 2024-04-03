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
