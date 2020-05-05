import Definitions
from Exceptions import ExcecutionError
from typing import List, Dict, Callable

class Cpu():

    DIRECT = 10
    REGISTER = 11
    REFERENCE = 12
    INDEXED = 13

    REGAX = 1
    REGBX = 2
    REGCX = 3
    REGDX = 4
    REGIX = 13
    REGSP = 14
    REGIP = 15

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

            0x00EE: self.NOP,
            0x00FF: self.HLT
        }

    def reset(self) -> None:
        self.AX = 0
        self.BX = 0
        self.CX = 0
        self.DX = 0
        self.IX = 0
        self.SP = 0
        self.IP = 0
        self.FLAGS = 0

    def SF(self) -> bool:
        return (self.FLAGS & 0b000001) == 0b000001

    def OF(self) -> bool:
        return (self.FLAGS & 0b000010) == 0b000010

    def ZF(self) -> bool:
        return (self.FLAGS & 0b000100) == 0b000100

    def CF(self) -> bool:
        return (self.FLAGS & 0b001000) == 0b001000

    def PF(self) -> bool:
        return (self.FLAGS & 0b010000) == 0b010000

    def IF(self) -> bool:
        return (self.FLAGS & 0b100000) == 0b100000

    def setSF(self, value: bool):
        if value:
            self.FLAGS = self.FLAGS | 0b000001
        else:
            self.FLAGS = self.FLAGS & 0b111110

    def setOF(self, value: bool):
        if value:
            self.FLAGS = self.FLAGS | 0b000010
        else:
            self.FLAGS = self.FLAGS & 0b111101

    def setZF(self, value: bool):
        if value:
            self.FLAGS = self.FLAGS | 0b000100
        else:
            self.FLAGS = self.FLAGS & 0b111011

    def setCF(self, value: bool):
        if value:
            self.FLAGS = self.FLAGS | 0b001000
        else:
            self.FLAGS = self.FLAGS & 0b110111

    def setPF(self, value: bool):
        if value:
            self.FLAGS = self.FLAGS | 0b010000
        else:
            self.FLAGS = self.FLAGS & 0b101111

    def setIF(self, value: bool):
        if value:
            self.FLAGS = self.FLAGS | 0b100000
        else:
            self.FLAGS = self.FLAGS & 0b011111

    def makeWord(self, value: int) -> int:
        return value & 0xFFFF

    def cycle(self) -> bool:
        i = self.memory[self.IP]
        opcode = i & 0x00FF
        self.parameter1Mode = (i & 0xF000) >> 12
        self.parameter2Mode = (i & 0x0F00) >> 8
        instruction: Callable = self.instructionTable[opcode]
        return instruction()

    def setRegister(self, reg: int, value: int):
        if reg == self.REGAX:
            self.AX = self.makeWord(value)
        elif reg == self.REGBX:
            self.BX = self.makeWord(value)
        elif reg == self.REGCX:
            self.CX = self.makeWord(value)
        elif reg == self.REGDX:
            self.DX = self.makeWord(value)
        elif reg == self.REGIX:
            self.IX = self.makeWord(value)
        elif reg == self.REGIP:
            self.IP = self.makeWord(value)
        elif reg == self.REGSP:
            self.SP = self.makeWord(value)

    def getRegister(self, reg: int) -> int:
        if reg == self.REGAX:
            return self.AX
        elif reg == self.REGBX:
            return self.BX
        elif reg == self.REGCX:
            return self.CX
        elif reg == self.REGDX:
            return self.DX
        elif reg == self.REGIX:
            return self.IX
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
        elif paramMode == self.INDEXED:
            regValue = self.getRegister(memValue)
            return self.memory[regValue + self.IX]
        return -1    
    
    def setFlagsFromResult(self, value: int):
        self.setZF(value == 0)
        self.setSF(value < 0)
        self.setOF(value < (-2 ** 15) + 1)
        self.setPF(bin(value).count("1") % 2 == 0)
        self.setCF(value > (2 ** 16) - 1)
        # http://www.c-jump.com/CIS77/ASM/Flags/F77_0110_overflow_flag.htm

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

        if self.parameter1Mode != self.REGISTER and self.parameter1Mode != self.DIRECT:
            raise ExcecutionError("STOR: Bad Parameter 1", self.IP)

        if self.parameter2Mode != self.REFERENCE and self.parameter2Mode != self.INDEXED:
            raise ExcecutionError("STOR: Bad Parameter 2", self.IP)

        value = self.determineValue(self.parameter1Mode, self.memory[self.IP + 1])
        ref = self.getRegister(self.memory[self.IP + 2])
        if self.parameter2Mode == self.INDEXED:
            ref += self.IX
        self.memory[ref] = self.makeWord(value)

        self.IP += 3
        return True

    def CMP(self):
        # print("CMP")

        if self.parameter1Mode != self.REGISTER:
            raise ExcecutionError("CMP: Bad Parameter 1", self.IP)

        if self.parameter2Mode == self.REFERENCE:
            raise ExcecutionError("CMP: Bad Parameter 2", self.IP)

        value1 = self.determineValue(self.parameter1Mode, self.memory[self.IP + 1])
        value2 = self.determineValue(self.parameter2Mode, self.memory[self.IP + 2])

        self.setFlagsFromResult(value1 - value2)

        self.IP += 3
        return True

    def JZ(self):
        # print("JZ")

        if self.parameter1Mode != self.DIRECT:
            raise ExcecutionError("JZ: Bad Parameter 1", self.IP)

        if self.ZF() == True:
            self.IP = self.memory[self.IP + 1]
        else:
            self.IP += 2
        
        return True

    def JNZ(self):
        # print("JNZ")

        if self.parameter1Mode != self.DIRECT:
            raise ExcecutionError("JNZ: Bad Parameter 1", self.IP)

        if self.ZF() == False:
            self.IP = self.memory[self.IP + 1]
        else:
            self.IP += 2

        return True

    def JO(self):
        # print("JO")

        if self.parameter1Mode != self.DIRECT:
            raise ExcecutionError("JO: Bad Parameter 1", self.IP)

        if self.OF() == True:
            self.IP = self.memory[self.IP + 1]
        else:
            self.IP += 2

        return True

    def JNO(self):
        # print("JNO")

        if self.parameter1Mode != self.DIRECT:
            raise ExcecutionError("JNO: Bad Parameter 1", self.IP)

        if self.OF() == False:
            self.IP = self.memory[self.IP + 1]
        else:
            self.IP += 2

        return True

    def JC(self):
        # print("JC")

        if self.parameter1Mode != self.DIRECT:
            raise ExcecutionError("JC: Bad Parameter 1", self.IP)

        if self.CF() == True:
            self.IP = self.memory[self.IP + 1]
        else:
            self.IP += 2

        return True

    def JNC(self):
        # print("JNC")

        if self.parameter1Mode != self.DIRECT:
            raise ExcecutionError("JC: Bad Parameter 1", self.IP)

        if self.CF() == False:
            self.IP = self.memory[self.IP + 1]
        else:
            self.IP += 2

        return True

    def JL(self):
        # print("JL")

        if self.parameter1Mode != self.DIRECT:
            raise ExcecutionError("JL: Bad Parameter 1", self.IP)

        if self.OF() != self.SF():
            self.IP = self.memory[self.IP + 1]
        else:
            self.IP += 2

        return True

    def JLE(self):
        # print("JLE")

        if self.parameter1Mode != self.DIRECT:
            raise ExcecutionError("JLE: Bad Parameter 1", self.IP)

        if self.OF() != self.SF() or self.ZF:
            self.IP = self.memory[self.IP + 1]
        else:
            self.IP += 2

        return True

    def JG(self):
        # print("JG")

        if self.parameter1Mode != self.DIRECT:
            raise ExcecutionError("JG: Bad Parameter 1", self.IP)

        if self.ZF() == False and self.OF() == self.SF():
            self.IP = self.memory[self.IP + 1]
        else:
            self.IP += 2

        return True

    def JGE(self):
        # print("JGE")

        if self.parameter1Mode != self.DIRECT:
            raise ExcecutionError("JGE: Bad Parameter 1", self.IP)

        if self.OF() == self.SF():
            self.IP = self.memory[self.IP + 1]
        else:
            self.IP += 2

        return True

    def ADD(self):
        # print("ADD")

        if self.parameter1Mode != self.REGISTER:
            raise ExcecutionError("ADD: Bad Parameter 1", self.IP)

        if self.parameter2Mode == self.REFERENCE:
            raise ExcecutionError("ADD: Bad Parameter 2", self.IP)

        value1 = self.getRegister(self.memory[self.IP + 1])
        value2 = self.determineValue(self.parameter2Mode, self.memory[self.IP + 2])

        value1 += value2

        self.setRegister(self.memory[self.IP + 1], value1)

        self.setFlagsFromResult(value1)

        self.IP += 3
        return True

    def SUB(self):
        # print("SUB")

        if self.parameter1Mode != self.REGISTER:
            raise ExcecutionError("SUB: Bad Parameter 1", self.IP)

        if self.parameter2Mode == self.REFERENCE:
            raise ExcecutionError("SUB: Bad Parameter 2", self.IP)

        value1 = self.getRegister(self.memory[self.IP + 1])
        value2 = self.determineValue(self.parameter2Mode, self.memory[self.IP + 2])

        value1 -= value2

        self.setRegister(self.memory[self.IP + 1], value1)

        self.setFlagsFromResult(value1)

        self.IP += 3
        return True

    def MUL(self):
        # print("MUL")

        if self.parameter1Mode != self.REGISTER:
            raise ExcecutionError("MUL: Bad Parameter 1", self.IP)

        if self.parameter2Mode == self.REFERENCE:
            raise ExcecutionError("MUL: Bad Parameter 2", self.IP)

        value1 = self.getRegister(self.memory[self.IP + 1])
        value2 = self.determineValue(self.parameter2Mode, self.memory[self.IP + 2])

        value1 *= value2

        self.setRegister(self.memory[self.IP + 1], value1)

        self.setFlagsFromResult(value1)

        self.IP += 3
        return True

    def DIV(self):
        # print("DIV")

        if self.parameter1Mode != self.REGISTER:
            raise ExcecutionError("MUL: Bad Parameter 1", self.IP)

        if self.parameter2Mode == self.REFERENCE:
            raise ExcecutionError("MUL: Bad Parameter 2", self.IP)

        value1 = self.getRegister(self.memory[self.IP + 1])
        value2 = self.determineValue(self.parameter2Mode, self.memory[self.IP + 2])

        r = value1 % value2
        q = value1 // value2

        self.setRegister(self.memory[self.IP + 1], q)
        self.setRegister(Definitions.registers["DX"], r)

        self.IP += 3
        return True

    def DEC(self):
        # print("DEC")

        if self.parameter1Mode != self.REGISTER:
            raise ExcecutionError("DEC: Bad Parameter 1", self.IP)
        
        param1 = self.memory[self.IP + 1]
        value = self.getRegister(param1)
        value = value - 1
        self.setFlagsFromResult(value)
        self.setRegister(param1, value)

        self.IP += 2
        return True

    def INC(self):
        # print("INC")

        if self.parameter1Mode != self.REGISTER:
            raise ExcecutionError("INC: Bad Parameter 1", self.IP)
        
        param1 = self.memory[self.IP + 1]
        value = self.getRegister(param1)
        value = value + 1
        self.setFlagsFromResult(value)
        self.setRegister(param1, value)

        self.IP += 2
        return True

    def AND(self):
        # print("AND")

        if self.parameter1Mode != self.REGISTER:
            raise ExcecutionError("AND: Bad Parameter 1", self.IP)

        if self.parameter2Mode == self.REFERENCE:
            raise ExcecutionError("AND: Bad Parameter 2", self.IP)

        value1 = self.getRegister(self.memory[self.IP + 1])
        value2 = self.determineValue(self.parameter2Mode, self.memory[self.IP + 2])

        value1 = value1 & value2

        self.setRegister(self.memory[self.IP + 1], value1)

        self.setFlagsFromResult(value1)

        self.IP += 3
        return True
    
    def OR(self):
        # print("OR")

        if self.parameter1Mode != self.REGISTER:
            raise ExcecutionError("OR: Bad Parameter 1", self.IP)

        if self.parameter2Mode == self.REFERENCE:
            raise ExcecutionError("OR: Bad Parameter 2", self.IP)

        value1 = self.getRegister(self.memory[self.IP + 1])
        value2 = self.determineValue(self.parameter2Mode, self.memory[self.IP + 2])

        value1 = value1 | value2

        self.setRegister(self.memory[self.IP + 1], value1)

        self.setFlagsFromResult(value1)

        self.IP += 3
        return True
    
    def XOR(self):
        # print("XOR")

        if self.parameter1Mode != self.REGISTER:
            raise ExcecutionError("XOR: Bad Parameter 1", self.IP)

        if self.parameter2Mode == self.REFERENCE:
            raise ExcecutionError("XOR: Bad Parameter 2", self.IP)

        value1 = self.getRegister(self.memory[self.IP + 1])
        value2 = self.determineValue(self.parameter2Mode, self.memory[self.IP + 2])

        value1 = value1 ^ value2

        self.setRegister(self.memory[self.IP + 1], value1)

        self.setFlagsFromResult(value1)

        self.IP += 3
        return True
    
    def NOT(self):
        # print("NOT")

        if self.parameter1Mode != self.REGISTER:
            raise ExcecutionError("XOR: Bad Parameter 1", self.IP)

        value1 = self.getRegister(self.memory[self.IP + 1])
        value1 = ~value1

        self.setRegister(self.memory[self.IP + 1], value1)

        self.setFlagsFromResult(value1)

        self.IP += 2
        return True

    def PUSH(self):
        # print("PUSH")

        if self.parameter1Mode != self.REGISTER:
            raise ExcecutionError("PUSH: Bad Parameter 1", self.IP)

        value = self.getRegister(self.memory[self.IP + 1])
        self.memory[self.SP] = value
        self.SP += 1

        self.IP += 2
        return True
    
    def POP(self):
        # print("POP")

        if self.parameter1Mode != self.REGISTER:
            raise ExcecutionError("POP: Bad Parameter 1", self.IP)

        self.SP -= 1
        value = self.memory[self.SP]
        self.setRegister(self.memory[self.IP + 1], value)

        self.IP += 2
        return True

    def PUSHF(self):
        # print("PUSHF")

        self.memory[self.SP] = self.FLAGS
        self.SP += 1

        self.IP += 1
        return True
    
    def POPF(self):
        # print("POPF")

        self.SP -= 1
        self.FLAGS = self.memory[self.SP]

        self.IP += 1
        return True

    def CALL(self):
        # print("CALL")

        if self.parameter1Mode != self.DIRECT:
            raise ExcecutionError("CALL: Bad Parameter 1", self.IP)

        self.memory[self.SP] = self.IP + 2
        self.SP += 1

        self.IP = self.memory[self.IP + 1]

        return True
    
    def RET(self):
        # print("RET")

        self.SP -= 1
        self.IP = self.memory[self.SP]

        return True

    def SHL(self):
        # print("SHL")

        if self.parameter1Mode != self.REGISTER:
            raise ExcecutionError("SHL: Bad Parameter 1", self.IP)
        
        param1 = self.memory[self.IP + 1]
        value = self.getRegister(param1)
        value = value << 1
        self.setFlagsFromResult(value)
        self.setRegister(param1, value)

        self.IP += 2
        return True

    def SHR(self):
        # print("SHR")

        if self.parameter1Mode != self.REGISTER:
            raise ExcecutionError("SHR: Bad Parameter 1", self.IP)
        
        param1 = self.memory[self.IP + 1]
        value = self.getRegister(param1)
        value = value >> 1
        self.setFlagsFromResult(value)
        self.setRegister(param1, value)

        self.IP += 2
        return True

    def NOP(self):
        # print("NOP")

        # NOP : Nothing to do !

        self.IP += 1
        return True

    def HLT(self):
        # print("HLT")

        self.IP += 0
        return False
