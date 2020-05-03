import Definitions
from Exceptions import ExcecutionError
from typing import List, Dict, Callable

class Cpu():

    DIRECT = 10
    REGISTER = 11
    REFERENCE = 12

    REGAX = 1
    REGBX = 2
    REGCX = 3
    REGDX = 4
    REGIP = 15
    REGSP = 14

    def __init__(self, memory: List[int]):
        self.memory = memory
        self.reset()
        self.parameter1Mode = 0
        self.parameter2Mode = 0

        self.instructionTable: Dict[int, Callable] = {
            0x0010: self.MOV,
            0x0011: self.CMP,
            
            0x0012: self.ADD,
            0x0013: self.SUB,
            0x0014: self.MUL,
            0x0015: self.DIV,

            0x0016: self.JMP,
            0x0017: self.JZ,
            0x0018: self.JNZ,
            0x0019: self.JO,
            0x0020: self.JNO,
            0x0021: self.JC,
            0x0022: self.JNC,

            0x0023: self.DEC,
            0x0024: self.INC,

            0x0025: self.AND,
            0x0026: self.OR,
            0x0027: self.XOR,
            0x0028: self.NOT,

            0x0029: self.PUSH,
            0x0030: self.POP,
            0x0031: self.PUSHF,
            0x0032: self.POPF,

            0x0033: self.CALL,
            0x0034: self.RET,

            0x0035: self.JL,
            0x0036: self.JLE,

            0x0037: self.JG,
            0x0038: self.JGE,

            0x0039: self.STOR,

            0x0040: self.SHL,
            0x0041: self.SHR,

            0x00FF: self.HLT
        }

    def reset(self) -> None:
        self.AX = 0
        self.BX = 0
        self.CX = 0
        self.DX = 0
        self.SP = 0
        self.IP = 0
        self.FLAGS = 0

    def SF(self) -> bool:
        return self.FLAGS & 0b000001 == 0b000001

    def OF(self) -> bool:
        return self.FLAGS & 0b000010 == 0b000010

    def ZF(self) -> bool:
        return self.FLAGS & 0b000100 == 0b000100

    def CF(self) -> bool:
        return self.FLAGS & 0b001000 == 0b001000

    def PF(self) -> bool:
        return self.FLAGS & 0b010000 == 0b010000

    def IF(self) -> bool:
        return self.FLAGS & 0b100000 == 0b100000

    def cycle(self) -> bool:
        i = self.memory[self.IP]
        opcode = i & 0x00FF
        self.parameter1Mode = (i & 0xF000) >> 12
        self.parameter2Mode = (i & 0x0F00) >> 8
        instruction: Callable = self.instructionTable[opcode]
        return instruction()

    def setRegister(self, reg: int, value: int):
        if reg == self.REGAX:
            self.AX = value
        elif reg == self.REGBX:
            self.BX = value
        elif reg == self.REGCX:
            self.CX = value
        elif reg == self.REGDX:
            self.DX = value
        elif reg == self.REGIP:
            self.IP = value
        elif reg == self.REGSP:
            self.SP = value

    def getRegister(self, reg: int) -> int:
        if reg == self.REGAX:
            return self.AX
        elif reg == self.REGBX:
            return self.BX
        elif reg == self.REGCX:
            return self.CX
        elif reg == self.REGDX:
            return self.DX
        elif reg == self.REGIP:
            return self.IP
        elif reg == self.REGSP:
            return self.SP
        return -1

    def determineValue(self, paramMode: int, memValue: int) -> int:
        if paramMode == self.DIRECT:
            return memValue
        elif paramMode == self.REGISTER:
            return self.getRegister(memValue)
        elif paramMode == self.REFERENCE:
            regValue = self.getRegister(memValue)
            return self.memory[regValue]
        return -1    
    
    def JMP(self):
        # print("JMP")
        if self.parameter1Mode != self.DIRECT:
            raise ExcecutionError("JMP: Bad Parameter 1", self.IP)

        self.IP = self.memory[self.IP + 1]
        return True

    def MOV(self):
        # print("MOV")

        if self.parameter1Mode != self.REGISTER:
            raise ExcecutionError("MOV: Bad Parameter 1", self.IP)

        regTo = self.memory[self.IP + 1]
        value = self.determineValue(self.parameter2Mode, self.memory[self.IP + 2])

        self.setRegister(regTo, value)

        self.IP += 3
        return True

    def STOR(self):
        # print("STOR")

        self.IP += 3
        return True

    def CMP(self):
        # print("CMP")

        self.IP += 3
        return True

    def JZ(self):
        # print("JZ")

        self.IP += 2
        return True

    def JNZ(self):
        # print("JNZ")

        self.IP += 2
        return True

    def JO(self):
        # print("JO")

        self.IP += 2
        return True

    def JNO(self):
        # print("JNO")

        self.IP += 2
        return True

    def JC(self):
        # print("JO")

        self.IP += 2
        return True

    def JNC(self):
        # print("JNC")

        self.IP += 2
        return True

    def JL(self):
        # print("JL")

        self.IP += 2
        return True

    def JLE(self):
        # print("JLE")

        self.IP += 2
        return True

    def JG(self):
        # print("JG")

        self.IP += 2
        return True

    def JGE(self):
        # print("JGE")

        self.IP += 2
        return True

    def ADD(self):
        # print("ADD")

        self.IP += 3
        return True

    def SUB(self):
        # print("SUB")

        self.IP += 3
        return True

    def MUL(self):
        # print("MUL")

        self.IP += 3
        return True

    def DIV(self):
        # print("DIV")

        self.IP += 3
        return True

    def DEC(self):
        # print("DEC")

        self.IP += 2
        return True

    def INC(self):
        # print("INC")

        self.IP += 2
        return True

    def AND(self):
        # print("AND")

        self.IP += 3
        return True
    
    def OR(self):
        # print("OR")

        self.IP += 3
        return True
    
    def XOR(self):
        # print("XOR")

        self.IP += 3
        return True
    
    def NOT(self):
        # print("NOT")

        self.IP += 2
        return True

    def PUSH(self):
        # print("PUSH")

        self.IP += 2
        return True
    
    def POP(self):
        # print("POP")

        self.IP += 2
        return True

    def PUSHF(self):
        # print("PUSHF")

        self.IP += 1
        return True
    
    def POPF(self):
        # print("POPF")

        self.IP += 1
        return True

    def CALL(self):
        # print("CALL")

        self.IP += 2
        return True
    
    def RET(self):
        # print("RET")

        self.IP += 1
        return True

    def SHL(self):
        # print("SHL")

        self.IP += 2
        return True

    def SHR(self):
        # print("SHR")

        self.IP += 2
        return True

    def HLT(self):
        # print("HLT")

        self.IP += 0
        return False
