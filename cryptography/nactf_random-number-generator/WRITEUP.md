## Challenge name:	Random Number Generator

### Description:
> Dr. J created a fast pseudorandom number generator (prng) to randomly assign pairs for the upcoming group test. Austin really wants to know the pairs ahead of time... can you help him and predict the next output of Dr. J's prng?
> 
> nc challenges.ctfd.io 30264
> 
> P.S: given files: *[rand0.py](./rand0.py)*

### Solution:

In the first view, we think we should hack the python random.randint function (It's possible!), but this challenge is a lot easier! in provided file, we see the service will set the python random seed in start. That's it, we have the exact time, we can set our seed equal to server seed and generate exact random number. This is possible with a simple bruteforce!

The **time.time()** will return seconds passed from 1970. So before we start the connection to service, we use it to get time. Then we get a number **r** from server to compare our generated number to server. I used **pwn** library for connection and two functions to get **r** and send my generated numbers:

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

Since the service use only 5 precision of time() function, and it's divided by 100, the bruteforce should not be large. Add **0.000001** to time, generate a random number, compare to **r**, till we find right seed. Then we generate two next numbers and send to server and get flag in return. let's see the code:

    start_seed = round(time.time() / 100, 5)

    r = remote("challenges.ctfd.io", 30264)

    r_num = get_r_num('r')
    print('[*] random number: {0}'.format(r_num))
    seed_num = 0
    found = False

    for i in range(100000):
        seed_num = round(start_seed + i/100000, 5)
        random.seed(seed_num)
        r1 = random.randint(1, 100000)

        if (r1 == r_num):
            print('[+] seed found')
            found = True
            break

    if (found == False):
        print('[-] seed not found')
    else:
        print('[*] sending random numbers')  
        r1 = random.randint(1, 100000000)
        r2 = random.randint(1, 100000000)

        resp = send_r('{0}'.format(r1), '{0}'.format(r2))
        print(resp)

At first, i didn't get the flag. So i tried larger loop. That mean adding more minutes as hours, and stil failed! Then I realized there can be time difference between my location and server location! so I saved start_seed for some hours ago, and It works!

    start_seed = round(time.time() / 100 - 10, 5)

**Output**
	
    [+] Opening connection to challenges.ctfd.io on port 30264: Done
    [*] random number: 15487693
    [*] step 0.0
    [*] step 1.0
    [+] seed found
    [*] sending random numbers
    b'> '
    b'Guess the next two random numbers for a flag!\nGood luck!\nEnter your first guess:\n> '
    b"Wow, lucky guess... You won't be able to guess right a second time\nEnter your second guess:\n> "
    b"What? You must have psychic powers... Well here's your flag: \n"
    b'nactf{ch000nky_turn1ps_1674973}\n'

[final script.py](./script.py)

**The Flag**

    nactf{ch000nky_turn1ps_1674973}
