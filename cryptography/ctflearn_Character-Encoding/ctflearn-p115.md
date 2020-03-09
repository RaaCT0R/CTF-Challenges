## Challenge name: Character Encoding
### Difficulty:	Hard

### Description:
> In the computing industry, standards are established to facilitate information interchanges among American coders. Unfortunately, I've made communication a little bit more difficult. Can you figure this one out? 41 42 43 54 46 7B 34 35 43 31 31 5F 31 35 5F 55 35 33 46 55 4C 7D

### My note:

This is a very easy challenge. I don't know why they called it hard :|.

### Solution:

In first look, what we see is exactly like a hex encoding, So we decode it to check.

	import codecs

	c = '41 42 43 54 46 7B 34 35 43 31 31 5F 31 35 5F 55 35 33 46 55 4C 7D'

	# remove spaces to decode cipher
	c = c.replace(' ', '')
	m = codecs.decode(c, 'hex').decode('ascii')
	print(m)

The flag: `ABCTF{45C11_15_U53FUL}`