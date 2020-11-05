## Challenge name:	Error 1

### Description:
> Pranay has decided that the previous error detection scheme is a little bit too inefficient... While eating his delicious HAM-filled Italian Sub at lunch, he came up with a new idea. Fortunately, he has also invested in a less noisy communication channel.
> 
> P.S: given files: *[error1.py](./error1.py)*, *[enc.txt](./enc.txt)*

### Solution:

This is not a cryptography but a communication systems challenge that referred to **Hamming code Error Detection**. It **XOR** the index of ones (actually, index + 1) in binary representation of each block of message and save the result number *(parity)* with the block. You can read more [here](https://en.wikipedia.org/wiki/Hamming_code).

In this challenge, they partitioned the message into block of size 11-bit that form a 4-bit parity and saved them at indexes of 0, 1, 3 and 7, which will form 15-bit blocks. After creating each block, they simulate one-bit error that flip a single bit. The parity number of result block will be:

> parity = last_parity ^ (index_of_fliped_bit + 1)

As we know about XOR, we can calculate **index_of_fliped_bit** as follow:

> index_of_fliped_bit = (parity ^ last_parity) - 1

So we need to partition the cipher into 15-bit blocks, calculate parity and compare it to parity that is saved with message, calculate XOR of them to get fliped bit index, and correct it.

**Code**

    from functools import reduce

    text = ''

    with open('enc.txt', 'r') as fd:
        text = fd.read()

    flag = []
    flag = [[int(j) for j in text[i:i + 15]] for i in range(0, len(text), 15)]

    code = ''
    for i in flag:
        p_arr = []
        for j in range(4):
            p_arr.append(str(i[2 ** j - 1]))
        p_num = int(p_arr[0]) + int(p_arr[1]) * 2 + int(p_arr[2]) * 4 + int(p_arr[3]) * 8

        parity = reduce(lambda a, b: a ^ b, [j + 1 for j, bit in enumerate(i) if (bit and j != 0 and j != 1 and j != 3 and j != 7)])
        parity_arr = list(reversed(list(str(format(parity, "04b")))))

        ind = (p_num ^ parity) - 1
        i[ind] = int(not i[ind])
        
        for j in range(15):
            if (j != 0 and j != 1 and j != 3 and j != 7):
                code += str(i[j])

    for i in range(0, len(code), 8):
        print(chr(int(code[i:i+8], 2)), end='')
    print()

**The Flag**

    nactf{hamm1ng_cod3s_546mv3q9a0te}
