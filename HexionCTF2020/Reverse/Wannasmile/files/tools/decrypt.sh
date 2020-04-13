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
