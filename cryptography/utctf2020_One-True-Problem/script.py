from codecs import decode

def nonrepeatxor(text, key):
	sk = len(key)
	for i in range(0, 2 * sk, 2):
		x = int(text[i:i + 2], 16)
		y = ord(key[i // 2])
		if (x ^ y > 31):
			print(chr(x ^ y), end='')
		else:
			print('\\x%x' % (x ^ y), end='')

def run():
	st = len(c1)
	sk = len(key)

	nonrepeatxor(c1, key)
	print ((st - sk) * '?')
	nonrepeatxor(c2, key)
	print ((st - sk) * '?')

c1 = '213c234c2322282057730b32492e720b35732b2124553d354c22352224237f1826283d7b0651'
c2 = '3b3b463829225b3632630b542623767f39674431343b353435412223243b7f162028397a103e'

print ("The key is: ", end='')
nonrepeatxor(c1, 'utflag{')
key = "THE BES"

print ("\nCommandline:")
