def name2Serial(name: str) -> None:
    serial = []
    key = [0x10, 0x20, 0x30]
    for l in range(0, len(name)):
        serial.append(str(hex(ord(name[l]) ^ (key[l % 3]))).upper()[2:])
    print("> Serial : {}".format(''.join(serial)))

def serial2Name(serial: str) -> None:
    name = []
    key = [0x10, 0x20, 0x30]
    serial = [serial[i:i+2] for i in range(0, len(serial), 2)]
    for l in range(0, len(serial)):
        name.append(chr(int(serial[l], 16) ^ key[l % 3]))
    print("> Name : {}".format(''.join(name)))

choice = input("> 1: Generate Serial\n> 2: Generate Name\n")
if choice == "1":
    name = input("> Name\n")
    name2Serial(name)
else:
    serial = input("> Serial\n")
    serial2Name(serial)
