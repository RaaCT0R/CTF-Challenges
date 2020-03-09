## Challenge name: ALEXCTF CR2: MANY TIME SECRETS
### Difficulty:	medium

### Description:
> This time Fady learned from his old mistake and decided to use onetime pad as his encryption technique, but he never knew why people call it one time pad! Flag will start with ALEXCTF{. 
> 
> P.S: given file: ctflearn-p177-file

### Solution:

One time pad is an encryption algorithm using an unique key same length of the text. But look what we have here: "but he never knew why people call it one time pad!". So we guess there should be a key with length less than text's length.
Look at the file, we saw 11 lines. My guess, all of them have same key!
lets try the guess!

Implement 3 functions for the test:

	import codecs

	def nonrepeatxor(text, key):
		sk = len(key)
		for i in range(0, 2 * sk, 2):
			x = int(text[i:i + 2], 16)
			y = ord(key[i // 2])
			print(chr(x ^ y), end='')

	def repeatxor(text, key):
		st = len(text)
		sk = len(key)
		empty=""
		for i in range(0, st, 2):
			x = int(text[i:i + 2], 16)
			y = ord(key[(i // 2) % sk])
			print(chr(x ^ y), end='')
	
	def listxorfunc(a, fm):
		for i in range(len(a)):
			nonrepeatxor(a[i], fm)
			print()

Define ***a*** as a list, and ***fm*** as a variable, then use ***nonrepeatxor*** function for all lines.

	a = ['0529242a631234122d2b36697f13272c207f2021283a6b0c7908'
	,'2f28202a302029142c653f3c7f2a2636273e3f2d653e25217908'
	,'322921780c3a235b3c2c3f207f372e21733a3a2b37263b313012'
	,'2f6c363b2b312b1e64651b6537222e37377f2020242b6b2c2d5d'
	,'283f652c2b31661426292b653a292c372a2f20212a316b283c09'
	,'29232178373c270f682c216532263b2d3632353c2c3c2a293504'
	,'613c37373531285b3c2a72273a67212a277f373a243c20203d5d'
	,'243a202a633d205b3c2d3765342236653a2c7423202f3f652a18'
	,'2239373d6f740a1e3c651f207f2c212a247f3d2e65262430791c'
	,'263e203d63232f0f20653f207f332065262c3168313722367918'
	,'2f2f372133202f142665212637222220733e383f2426386b']

	fm = 'ALEXCTF{'
	listxorfunc(a, fm)

**Output**
	
    Dear Fri
	nderstoo
	sed One
	n scheme
	is the o
	hod that
	 proven
	ever if
	cure, Le
	gree wit
	ncryptio

We got meaningful words! For example, first line is "Dear Friend ...".
Now we guess the words, XOR missing characters with their pairs in the list, find the key! 
Lets implement 2 functions to make things easier:
	
	def hexstrxorstr(t1, t2):
	output = ''
	for i in range(len(t2)):
		output += chr(int(t1[2*i:2*i+2], 16) ^ ord(t2[i]))
	return output
			
	def updatekey(a, fm, index, pt):
		x = hexstrxorstr(a[index][len(fm)*2:len(fm)*2+len(pt)*2], pt)
		print("Result: ", end='')
		print(x)
		fm += x
		print("New key: ", end='')
		print(fm)
		return fm

Run the code with the command inspect, using this:

	python -i code.py

After saw the output, run this:
	
	fm = updatekey(a, fm, 0, 'end')

**output**

	>>> updatekey(a, fm, 0, 'end')
	Result: HER
	New key: ALEXCTF{HER

lets see the text again:

	listxorfunc(a, fm)

**output**

	>>> listxorfunc(a,fm)
	Dear Friend
	nderstood m
	sed One tim
	n scheme, I
	is the only
	hod that is
	 proven to
	ever if the
	cure, Let M
	gree with m
	ncryption s

Line 3, it should be "time"! and continue with " pad", that's it, "One time pad"!

	fm = updatekey(a, fm, 2, 'e pad')

**output**

	>>> fm = updatekey(a, fm, 2, 'e pad')
	Result: E_GOE
	New key: ALEXCTF{HERE_GOE

Repeat this procedure, complete the flag (showing below how i complete the flag):

	>>> listxorfunc(a,fm)
	Dear Friend, Thi
	nderstood my mis
	sed One time pad
	n scheme, I hear
	is the only encr
	hod that is math
	 proven to be no
	ever if the key
	cure, Let Me kno
	gree with me to
	ncryption scheme
	>>> fm = updatekey(a, fm, 4, 'ypt')
	Result: S_T
	New key: ALEXCTF{HERE_GOES_T
	>>> listxorfunc(a,fm)
	Dear Friend, This t
	nderstood my mistak
	sed One time pad en
	n scheme, I heard t
	is the only encrypt
	hod that is mathema
	 proven to be not c
	ever if the key is
	cure, Let Me know i
	gree with me to use
	ncryption scheme al
	>>> fm = updatekey(a, fm, 1, 'e')
	Result: H
	New key: ALEXCTF{HERE_GOES_TH
	>>> listxorfunc(a,fm)
	Dear Friend, This ti
	nderstood my mistake
	sed One time pad enc
	n scheme, I heard th
	is the only encrypti
	hod that is mathemat
	 proven to be not cr
	ever if the key is k
	cure, Let Me know if
	gree with me to use
	ncryption scheme alw
	>>> fm = updatekey(a, fm, 10, 'ays')
	Result: E_K
	New key: ALEXCTF{HERE_GOES_THE_K
	>>> listxorfunc(a,fm)
	Dear Friend, This time
	nderstood my mistake an
	sed One time pad encryp
	n scheme, I heard that
	is the only encryption
	hod that is mathematica
	 proven to be not crack
	ever if the key is kept
	cure, Let Me know if yo
	gree with me to use thi
	ncryption scheme always
	>>> fm = updatekey(a, fm, 2, 't')
	Result: E
	New key: ALEXCTF{HERE_GOES_THE_KE
	>>> listxorfunc(a,fm)
	Dear Friend, This time I
	nderstood my mistake and
	sed One time pad encrypt
	n scheme, I heard that i
	is the only encryption m
	hod that is mathematical
	 proven to be not cracke
	ever if the key is kept
	cure, Let Me know if you
	gree with me to use this
	ncryption scheme always.
	>>> fm = updatekey(a, fm, 0, ' u')
	Result: Y}
	New key: ALEXCTF{HERE_GOES_THE_KEY}

The flag: `ALEXCTF{HERE_GOES_THE_KEY}`

If you want to see the text, just run this command at last:

	repeatxor(''.join(a), fm)

**output**

	Dear Friend, This time I understood my mistake and used 
	One time pad encryption scheme, I heard that it is the 
	only encryption method that is mathematically proven to be 
	not cracked ever if the key is kept secure, Let Me know if 
	you agree with me to use this encryption scheme always.
