## Challenge name:	Home Rolled Crypto

### Description:
> Aplet made his own block cipher! Can you break it?
> 
> nc crypto.2021.chall.actf.co 21602
> 
> P.S: given files: *[chall.py](./chall.py)*

### Solution:

First we read the server code. There is a Class *Cipher* which has block size of 16 and 3 rounds. Also from `assert(len(key) == self.BLOCK_SIZE*self.ROUNDS)`, we know key length is 48 (3 blocks of 16bytes). Also from for loop in encrypt function, we know cipher encrypt each block separately. Let's see block encryption:

    def __block_encrypt(self, block):
        enc = int.from_bytes(block, "big")
        for i in range(self.ROUNDS):
            k = int.from_bytes(self.key[i*self.BLOCK_SIZE:(i+1)*self.BLOCK_SIZE], "big")
            enc &= k
            enc ^= k
        return hex(enc)[2:].rjust(self.BLOCK_SIZE*2, "0")

According to code, each bit of block encrypted by only 1 bit in each round and that is corresponding bit of **round**th block of the key. For example, encrypting **1**st bit of block uses **1**st, **17**th and **33**th bit of the key. 

All we need to do is writing truth table, to see each case:

| *i* th bit of enc | *i* th bit of key | round 1 output | *i+16* th bit of key | round 2 output | *i+32* th bit of key | round 3 output
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 0 | **0** | 0 | **0** | 0 | **0** |
| 0 | 0 | **0** | 0 | **0** | 1 | **1** |
| 0 | 0 | **0** | 1 | **1** | 0 | **0** |
| 0 | 0 | **0** | 1 | **1** | 1 | **0** |
| 0 | 1 | **1** | 0 | **0** | 0 | **0** |
| 0 | 1 | **1** | 0 | **0** | 1 | **1** |
| 0 | 1 | **1** | 1 | **0** | 0 | **0** |
| 0 | 1 | **1** | 1 | **0** | 1 | **1** |
| 1 | 0 | **0** | 0 | **0** | 0 | **0** |
| 1 | 0 | **0** | 0 | **0** | 1 | **1** |
| 1 | 0 | **0** | 1 | **1** | 0 | **0** |
| 1 | 0 | **0** | 1 | **1** | 1 | **0** |
| 1 | 1 | **0** | 0 | **0** | 0 | **0** |
| 1 | 1 | **0** | 0 | **0** | 1 | **1** |
| 1 | 1 | **0** | 1 | **1** | 0 | **0** |
| 1 | 1 | **0** | 1 | **1** | 1 | **0** |

Some rows end in same state. Since we need to encrypt, it doesn't matter which one the key was. So we encrypt two input:

	p1 = 'ffffffffffffffffffffffffffffffff'
	p2 = '00000000000000000000000000000000'

First one, all bits are 1 and second one, all bits are zero. we compare two output with truth table and decide which row we use. Then we can create a key that encrypt with server key.

    def find_key(x, y):
        assert len(x) == 8
        
        o1 = ''
        o2 = ''
        o3 = ''
        for i in range(8):
            if (x[i] == '0' and y[i] == '0'):
                o1 += '0'
                o2 += '0'
                o3 += '0'
            elif (x[i] == '0' and y[i] == '1'):
                o1 += '1'
                o2 += '1'
                o3 += '1'
            elif (x[i] == '1' and y[i] == '0'):
                raise Exception('compare 1 to 0. this can\'t happen')
            else:
                o1 += '0'
                o2 += '0'
                o3 += '1'
        return (int(o1, 2).to_bytes(1, 'big'), int(o2, 2).to_bytes(1, 'big'), int(o3, 2).to_bytes(1, 'big'))

Note: **x** is 8bits of output corresponding to **p1** input.

[final exploit.py](./exploit.py)

**Output**

    [+] Opening connection to crypto.2021.chall.actf.co on port 21602: Done
    [*] Key creation phase
    [+] key: 01108100000008448a4012802000040001108100000008448a40128020000400031aab14010128fccbf47aa239000cc8
    [*] Encryption phase
    [*] Encrypting: b'a2f18d5590c14c874788ab2883ac28201c323d743c776de4894ca00013b1bb35'
    [*] Encrypting: b'aed7897e682cba2feb02bfa3ef13e1d53f9ac8e0d3d84aaa078ee82ca57c638b'
    [*] Encrypting: b'93bdfe355e015f7b36d43580457af1ef8e2944614b85c6d2c7660963e47a05a5'
    [*] Encrypting: b'5685a2028d46fe91555b1f3716cdc3d424c28e267e53308f7d86e007b97be64e'
    [*] Encrypting: b'0ba47b26348883f7244c21b3517b9707f295f3e129cf9b2beb922bbf0ec2be94'
    [*] Encrypting: b'84fa6c6df8ef9a792592cbb1cbeffa59914616ae9ffed349b2553f0ae1d47f3e'
    [*] Encrypting: b'ff2e897a2764b7f21a6d3fcc45ad25975c6c7b236f5593b1f6abeb473fd2b1f6'
    [*] Encrypting: b'43120230f6ae566209a9b0e4e93732f3d14ee896112d80702be5d93bf8c0da86'
    [*] Encrypting: b'a179476a82cac1601d1a2fcafae10b5b1409e2465145f11694623c65c2c2f164'
    [*] Encrypting: b'255a099bbba38cc483ca49458b775d18304c66599aed0efbecf47010b692c004'
    b'W\nactf{no_bit_shuffling_is_trivial}\nWould you like to encrypt [1], or try encrypting [2]? '

**The Flag**

    actf{no_bit_shuffling_is_trivial}
