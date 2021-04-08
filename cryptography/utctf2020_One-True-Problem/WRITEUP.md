## Challenge name:	One True Problem

### Description:
> Two of my friends were arguing about which CTF category is the best, but they encrypted it because they didn't want anyone to see. Lucky for us, they reused the same key; can you recover it?
> 
> Here are the ciphertexts:
> 
> 213c234c2322282057730b32492e720b35732b2124553d354c22352224237f1826283d7b0651
> 
> 3b3b463829225b3632630b542623767f39674431343b353435412223243b7f162028397a103e

### Solution:

There is an algorithm named **One-Time-Pad**. You generate a true random key with the size as long as plaintext size. Then XOR them, bit by bit.

In this problem, I try something else. We know the flag start with **utflag{**. So, if we XOR first seven bytes with it, we can find first seven bytes of key:

    def nonrepeatxor(text, key):
        sk = len(key)
        for i in range(0, 2 * sk, 2):
                x = int(text[i:i + 2], 16)
                y = ord(key[i // 2])
                if (x ^ y > 31):
                        print(chr(x ^ y), end='')
                else:
                        print('\\x%x' % (x ^ y), end='')

    c1 = '213c234c2322282057730b32492e720b35732b2124553d354c22352224237f1826283d7b0651'
    c2 = '3b3b463829225b3632630b542623767f39674431343b353435412223243b7f162028397a103e'

    nonrepeatxor(c1, 'utflag{)

**Output**

    THE BES

It seems, the key starts with "THE BEST". With a look at challenge description, next word could be "CTF" or "Category". 

Now we can XOR cipher with key and get the plaintext. Let's open commandline after running script and use this function and updating key for catching plaintext. First I tried "Category" for next and failed! Then tried "CTF" and it was okey.

    def run():
        st = len(c1)
        sk = len(key)

        nonrepeatxor(c1, key)
        print ((st - sk) * '?')
        nonrepeatxor(c2, key)
        print ((st - sk) * '?')

**Output**
	
    The key is: THE BES
    Commandline:
    >>> run()
    utflag{?????????????????????????????????????????????????????????????????????
    os\x3\x18kg\x8?????????????????????????????????????????????????????????????????????
    >>> key += "T CTF CATEGORY"
    >>> run()
    utflag{tw0_tim3_p4ds}???????????????????????????????????????????????????????
    os\x3\x18kg\x8b\x12 _\x12\x6`7+| \xbcm???????????????????????????????????????????????????????
    >>> 

[final script.py](./script.py)

**The Flag**

    utflag{tw0_tim3_p4ds}
    
P.S: 2 day after CTF, i wonder why other characters wasn't printable, so I thinked a little more and realized, the flag, wasn't plaintext (should realize sooner! as the challenge description said!), but it was the key! With this function. We can use this function and find plaintext:

	def repeatxor(text, key):
		st = len(text)
		sk = len(key)
		empty=""
		for i in range(0, st, 2):
			x = int(text[i:i + 2], 16)
			y = ord(key[(i // 2) % sk])
			print(chr(x ^ y), end='')
			
**Output**

	THE BEST CTF CATEGORY IS CRYPTOGRAPHY!
	NO THE BEST ONE IS BINARY EXPLOITATION
