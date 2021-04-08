from pwn import *

pchar = ''
r = remote("ecb.utctf.live", 9003)
flag = ''

def init_pchar():
	global pchar
	for i in range(26):
		pchar += chr(ord('a') + i)
	for i in range(10):
		pchar += chr(ord('0') + i)
	pchar += '_'
	pchar += '{}'
	for i in range(26):
		pchar += chr(ord('A') + i)
	pchar += '\0'

def bf():
	global flag
	pf = 'a' * (31 - len(flag))
	print('\t|--Poison data: "%s"' % (pf))
	resp1 = f_send(pf)[:64]
	resp2 = ''
	while True:
		resp2 = f_send(pf)[:64]
		if resp1 != resp2:
			break
	print('\t\t|--resp1: %s' % (resp1))
	print('\t\t|--resp2: %s' % (resp2))

	for c in pchar:
		pd = pf + flag + c
		print('\t\t|--Test on "%s"' % (pd))
		res1 = f_send(pd)[:64]
		res2 = ''
		while True:
			res2 = f_send(pd)[:64]
			if res2 != res1:
				break

		print('\t\t\t|--res1: %s' % (res1))
		print('\t\t\t|--res2: %s' % (res2))
		if (res1 == resp1 and res2 == resp2) or (res1 == resp2 and res2 == resp1):
			flag += c
			print('\t\t\t|--Character found: %c' % (c))
			return 0

	print ('\t\t\t|--not found!')
	return -1

def f_send(text):
	r.sendlineafter(':\n', text)
	r.recvuntil(':)\n')
	resp = r.recvline()[:-1]
	return resp

init_pchar()
while len(flag) != 32:
	if bf() == -1:
		print('\t|--ERROR character not found')
		break
	print ('[*] flag: %s, len(flag): %d' % (flag, len(flag)))

