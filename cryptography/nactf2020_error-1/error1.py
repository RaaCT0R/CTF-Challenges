import random
from functools import reduce

with open("flag.txt", "r") as fin:
    flag = fin.read()

flag = "".join(str(format(ord(c), '08b')) for c in flag)  # converts flag to 8 bit ascii representation
flag = [[int(j) for j in flag[i:i + 11]] for i in range(0, len(flag), 11)]  # separates into 11 bit groups
code = []
for i in flag:
    for j in range(4):
        i.insert(2 ** j - 1, 0)
    parity = reduce(lambda a, b: a ^ b, [j + 1 for j, bit in enumerate(i) if bit])
    parity = list(reversed(list(str(format(parity, "04b"))))) # separates number into individual binary bits

    for j in range(4):
        if parity[j] == "1":
            i[2 ** j - 1] = 1
    
    # ind = random.randint(0, len(i) - 1)
    # i[ind] = int(not i[ind]) # simulates a one bit error
    code.extend(i)

enc = "".join([str(i) for i in code])
with open("enc1.txt", "w") as fout:
    fout.write(enc)
