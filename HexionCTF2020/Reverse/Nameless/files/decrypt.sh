#!/bin/bash

for i in `seq 1586537927 1586635200`;
do
    ./decrypt $i
    ret=$(grep -ai hexCTF flag.txt)
    if [[ ! -z $ret ]] ; then
        echo "[+] Found flag :"
        cat flag.txt
        echo -ne "\n[+] Seed was :\n$i\n"
        break
    fi
done
