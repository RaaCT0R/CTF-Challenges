from pwn import *
import time
import random

def get_r_num(text):
	r.sendlineafter('> ', text)
	resp = r.recvuntil('\n\n')
	resp = int(resp[:-2])
	return resp

def send_r(text1, text2):
    print(r.sendlineafter('> ', 'g'))
    print(r.sendlineafter('> ', text1))
    print(r.sendlineafter('> ', text2))
    print(r.recvline())
    resp = r.recvline()
    return resp

start_seed = round(time.time() / 100 - 10, 5)

r = remote("challenges.ctfd.io", 30264)

r_num = get_r_num('r')
print('[*] random number: {0}'.format(r_num))
seed_num = 0
found = False

for i in range(10000000):
    seed_num = round(start_seed + i/100000, 5)
    random.seed(seed_num)
    r1 = random.randint(1, 100000000)

    if (r1 == r_num):
        print('[+] seed found')
        found = True
        break

    if (i % 1000000 == 0):
        print('[*] step {0}'.format(i / 1000000))

if (found == False):
    print('[-] seed not found')
else:
    print('[*] sending random numbers')
    random.seed(seed_num)
    r1 = random.randint(1, 100000000)   
    r1 = random.randint(1, 100000000)
    r2 = random.randint(1, 100000000)

    resp = send_r('{0}'.format(r1), '{0}'.format(r2))
    print(resp)