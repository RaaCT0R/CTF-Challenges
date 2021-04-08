## Challenge name:	Oracle of Blair

### Description:
> Not to be confused with the ORACLE of Blair. Source
>
> nc crypto.2021.chall.actf.co 21112
> 
> P.S: given files: *[server.py](./server.py)*

### Solution:

My favorite challenge in this CTF! We have server code, which take an input from us, replace any "*{}*" occurrence with flag string and then apply some cryptography to it. 

First I tried to get flag size. Sending '*{}*' to server and get 32bytes of data, meaning that flag length is in range 17 to 32. All we need to is add character to the string one by one and see the results.

    for i in range(16):
        pd1 = 'a'*i + '{}'
        y = f_send(pd1.encode().hex())
        print ('i: {0}, len(y): {1}'.format(i, len(y)))

With **i=8** we get 96 instead of 72, which mean the flag length is **32 - 7**=**25**. Then I thought this is a Padding Oracle challenge. After a little implementation, I realized server is decrypting **inp**, not encrypting! So I came up with a new attack. First let's have a look at Block Cipher CBC mode decryption schema:

![block_cipher_cbc_decryption](bc_cbc_decryption.png)

Assume we are giving server **pd1** and flag is something like this:

    pd1 = 'a'*7 + '{}' + 'a'*32
    flag = 'actf{XXXXXXXXXXXXXXXXXXX}

Then **inp** will be:

    aaaaaaaactf{XXXX XXXXXXXXXXXXXXX} aaaaaaaaaaaaaaaa aaaaaaaaaaaaaaaa

Now, let's call first 16 characters of '*a*' **C1** and second 16 characters of '*a*' **C2** and "*XXXXXXXXXXXXXXX}*" **C0**. The server response will be 128 hex characters representing 64bytes of data. According to last sentence, the last 16bytes of server response will be **P2**, the bytes before that will be **P1**. We know **I2**=**I1** (CBC mode basics!). We also know that **C1**^**I2**=**P2** ('*^*' is **XOR** operator). So we have **C1**^**P2**=**I2**.

We know all of this for previous block too, **C0**^**P1**=**I1**. We know **C1**, **P1**, **P2**. Then we can calculate **C0** as: 

    C0 = (P2 ^ C1) ^ P1

So using this input, we calculate last 16bytes of flag. We can do this for first 9bytes of flag too. Now we give server **pd2**:

    pd2 = 'a'*7 + '{}' + flag_2.decode('ascii')

Where **flag_2** is last 16bytes of flag which we computed in previous round. **inp** will be:

    aaaaaaaactf{XXXX XXXXXXXXXXXXXXX} XXXXXXXXXXXXXXX}

Similar to previous round, we have:

    C0 = "aaaaaaaactf{XXXX"
    C1 = "XXXXXXXXXXXXXXX}"
    C2 = "XXXXXXXXXXXXXXX}"

Like previous round we know **C1**, **P1**, **P2**. Then we can calculate **C0** as:

    C0 = (P2 ^ C1) ^ P1

[final exploit.py](./exploit.py)

**Output**

    [+] Opening connection to crypto.2021.chall.actf.co on port 21112: Done
    [*] Round 1
        | pd1: 616161616161617b7d6161616161616161616161616161616161616161616161616161616161616161
        | server response: b'd26f173c624760c6bee3613d57905e983efbcf4caaa235a4b8a9b3559bef21609f6ca0745f99ce624552a5f677f85ff09362b3706194c668416ca1f474c65dec'
        | P1: 9f6ca0745f99ce624552a5f677f85ff0
        | P2: 9362b3706194c668416ca1f474c65dec
        | C1: 61616161616161616161616161616161
    [+] C0: b'more_like_ecb_c}'
    [*] Round 2
        | pd1: 616161616161617b7d6d6f72655f6c696b655f6563625f637d
        | server response: b'b09cbe77feb3635924439d2a0de64ba03efbcf4caaa235a4b8a9b3559bef216032f5dc4894af3daebe82b04d9ad22142'
        | P1: 3efbcf4caaa235a4b8a9b3559bef2160
        | P2: 32f5dc4894af3daebe82b04d9ad22142
        | C1: 6d6f72655f6c696b655f6563625f637d
    [+] C0: b'aaaaaaaactf{cbc_'
    [+] Flag: b'actf{cbc_more_like_ecb_c}'



**The Flag**

    actf{cbc_more_like_ecb_c}
