from binaryninja import *
import time

filepath = "/home/lexsek/GITHUB/Cracking/reversing.kr/EasyUnpack/files/Easy_UnpackMe.exe"
dbpath = "/home/lexsek/GITHUB/Cracking/reversing.kr/EasyUnpack/Easy_UnpackMe.bndb"
fm = FileMetadata()
db = fm.open_existing_database(dbpath)
bv = db.get_view_of_type('PE')
br = BinaryReader(bv)
bw = BinaryWriter(bv)
bv.update_analysis()
time.sleep(1)

packed = bv.start + 0x1000
count = bv.start + 0x5000 - packed
print count

br.seek(packed)
bw.seek(packed)

key = [0x10, 0x20, 0x30, 0x40, 0x50]

for b in range(0, count):
    try:
        data = ord(br.read(1)) ^ key[b % len(key)]
        print chr(bw.write(chr(data)))
    except:
        pass

fm.create_database("/home/lexsek/GITHUB/Cracking/reversing.kr/EasyUnpack/unpacked.bndb")
print fm.saved
