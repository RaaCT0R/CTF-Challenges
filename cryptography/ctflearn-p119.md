## Challenge name: RSA Beginner
### Difficulty:	Hard

### Description:
> I found this scribbled on a piece of paper. Can you make sense of it? https://mega.nz/#!zD4wDYiC!iLB3pMJElgWZy6Bv97FF8SJz1KEk9lWsgBSw62mtxQg
> 
> P.S: given file: ctflearn-p119-file

### My note:

Acctualy, this is a medium challenge, maybe easy. All you need to know is RSA-encryption algorithm. Here i explain how RSA works:

> Suppose we have ***plain_text***, we convert it to number ***m*** with some algorithm (e.g. with hex encoding), we choose two prime like ***p*** and ***q***, define ***n*** as ***p \* q***. Now we calculate ***c*** as follow:
	
	c = m^e mod n

> ***c*** is our **cipher**. For decrypt, we choose ***d*** such that:

	d = k^(-1) mod n

> Now we calculate ***m*** as follow:

	m = c^d mod n

> And then decode ***m*** to ***plain_text***.

Now we go through the challenge :)

### Solution:

According to file, we have ***e***, ***c*** and ***n***:

	e = 3
	c = 219878849218803628752496734037301843801487889344508611639028
	n = 245841236512478852752909734912575581815967630033049838269083

But ***n*** is a small number, so we can factorize it. I use [Factordb](http://factordb.com/) for factorizing. We find ***p*** and ***q*** as follow:

	p = 416064700201658306196320137931
	q = 590872612825179551336102196593

I define 2 function for calculating ***d***, using **Extended Greatest Common Diviser**:

	import codecs

	def egcd(a, b):
		x,y, u,v = 0,1, 1,0
		while a != 0:
			q, r = b//a, b%a
			m, n = x-u*q, y-v*q
			b,a, x,y, u,v = a,r, u,v, m,n
		return x

	def findD(a, b):
		return b + egcd(a, b)

Then, calculate ***d*** and ***m*** as follow:

	d = findD(e, (p-1) * (q-1))
	m = pow(c, d, n)

Now we need to decode ***m*** to ***plain_text***. First i try decoding it with ascii:

	plain_text = codecs.decode(hex(m), 'hex').decode('ascii')

The flag: `abctf{rs4_is_aw3s0m3}`