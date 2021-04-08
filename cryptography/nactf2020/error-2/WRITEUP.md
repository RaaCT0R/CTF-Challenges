## Challenge name:	Error 2

### Description:
> Kayla decided she wants to use the previous error detection scheme for cryptography! After computing the normal error bits, she switched them around according to a secret key.
> 
> P.S: given files: *[error2.py](./error2.py)*, *[enc.txt](./enc.txt)*

### Solution:

As they said in Description, this is similar to challenge **Error 1**, but they just change the index of parity bits (if you don't read Error 1 challenge and its writeup, please read it [here](../nactf_error-1/WRITEUP.md) before proceed).

So how we calculate parity number if we don't know which indexes are they ? The answer is easy, we try all of them! There are 15 bits and 4 parity bits, so we have C(4, 15) = 1365 cases to check. We bruteforce on parity bits indexes, then we have 1365 flags. Just print the cases that start with **nactf**.

**Code**

    from functools import reduce
    import string

    arr_of_pos = []

    def init_arr():
        for i in range(15):
            for j in range(15):
                if (i == j):
                    continue
                for k in range(15):
                    if (i == k or j == k):
                        continue
                    for z in range(15):
                        if (i == z or j == z or k == z):
                            continue
                        arr = (i, j, k, z)
                        if (arr not in arr_of_pos):
                            arr_of_pos.append(arr)

    def check(arr):
        output = []

        for pos_arr in arr_of_pos:
            parity_pos = (0, 1, 3, 7)
            code = ''

            arr_copy = arr.copy()

            p_num = int(arr[pos_arr[0]]) + int(arr[pos_arr[1]]) * 2 + int(arr[pos_arr[2]]) * 4 + int(arr[pos_arr[3]]) * 8

            arr_copy = [k for j, k in enumerate(arr_copy) if j not in pos_arr]
            for j in range(4):
                arr_copy.insert(parity_pos[j], arr[pos_arr[j]])

            parity = reduce(lambda a, b: a ^ b, [j + 1 for j, bit in enumerate(arr_copy) if (bit and j not in (0, 1, 3, 7))])
            parity_arr = list(reversed(list(str(format(parity, "04b")))))

            ind = (p_num ^ parity) - 1
            arr_copy[ind] = int(not arr_copy[ind])
            
            for j in range(15):
                if (j not in (0, 1, 3, 7)):
                    code += str(arr_copy[j])

            output.append(code)

        return output

    init_arr()
    text = ''
    with open('enc.txt', 'r') as fd:
        text = fd.read()

    flag = []
    flag = [[int(j) for j in text[i:i + 15]] for i in range(0, len(text), 15)]

    code = []
    for i in flag:
        code.append(check(i))

    flag_arr = []

    def bruteforce(code):
        for i in range(len(code[0])):
            message = ''
            decrypted_flag = ''
            for j in range(len(code)):
                message += code[j][i]

            for j in range(0, len(message), 8):
                c = chr(int(message[j:j+8], 2))
                if (c in string.printable):
                    decrypted_flag += c
                else:
                    continue

            flag_arr.append(decrypted_flag)
            if (decrypted_flag[0:6] == 'nactf{' or decrypted_flag[0:6] == 'NACTF{'):
                print(decrypted_flag)

    bruteforce(code)

**Output**

    nactf{err0r_c0rr3cti0n_w1th_th3_c0rr3ct_f1le_q73xer7k9}
    nactf{MrB0r_c0rpctY0_w14lCt(s_w0rrT^1je_q73per'+}
    nactf{ercr_btrpctx|_w1<lCt(s_w0rrPn1e_q7zyMckm

**The Flag**

    nactf{err0r_c0rr3cti0n_w1th_th3_c0rr3ct_f1le_q73xer7k9}
