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
            chr(bw.write(chr(data)))
        except:
            pass

def parseIAT(start):
    
    magic = '\xac\xdf'
    end = magic + '\x30\x40'
    br.seek(start)
    while True:
        if br.read(4) == end:
            break
        else:
            br.offset -= 4
        if br.read(2) == magic:
            while br.read(1) != '\x00':
                pass
        else:
            br.offset -= 2
        addr = br.read32le()
        name = ''
        while br.read(1) != '\x00':
            br.offset -= 1
            name += br.read(1)
        bv.define_user_symbol(Symbol(SymbolType.DataSymbol, addr, name))

filepath = "/home/lexsek/GITHUB/Cracking/reversing.kr/EasyUnpack/files/Easy_UnpackMe.exe"
dbpath = "/home/lexsek/GITHUB/Cracking/reversing.kr/EasyUnpack/Easy_UnpackMe.bndb"
fm = FileMetadata()
db = fm.open_existing_database(dbpath)
bv = db.get_view_of_type('PE')
br = BinaryReader(bv)
bw = BinaryWriter(bv)
bv.update_analysis()
time.sleep(1)

unpack(bv.start + 0x9000, bv.start + 0x94ee) # Unpack IAT
unpack(bv.start + 0x1000, bv.start + 0x5000) # Unpack code
unpack(bv.start + 0x6000, bv.start + 0x9000) # Unpack .data
parseIAT(bv.start + 0x9129) # Resolve IAT

fm.create_database("/home/lexsek/GITHUB/Cracking/reversing.kr/EasyUnpack/unpacked.bndb")