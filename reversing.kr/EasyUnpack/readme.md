# Cracking

## Informations

- Website  : reversing.kr 
- Filename : Easy_UnpackMe.exe 
- Sha256   : b4d90c754de829482d70d47593ecedc2d518c8d902347da55e325bf7709d2134 
- Filetype : PE32 executable (GUI) Intel 80386, for MS Windows

## Analysis

### First look

The file Easy_UnpackMe.exe is a PE32 executable cracking challenge as shown by CFF Explorer.

![alt text](images/image1.png)
![alt text](images/image2.png)

But the file info is undefined.

Launching PEiD gives us the following information about the sections:

![alt text](images/image3.png)

The .Gogi and .GWan section are weird, and the entry point of the program is set the to .GWan section, so it may be packed (the name of the challenge gives us a hint about that).

A ReadMe.txt file is giving us some informations about our objective :

![alt text](images/image4.png)

We will have to unpack the program, and the flag will be the entry point of the unpacked program.

Having a look into binary ninja in order to understand how it works, you can see in the following graph of the start address function :
- Start block
- Import Address Table unpack (highlighted in blue)
- Import Address Table Resolution (highlighted in green)
- Executable code unpack (highlighted in orange)
- .data unpack (highlighted in red)
- Executable code packed (highlighted in black)

![alt text](images/image0.png)

### Packer steps

#### Executable code packed

We can determine that this code is packed, due to the loops with xor's before, and also unconsistant instructions.

![alt text](images/image11.png)

So we need to analyze the loops in order to understand how to unpack this.

#### Starting block

The starting block consists of resolving at runtime the address of kernel32.dll module and it's functions (FreeLibrary and GetModuleHandle).

Then it will mov the start address of the first encrypted chunk in ecx, and the end in edx.

![alt text](images/image5.png)

#### IAT unpack

The Import Address table start address is stored in ecx. 

The loop will simply xor all the import address table with the key "\x10\x20\x30\x40\x50", and also change the memory page protection of the .rdata section with Read/Write.

The decrypted block will contain the name of the functions that will be loaded at runtime by the IAT Resolution block.

![alt text](images/image6.png)

#### IAT resolution

This block consists of iterating over the function names that have been decrypted by the IAT unpack routine, and loading at runtime these functions.

Loading the modules:

![alt text](images/image7.png)

Getting the address the functions:

![alt text](images/image8.png)

At the end, it will change the permission of the executable code by giving it Writing rights to unpack it.

#### Executable code unpack

This loop consists of unpacking the executable code with the key "\x10\x20\x30\x40\x50".

![alt text](images/image9.png)

#### .data unpack

This loop consists of unpacking the .data section with the key "\x10\x20\x30\x40\x50".

![alt text](images/image10.png)

And then jumping on the unpacked code, so the real entry point of the program is : "0x401150".

#### Unpacked code

The unpacked code will simply create a white window.

![alt text](images/image12.png)

### Conclusion

The unpack program starts at the address "401150", so looking at the ReadMe.txt file gives us the right format to validate the challenge and gives us the web browser alert telling us we validated (or alrady have valited) the challenge.

Flag : "00401150"

![alt text](images/image13.png)