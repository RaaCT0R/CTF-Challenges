## Challenge name:	DeFUNct Ransomware

### Description:
> Santa got infected by a ransomware! His elves managed to extract the public key, but couldn't break it. Help Santa decrypt his memos and save Christmas!
> 
> P.S: given files: *xmasctf-crypto2-file1.txt*, *xmasctf-crypto2-file2.enc*

### Solution:

We take a look at the text file, we see 2 variables named as **n** nad **e**. Challenge description is also talking about a public key, so we have a RSA here!

First of all, we try to factorize **n**. I use [Factordb](http://factordb.com/) to do it. Seems our **n** is formed as **p^2** * **q^2** where **p** and **q** are primes. So, we have:

    φ(n) = φ(p^2 * q^2)
    φ(p^2 * q^2) = φ(p^2) * φ(q^2)  #p^2 and q^2 are co-prime
    φ(p^2) = (p - 1) * p            #p is prime

    φ(n) = p * q * (p - 1) * (q - 1)

Now all we need is to use a script to find **d** and calculate plaintext. We define two functions in order to find **d**:

    def egcd(a, b):
        if a == 0:
            return (b, 0, 1)
        else:
            g, y, x = egcd(b % a, a)
            return (g, x - (b // a) * y, y)

    def modinv(a, m):
        g, x, y = egcd(a, m)
        if g != 1:
            raise Exception('modular inverse does not exist')
        else:
            return x % m

We have φ(n) as well, so we decrypt c and try decoding it using ASCII:

    d = modinv(e, (p-1)*p*(q-1)*q)
    m = pow(x, d, n)
    t = codecs.decode(hex(m)[2:], 'hex')
    print(t)

**Output**
	
    'TODO\n----\n\n* Stop downloading RAM for the internet.\n* Remove yakuhito from the naughty kids list.\n* Drink all the milk; eat all the cookies\n* Do not forget the flag: X-MAS{yakuhito_should_n0t_b3_0n_th3_n@ughty_l1st_941282a75d89e080}\n'

**The Flag**

    X-MAS{yakuhito_should_n0t_b3_0n_th3_n@ughty_l1st_941282a75d89e080}


