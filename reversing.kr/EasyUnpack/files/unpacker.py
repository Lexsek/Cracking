from binaryninja import *
import time

def unpack(start, end):

    count = end - start
    key = [0x10, 0x20, 0x30, 0x40, 0x50]
    br.seek(start)
    bw.seek(start)
    for b in range(0, count):
        try:
            data = ord(br.read(1)) ^ key[b % len(key)]
            print chr(bw.write(chr(data)))
        except:
            pass

filepath = "/home/lexsek/GITHUB/Cracking/reversing.kr/EasyUnpack/files/Easy_UnpackMe.exe"
dbpath = "/home/lexsek/GITHUB/Cracking/reversing.kr/EasyUnpack/Easy_UnpackMe.bndb"
fm = FileMetadata()
db = fm.open_existing_database(dbpath)
bv = db.get_view_of_type('PE')
br = BinaryReader(bv)
bw = BinaryWriter(bv)
bv.update_analysis()
time.sleep(1)

unpack(bv.start + 0x9000, bv.start + 0x94ee)
unpack(bv.start + 0x1000, bv.start + 0x5000)
unpack(bv.start + 0x6000, bv.start + 0x9000)

fm.create_database("/home/lexsek/GITHUB/Cracking/reversing.kr/EasyUnpack/unpacked.bndb")
print fm.saved
