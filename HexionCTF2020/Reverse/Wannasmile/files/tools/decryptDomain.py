encryptedDomain = ":0929:14019<101<\x1D\xF7"
ret = []

for i in range(0, 16):
    ret.append(chr((int(((ord(encryptedDomain[i % 2 + 16]) >> (i // 2)) & 1) != 0)) | 2 * ord(encryptedDomain[i])))

print("Decrypted domain is : {}".format(''.join(ret)))
