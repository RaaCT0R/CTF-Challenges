## Challenge name:	Follow the Currents

### Description:
> go with the flow... Source
> 
> P.S: given files: *[enc](./enc)*, *[source.py](./source.py)*

### Solution:

A simple bruteforce challenge! all source code do is generating key with *keystream* function and **XOR** it with flag. Keystream has 2 bytes for initial. We bruteforce all 65536 of them, generate the key and compute the plaintext and check if it contains "actf{".

    with open("enc","rb") as f:
        ciphertext = f.read()
        
    plain = []
    for j in range(65535):
        kb = j.to_bytes(2, 'big')
        k = keystream(kb)
        for i in ciphertext:
            plain.append(i ^ next(k))
            
        m = bytes(plain)
        if (b"actf{" in m):
            print (m)
        plain = []

[final exploit.py](./exploit.py)

**Output**

    b"x''R@\xc5\x05\xfb/9\xe7\x10\x13L\xc5\xd6\x19 minutes left before the ctf starts so i have no idea what to put here other than the flag which is actf{low_entropy_keystream}"
    b'\x88\x86\x02\x15\x8b are like 30 minutes left before the ctf starts so i have no idea what to put here other than the flag which is actf{low_entropy_keystream}'
    b'uX\x07\x80^\xec\xe0\x1e\x069\xe7\x10\x13L\xc5\xd6\x19 minutes left before the ctf starts so i have no idea what to put here other than the flag which is actf{low_entropy_keystream}'
    b'\x85\xf9"\xc7\x95\t\x84\x97L like 30 minutes left before the ctf starts so i have no idea what to put here other than the flag which is actf{low_entropy_keystream}'
    b'there are like 30 minutes left before the ctf starts so i have no idea what to put here other than the flag which is actf{low_entropy_keystream}'
    b'\x84\xc9@5\xae\xc5\x05\xfb/9\xe7\x10\x13L\xc5\xd6\x19 minutes left before the ctf starts so i have no idea what to put here other than the flag which is actf{low_entropy_keystream}'
    b'y\x17E\xa0{\t\x84\x97L like 30 minutes left before the ctf starts so i have no idea what to put here other than the flag which is actf{low_entropy_keystream}'
    b'\x89\xb6`\xe7\xb0\xec\xe0\x1e\x069\xe7\x10\x13L\xc5\xd6\x19 minutes left before the ctf starts so i have no idea what to put here other than the flag which is actf{low_entropy_keystream}'

**The Plaintext**

    there are like 30 minutes left before the ctf starts so i have no idea what to put here other than the flag which is actf{low_entropy_keystream}
