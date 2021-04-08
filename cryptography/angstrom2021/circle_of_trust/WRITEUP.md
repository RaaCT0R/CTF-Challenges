## Challenge name:	Circle of Trust

### Description:
> Clam created a 1337 secret sharing scheme for his 1337 trio of friends. Can you crack it?
> 
> output source
> 
> P.S: given files: *[output.text](./output.txt)*, *[gen.py](./gen.py)*

### Solution:

First of all, I need to say that this challenge made me so much suffering. I was working on it for about 12 hours which most of it was for debugging.

As we see in code, there is nothing unusual about AES and also they gave us something related to key and iv. So the solution is to find them. As we see there are some known equations. Let's call **keynum + b_i** as **kb_i** and **ivnum + c_i** as **ic_i**. There we have:

    kb1 = keynum + b1
    kb2 = keynum + b2
    kb2 = keynum + b3
    ci1 = ivnum + c1
    ci2 = ivnum + c2
    ci3 = ivnum + c3

Also, `c = (a ** 2 - b ** 2).sqrt()` is in common between them. so we have:

    b1**2 + c1**2 = X
    b2**2 + c3**2 = X
    b3**2 + c2**2 = X

There we have 9 equations and 9 unknowns. Let's do some Algebra!

But this is when the suffering starts. First I wrote a script in sage to do the algebra part:

    var('b1 b2 b3 c1 c2 c3')
    eq1 = b1-b2==kb1-kb2
    eq2 = b3-b2==kb3-kb2
    eq3 = c1-c2==ic1-ic2
    eq4 = c3-c2==ic3-ic2
    eq5 = b1^2+c1^2==b2^2+c2^2
    eq6 = b1^2+c1^2==b3^2+c3^2
    ans = solve([eq1, eq2, eq3, eq4, eq5, eq6], b1, b2, b3, c1, c2, c3)[0]

Then used **b_i** and **c_i** to get **keynum** and **ivnum**. Unfortunately, the result was unacceptable. 52bits of key was computed successfully, but 2bits was wrong and 74bits of key was zero. I spend most of the time trying different approaches, such as computing **keynum** and **ivnum** with sage but that didn't work. It seems there are some nerve-racking approximation in sage float calcualtion and python. At last, after some headache, I multiplied **kb_i** and **ic_i** with *10\*\*11* to make them integers. Fortunately, that worked and gave me the flag.

[final exploit.sage](./exploit.sage)

**Output**

    [+] keynum with b1: 0x1bfe0b6f8a37046b215feb95ec7c3eec
    [+] keynum with b2: 0x1bfe0b6f8a37046b215feb95ec7c3eec
    [+] ivnum with c1: 0xfa10ce6588624a1abdae9708ffacd530
    [+] ivnum with c2: 0xfa10ce6588624a1abdae9708ffacd531
    [+] Plaintext: b'actf{elliptical^curve_minus_the_curve}\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'

There is '*^*' character in flag, which is probably due to bit miscalculation, which we know the right character is '*_*'.

**The Flag**

    actf{elliptical_curve_minus_the_curve}
