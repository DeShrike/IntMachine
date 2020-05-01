import Definitions
from Exceptions import *
from Instruction import *
from Label import *
from Parameter import *
import re

class Cpu():

    def __init__(self, memory):
        self.memory = memory
        self.reset()

        self.instructionTable = {
            0x0010: self.MOV,
            0x0011: self.CMP,
            
            0x0012: self.ADD,
            0x0013: self.SUB,
            0x0014: self.MUL,
            0x0015: self.DIV,

            0x0016: self.JMP,
            0x0017: self.JZ,
            0x0016: self.JNZ,
            0x0019: self.JO,
            0x0020: self.JNO,
            0x0021: self.JC,
            0x0022: self.JNC,

            0x0023: self.DEC,
            0x0024: self.INC,

            0x0025: self.AND,
            0x0026: self.OR,
            0x0027: self.XOR,
            0x0029: self.NOT,

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

    def cycle(self):
        i = self.memory[self.IP]
        opcode = i & 0x00FF
        print(hex(opcode))
        instruction = self.instructionTable[opcode]
        return instruction()

    def JMP(self):
        return True

    def MOV(self):
        return True

    def STOR(self):
        return True

    def CMP(self):
        return True

    def JZ(self):
        return True

    def JNZ(self):
        return True

    def JO(self):
        return True

    def JNO(self):
        return True

    def JC(self):
        return True

    def JNC(self):
        return True

    def JL(self):
        return True

    def JLE(self):
        return True

    def JG(self):
        return True

    def JGE(self):
        return True

    def ADD(self):
        return True

    def SUB(self):
        return True

    def MUL(self):
        return True

    def DIV(self):
        return True

    def DEC(self):
        return True

    def INC(self):
        return True

    def AND(self):
        return True
    
    def OR(self):
        return True
    
    def XOR(self):
        return True
    
    def NOT(self):
        return True

    def PUSH(self):
        return True
    
    def POP(self):
        return True

    def PUSHF(self):
        return True
    
    def POPF(self):
        return True

    def CALL(self):
        return True
    
    def RET(self):
        return True

    def SHL(self):
        return True

    def SHR(self):
        return True

    def HLT(self):
        return False
