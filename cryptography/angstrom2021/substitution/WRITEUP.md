## Challenge name:	Substitution

### Description:
> Source
> 
> nc crypto.2021.chall.actf.co 21601
> 
> P.S: given files: *[chall.py](./chall.py)*

### Solution:

The server code is simple. There is an array containing flag's characters ascii number. For each input, server encrypt flag and give just a number less than 691. Let's discuss how substitue function works. Imagine the flag is "actf". For input *3*, we have:

    key = [0x61, 0x63, 0x74, 0x66]
    output = (0x61 * 3**3 + 0x63 * 3**2 + 0x74 * 3 + 0x66) % 691

If we execute with input *0*, we have:

    output = (0x61 * 0 + 0x63 * 0 + 0x74 * 0 + 0x66) % 691

Which we have last character. I was trying to compute others one by one with last character, but that didn't work. Then I realized this is a simple Algebra too! Let's say the flag is 4 characters. We give server 4 input 0 to 3 and then we have:

    output0 = (key[0] * 0    + key[1] * 0    + key[2] * 0 + key[3]) % 691
    output1 = (key[0] * 1    + key[1] * 1    + key[2] * 1 + key[3]) % 691
    output2 = (key[0] * 2**3 + key[1] * 2**2 + key[2] * 2 + key[3]) % 691
    output3 = (key[0] * 3**3 + key[1] * 3**2 + key[2] * 3 + key[3]) % 691

4 equations, 4 unknowns! We solve this with sage. We create a matrix 4*4, that represents 0, 1, 2\*\*3, 3\*\*3, etc. We have vector representing unknowns and a vector, output of each equation. But we have another problem. We don't know the flag length. Don't worry! Just Bruteforce!! 

I defined **max_len** and as 50, requested server for each input from 0 to 49, then bruteforce flag length and solved equations using sage. For each length, I checked if '*actf{*' is in flag or not.

    print ('[*] Getting Y space')
    Y = []
    for i in range(max_len):
        Y.append(f_send(str(i)))
    Y = vector(Y)
        
    print ('[*] Bruteforce on flag length')
    for i in range(7, max_len):
        print ('\t| Flag length: {0}'.format(i))
        
        X = create_X(i)
        ans = (X.solve_right(Y[:i])) % 691
        
        flag = ''
        for c in ans:
            flag += chr(c)

        if ('actf{' in flag):
            print ('[+] Flag: {0}'.format(flag))
            break

[final exploit.py](./exploit.py)

**Output**

    [+] Opening connection to crypto.2021.chall.actf.co on port 21601: Done
    [*] Getting Y space
    [*] Bruteforce on flag length
        | Flag length: 7
        | Flag length: 8
        | Flag length: 9
        | Flag length: 10
        | Flag length: 11
        | Flag length: 12
        | Flag length: 13
        | Flag length: 14
        | Flag length: 15
        | Flag length: 16
        | Flag length: 17
        | Flag length: 18
        | Flag length: 19
        | Flag length: 20
        | Flag length: 21
        | Flag length: 22
        | Flag length: 23
        | Flag length: 24
        | Flag length: 25
        | Flag length: 26
        | Flag length: 27
        | Flag length: 28
        | Flag length: 29
        | Flag length: 30
        | Flag length: 31
        | Flag length: 32
        | Flag length: 33
        | Flag length: 34
        | Flag length: 35
        | Flag length: 36
        | Flag length: 37
        | Flag length: 38
        | Flag length: 39
        | Flag length: 40
    [+] Flag: actf{polynomials_20a829322766642530cf69}


**The Flag**

    actf{polynomials_20a829322766642530cf69}
