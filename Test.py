import re
import msvcrt
import unittest

def Parse(str: str):

        if re.match("^\\[([A-D]X|SP|IP)\\]$", str):
            return str[1:-1]

        return None

def Test(str):
    print(f"{str} => {Parse(str)}")

def ParseNumber(value: str):

    if value.isnumeric():
        return int(value)

    if re.match("^0(x|X)([0-9A-Fa-f]{1,4})$", value):
        value = value[2:]
        return int(value, 16)

    if re.match("^0(b|B)([0-1]{8}|[0-1]{16})$", value):
        value = value[2:]
        return int(value, 2)

    return None

def Test2(str):
    v = ParseNumber(str)
    if v == None:
        print(f"{str} = None")
    else:
        print(f"{str} => {v} = {hex(v)} = {bin(v)}")


Test("[AX]")
Test("[BX]")
Test("[CX]")
Test("[DX]")
Test("[SP]")
Test("[IP]")
Test("[EX]")
Test("[AY]")

Test2("123")
Test2("0")
Test2("42")
Test2("0x0")
Test2("0x0000")
Test2("0xFF00")
Test2("0xA")
Test2("0xFF")
Test2("0b00000000")
Test2("0b001000000")
Test2("0b00000100")
Test2("0b11111111")
Test2("0b1110000000011111")
Test2("0b111111")
Test2("0x111F1")
Test2("0y1111")
Test2("123A")
Test2("0x1H11")

while True:
    keycode = ord(msvcrt.getch())
    if keycode == 27: #ESC
        break
    elif keycode == 13: #Enter
        print("Enter")
    elif keycode == 224: #Special keys (arrows, f keys, ins, del, etc.)
        keycode = ord(msvcrt.getch())
        if keycode == 80: #Down arrow
            print("Arrow Down")
        elif keycode == 72: #Up arrow
            print("Arrow Up")
