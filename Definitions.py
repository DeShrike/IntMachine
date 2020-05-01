from Instruction import *

"""
MOV	AX, 6		reg, direct
MOV BX, label   reg, direct
MOV AX, BX	    reg, reg
MOV CX, [AX]    reg, ref
STOR AX, [BX]	reg, ref
"""

addressingModes = { 
    "direct": 0,
    "register": 1,
    "reference": 2
}

registers = {
    "AX": 1,
    "BX": 2,
    "CX": 3,
    "DX": 4,
    "SP": 14,
    "IP": 15,
}

datatypes = { "word" : 2, "byte" : 1, "string" : 0 }

"""
https://www.geeksforgeeks.org/program-execution-transfer-instructions-8086-microprocessor/?ref=lbp

flags: ZF, CF, OF, SF, PF, IF
"""

instructions = {
    "MOV": Instruction("MOV", 0x0010, 2),
    "CMP": Instruction("CMP", 0x0011, 2),

    "ADD": Instruction("ADD", 0x0012, 2),
    "SUB": Instruction("SUB", 0x0013, 2),
    "MUL": Instruction("MUL", 0x0014, 2),
    "DIV": Instruction("DIV", 0x0015, 2),

    "JMP": Instruction("JMP", 0x0016, 1),

    "JZ":  Instruction("JZ",  0x0017, 1),	# if ZF = 1 then jump 
    "JNZ": Instruction("JNZ", 0x0018, 1),	# if ZF = 0 then jump 

    "JO":  Instruction("JO",  0x0019, 1),	# if OF = 1 then jump 
    "JNO": Instruction("JNO", 0x0020, 1),	# if OF = 0 then jump 

    "JC":  Instruction("JC",  0x0021, 1),	# if CF = 1 then jump 
    "JNC": Instruction("JNC", 0x0022, 1),	# if CF = 0 then jump 

    "DEC": Instruction("DEC", 0x0023, 1),
    "INC": Instruction("INC", 0x0024, 1),

    "AND": Instruction("AND", 0x0025, 2),
    "OR":  Instruction("OR",  0x0026, 2),
    "XOR": Instruction("XOR", 0x0027, 2),
    "NOT": Instruction("NOT", 0x0028, 1),

    "PUSH": Instruction("PUSH", 0x0029, 1),
    "POP":  Instruction("POP",  0x0030, 1),

    "PUSHF": Instruction("PUSHF", 0x0031, 0),
    "POPF":  Instruction("POPF",  0x0032, 0),

    "CALL": Instruction("CALL", 0x0033, 1),
    "RET":  Instruction("RET",  0x0034, 0),

    "JL":  Instruction("JL",  0x0035, 1),	# if SF <> OF then jump 
    "JLE": Instruction("JLE", 0x0036, 1),	# if SF <> OF or ZF = 1 then jump

    "JG":  Instruction("JG",  0x0037, 1),	# if (ZF = 0) and (SF = OF) then jump
    "JGE": Instruction("JGE", 0x0038, 1),	# if SF = OF then jump

    "STOR": Instruction("STOR", 0x0039, 2),

    "SHL": Instruction("SHL", 0x0040, 1),
    "SHR": Instruction("SHR", 0x0041, 1),

    "HLT": Instruction("HLT", 0x00FF, 0) 
}

# https://www.programiz.com/python-programming/methods/string/find

def parseNumber(value: str):
    if value.isnumeric():
        return int(value)

    if re.match("^0(x|X)([0-9A-Fa-f]{1,4})$", value):
        value = value[2:]
        return int(value, 16)

    if re.match("^0(b|B)([0-1]{8}|[0-1]{16})$", value):
        value = value[2:]
        return int(value, 2)

    return None
