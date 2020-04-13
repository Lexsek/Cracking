# Reverse-Engineering

## Informations

- CTF : Hexion CTF 2020
- Challenge Name : Wanna Smile & Wanna Smile 2
- Challenge Author : (moka)@HexionCTFTeam
- Challenge Description : 
    - 1 : ```I accidentally executed this weird file that encrypted my important files! please help me understand what it does. ssh wannasmile@challenges1.hexionteam.com -p 4000 Password: hexctf *This challenge consists of 2 parts.
**Attached version has the first flag removed.```
    - 2 : ```Thank you for helping me stop the virus! can you recover my files now? ssh wannasmile@challenges1.hexionteam.com -p 4000 Password: hexctf```
- Filename : wannasmile 
- Sha256   : 152b1a72fd7b54a451948fc3b5fbf6e520e9776f766039c47996c274fe92f56f 
- Filetype : ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 3.2.0, BuildID[sha1]=cffaa7d672950992382109258cab9f85b17a7a41, stripped

## Analysis

### WannaSmile : First look

The wannasmile file is an ELF 64-bit executable, that is dynamically linked, and stripped. 

The title of the challenge and the binary reminds us about "WannaCry" ransomware.

Getting the dynamic libs with ldd reveals the use of libcrypto, which might let us think that this sample corresponds to a "Wannacry" reimplementation for linux.

```console
lexsek@lexsek:~$ ldd wannasmile
linux-vdso.so.1 (0x00007ffd4b237000)
libcrypto.so.1.1 => /usr/lib/libcrypto.so.1.1 (0x00007fc63e607000)
libc.so.6 => /usr/lib/libc.so.6 (0x00007fc63e441000)
libdl.so.2 => /usr/lib/libdl.so.2 (0x00007fc63e43c000)
libpthread.so.0 => /usr/lib/libpthread.so.0 (0x00007fc63e41a000)
/lib64/ld-linux-x86-64.so.2 => /usr/lib64/ld-linux-x86-64.so.2 (0x00007fc63eb16000)
```

Strings also reveals important informations :
- libcrypto
- aes_256_cbc
- RSA functions
- RSA pubkey
- RSA privkey
- Extension list
- Encryption ransom message/note
- Flag related

```console
lexsek@lexsek:~$ strings wannasmile
[...]
libcrypto.so.1.1
[...]
RSA_size
RSA_public_encrypt
[...]
EVP_aes_256_cbc
[...]
SEND %d BITCOINS IF YOU WANT YOUR FILES BACK
Address: %s
<REDACTED> (shell server has flag here)
[...]
.jpg
.png
.txt
.doc
.pptx
-----BEGIN RSA PRIVATE KEY-----
MIIEowIBAAKCAQEAujCxmc9GU2RHVWRgQKhHkU+vrD35XbAbWIGFu+a5mghCvLWc
aCm0HDW7zU8t8InSXkCa03mUrZLtERl00JviFEdREYpV3ATpKM9CG7WCMmCvT7+k
j9ReKhqNwmJTfYxf/yEN3STMtl8d2UUDAXLDX6RMijuVF4r1hhHJcmzbQsfi4SzL
xmBkTEdr+0P+8WyLGb6eI1NsCPhLw5ctma2Sf/iAuN1VZ4EFrhP8DMQR683Ha0w5
zllh6Olz15d6AoMtOAKpt1/d+oebmimnweUdoUji3M09g0RlzcbkcjGdydFmkTfl
RfXruneYwx/1ajbkzOIKSYtvsQ68qfutEv5UYwIDAQABAoIBAHV45YUavs88lLku
xH/m7IilEzyEOYI/63Dy/3KnRvEFRz4TA6TAsy+dQ2ltDJoYCs+GyWil7AV7jvFb
81TvFTwgJuj/M97GhmlGIvqikYvBbrrNOkG5BtRfvpMnQHAVEjhBHaMqZbKm3olH
vna6dsQwQE5y+0VIWlKFhGkaf1ho+HlghrTs1hp8q53LjYOkSzIiLC2llSqX+TJI
4likIe3SJc9I3tvBcNXjKE4lDtJv8UVvvOX870Okaiz4gcezghWKAP0jlBnjGt4h
aNPyCLN2QN5AsF6cL+VN6vKQqiTP6IO/Z27RvmZpFnZCS4lCdxIWVQplZSAQvhZr
S3vlU0kCgYEA/fP/Gum81jsZILHYQyHXD7c+mpDMsF9q8UcEgJWhsFwl7gpmXhKF
UkbbaAZ41LdRLEMULN9lrj9KsZgUSL+q1dbgg58QfeWeT23GrBryOLc4+73O2tDY
GLKlm1iDbzUcH90rt9N/l1P1mchum5yhPgce9s/Vxd+FsT+JrdKa2E0CgYEAu7Dg
TOIwZGkkAPChuzvgGwQc5zyB2W9JMIu6f/vjv5sO9ULml7YPNKLl5lQb3tLClLKE
mLH+km5Ktt9aSegxFMYxHBOjbPNHiQzNucziFld/gnLxZH2VecqAztu1eIaRLFsO
RN+M08Ci5AIcgNELopihwRWoOBIlxIm1YGPqN28CgYEAkz6ZCJLD8fccL6/Oc8Y4
Ox2Fh/szI4R/rlv+CUw5DtevCmEvT5YvhTAeYSd3gea0gxR1qzrwauK5vVUvVasE
M66+SLK+zjCH5QgCbKHHFgluWdCJEqiK028pxHPC6YUCxJrpkVFpJmYA/mSPdVyQ
xTU9x99j1LIwg0AS5R06uPUCgYBbwCJV0zh+zVr5TqhxI9rwufj7HPwI87rejV+1
EsiJsN4GDRc2UJxsSbmC99jL+1F9aSsijdh5cor5jIPRnzzm/9+f7wWzy9VLbMPg
sQRQkaNWfKP+UNnSOKjw9jxm17l96mE2T+XC2eeG+HVAj3BVorFn9xNNnalywzK0
FQO45wKBgGSNstScPA8i1Jrqa0NaMMbRvP1ifhID/snDt3mfgybvD1GEUcNIQUDu
1hUE/K5lMaijtcbsuvpW+9y8mL0ZTI3kk8voOV8VkJ8cMy8/RH7zRMC2lC+GU7es
nGUfgUSTuxJ06sNCNF3AqGwRmaIrQ/e7qRBmzrcU3QmkXTBiaEL9
-----END RSA PRIVATE KEY-----
-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAujCxmc9GU2RHVWRgQKhH
kU+vrD35XbAbWIGFu+a5mghCvLWcaCm0HDW7zU8t8InSXkCa03mUrZLtERl00Jvi
FEdREYpV3ATpKM9CG7WCMmCvT7+kj9ReKhqNwmJTfYxf/yEN3STMtl8d2UUDAXLD
X6RMijuVF4r1hhHJcmzbQsfi4SzLxmBkTEdr+0P+8WyLGb6eI1NsCPhLw5ctma2S
f/iAuN1VZ4EFrhP8DMQR683Ha0w5zllh6Olz15d6AoMtOAKpt1/d+oebmimnweUd
oUji3M09g0RlzcbkcjGdydFmkTflRfXruneYwx/1ajbkzOIKSYtvsQ68qfutEv5U
YwIDAQAB
-----END PUBLIC KEY-----
[...]
```

### WannaSmile : Analysis of the main

Having a look into BinaryNinja in order to understand how the wannasmile executable works.

We can figure out a decryption loop (highlighted in blue).

A block containing a call to "gethostbyname()" function (highlighted in white).

If the domain is valid, we go to the "puts()" that prints "\<REDACTED> (shell server has flag here)" (highlighted in green).

Else, if the domain isn't valid, we call the "sub_189f" function (highlighted in red).

![alt text](images/image2.png)
    
### WannaSmile : Domain name encryption and Killswitch

Here is the python code that reimplements the domain name decryption :

```python
encryptedDomain = ":0929:14019<101<\x1D\xF7"
ret = []

for i in range(0, 16):
    ret.append(chr((int(((ord(encryptedDomain[i % 2 + 16]) >> (i // 2)) & 1) != 0)) | 2 * ord(encryptedDomain[i])))

print("Decrypted domain is : {}".format(''.join(ret)))
```

```console
lexsek@lexsek:~$ python decryptDomain.py
Decrypted domain is : uaresuchacrybaby
```

Obviously, this domain will never answer, it is a killswitch, just like in the WannaCry ransomware.

If we add an entry in our /etc/hosts file :
```
127.0.0.1 uaresuchacrybaby
```

We can now securely start the ransomware :
```console
lexsek@lexsek:~$ ./wannasmile
<REDACTED> (shell server has flag here)
```

So the binary we have is different than the one on the server, it has a censored flag, so we have to go on the remote server with the ssh access we have been granted and change the dns options.

The thing is that, we don't have root access so we can't edit the /etc/hosts file in remote. 

We will have to use something different, like the environment variable called HOSTALIASES, that does pretty much the same without beeing root.

So we are going to redirect uaresuchacrybaby to a valid domain, like pornhub.com.

```console
lexsek@lexsek:~$ ssh wannasmile@challenges1.hexionteam.com -p 4000
Welcome to Ubuntu 18.04.4 LTS (GNU/Linux 5.0.0-1034-gcp x86_64)
[...]
wannasmile@c93d605716ed:~$ echo "uaresuchacrybaby pornhub.com" > /tmp/lexsek
wannasmile@c93d605716ed:~$ export HOSTALIASES=/tmp/lexsek
wannasmile@c93d605716ed:~$ ./wannasmile 
hexCTF{wh0_put5_k1ll_sw1tch3s_in_the1r_m4lw4r3}
```

Here we go, the first part of the WannaSmile challenge is solved.

Now let's move to part 2 !

### WannaSmile2 : First look

The part 2 analysis starts with the "sub_189f" function.

Here is it's graph displayed by BinaryNinja :

![alt text](images/image3.png)

The malware checks it is was started with an argument by checking the length of argc.

If yes, he executes the block highlighted in blue, and call the encryptionFunction.

Else, he will fork, the father code highlighted in green will simply print text to the console :

```
-- Roleplay mode activate ---
SEND 1742 BITCOINS IF YOU WANT YOUR FILES BACK
Address: 115p7UMMngoj1pMvkpHijcRdfJNXj6LrLn
```

The bitcoin amount and the wallet address depends on your UID for the rand.

There are 3 wallet address in the malware :
- 13AM4VW2dhxYgXeQepoHkHSQuy6NgaEb94
- 12t9YDPgwueZ9NyMgw519p7AA8isjr6SMw
- 115p7UMMngoj1pMvkpHijcRdfJNXj6LrLn

The son code highlighted in red will simply restart the malware with it's path as argument, by calling execve.

### WannaSmile2 : Encryption algorithm analysis

Now we are going to analyze the encryption function.

The malware iterates over the files located in the /var/wannasmile2 directory (highlighted in blue), and check if their extension matches the extension to encrypt that are (highlighted in green) :
- .jpg
- .png
- .txt
- .doc
- .pptx



If it matches, the malware calls the encryption file function.

![alt text](images/image5.png)
![alt text](images/image4.png)

Here is the graph of the file encryption function:

- Reads the file to encrypt
- Generate a random AES key
- Encrypt buffer containing file data with AES_256_CBC / key
- Creates a new buffer and write the AES_256_CBC key encrypted with the RSA public key
- Overwrites the file

![alt text](images/image6.png)
![alt text](images/image7.png)

The overwritten file follow this structure :
- WANNASMILE (10 bytes)
- AES_256_CBC key encrypted with RSA pubkey (256 bytes)
- Encrypted file data with AES_256_CBC key (x bytes)

### File decryption automatisation

Now that we know how a file is encrypted, we are going to write an antidote.

First we will have to recover the RSA encrypted AES_256_CBC key to decrypt our file.

Then we will have to decrypt it with the RSA private key that is stored in the malware.

After that, we will need to recover the encrypted file data and decrypt it with the AES_256_CBC key.

The following bash script will do the job :
```bash
#!/bin/bash

# WannaSmile Lexsek Decryptor

privkey=$1
input=$2

magic="WANNASMILE"

aeskeyenc=$input"_aes.key.enc"
aeskey=$input"_aes.key"

encfile=$input".enc"
decfile=$input".dec"

# Check if the file is a valid private key
is_private_key() {
    if openssl rsa -noout -modulus -in $privkey &> /dev/null; then
        return 1
    fi
    echo "[!] File $privkey is not a valid private key"
    exit
}

# Check if the file is encrypted
is_encrypted() {
    filestart=$(head -n1 $input|cut -c1-10)
    if [ "$filestart" = "$magic" ]; then
        return 1
    fi
    echo "[+] File $input is not encrypted"
    exit
}

# Check if file exists
file_exists() {
    if [ -f $1 ]; then
        return 1
    fi
    echo "[!] File $1 doesn't exists"
    exit
}

# Extract AES encrypted key from the encrypted file and decrypt it with the RSA private key
extract_and_decrypt_aes_key() {
    dd if=$input of=$aeskeyenc bs=1 skip=10 count=256
    openssl rsautl -decrypt -inkey $privkey -in $aeskeyenc -out $aeskey
}

# Extract the encrypted file data and decrypt it using the AES_256_CBC key
extract_and_decrypt_file_data() {
    dd if=$input of=$encfile bs=1 skip=266
    key=$(xxd -p $aeskey|tr -d '\n')
    openssl enc -aes-256-cbc -nosalt -d -in $encfile -K $key -iv 0 -out $decfile
}

# Remove operation files
remove_operation_files() {
    rm $aeskeyenc
    rm $encfile
    rm $aeskey
}

if [ $# -ne 2 ]; then
    echo "Usage : <RSA.privkey> <encryptedFile>"
    exit
fi

file_exists $privkey
file_exists $input
is_private_key
is_encrypted
extract_and_decrypt_aes_key
extract_and_decrypt_file_data
remove_operation_files

```

So now, we can connect to the remote server, download the encrypted files.

```console
lexsek@lexsek:~$ ssh sftp -P 4000 wannasmile@challenges1.hexionteam.com
wannasmile@challenges1.hexionteam.com's password: 
Connected to challenges1.hexionteam.com.
sftp> cd /var/wannasmile2/
sftp> get *
Fetching /var/wannasmile2/HexionLogo.png to HexionLogo.png
Fetching /var/wannasmile2/aaaaa.png to aaaaa.png
Fetching /var/wannasmile2/flag2.txt to flag2.txt
Fetching /var/wannasmile2/present.pptx to present.pptx
```

We run our decrypt script on them.

```console
lexsek@lexsek:~$ ./decrypt.sh key.priv aaaaa.png
lexsek@lexsek:~$ ./decrypt.sh key.priv flag2.txt
lexsek@lexsek:~$ ./decrypt.sh key.priv HexionLogo.png
lexsek@lexsek:~$ ./decrypt.sh key.priv present.pptx
```

Checking the filetype now.

```console
lexsek@lexsek:~$ file *
aaaaa.png:      PNG image data, 374 x 374, 8-bit/color RGBA, non-interlaced
flag2.txt:      ASCII text, with no line terminators
HexionLogo.png: PNG image data, 1467 x 1467, 8-bit/color RGBA, non-interlaced
present.pptx:   Microsoft PowerPoint 2007+
```

aaaaa.png :

![alt text](files/decrypted/aaaaa.png)

HexionLogo.png : 

![alt text](files/decrypted/HexionLogo.png)

present.pptx :

- Powerpoint about covid-19

flag2.txt :

- hexCTF{1_d0nt_w4nt_t0_smil3_4nym0r3}

Here we go, the second flag is here.

### Wannasmile & Wannasmile 2 : Conclusion

That was a really pleasuring challenge based on ransomware, encryption RSA/AES and domain killswitch ! Thanks again to the HexionCTF Staff & Challenger Makers for the fun !

Flags : 
- hexCTF{wh0_put5_k1ll_sw1tch3s_in_the1r_m4lw4r3}
- hexCTF{1_d0nt_w4nt_t0_smil3_4nym0r3}