import Definitions
from typing import Union, Optional
import re

class Parameter():

    DIRECT = "direct"
    REF = "reference"
    REGISTER = "register"

    def __init__(self, mode: int, value: int):
        self.mode = mode
        self.value = value
        self.labelName: Optional[str] = None

    def __repr__(self) -> str:
        return f"Parameter({self.mode}, {hex(self.value)})"

    @classmethod
    def fromDirect(cls, value: int) -> "Parameter":
        return cls(Definitions.addressingModes[cls.DIRECT], value)

    @classmethod
    def fromLabel(cls, name: str) -> "Parameter":
        ret = cls(Definitions.addressingModes[cls.DIRECT], 0)
        ret.labelName = name
        return ret

    @classmethod
    def fromRef(cls, register: int) -> "Parameter":
        return cls(Definitions.addressingModes[cls.REF], register)

    @classmethod
    def fromRegister(cls, register: int) -> "Parameter":
        return cls(Definitions.addressingModes[cls.REGISTER], register)

    @classmethod
    def fromString(cls, val: str) -> Union["Parameter", None]:
        if val in Definitions.registers:
            return Parameter.fromRegister(Definitions.registers[val])

        if re.match("^\\[([A-D]X|SP|IP)\\]$", val):
            val = val[1:-1]
            return Parameter.fromRef(Definitions.registers[val])

        n = Definitions.parseNumber(val)
        if n != None:
            return Parameter.fromDirect(n)

        if re.match("^([0-9a-zA-Z_]{1,32})$", val):
            return Parameter.fromLabel(val[:10])

        return None

    @staticmethod
    def findRegister(reg: int) -> str:
        for k, v in Definitions.registers.items():
            if v == reg:
                return k
        return "??"

    def disassemble(self) -> str:
        disass = ""
        if self.mode == Definitions.addressingModes[self.DIRECT]:
            if self.labelName != None:
                disass = self.labelName + ":"
            disass += "%04X(%d)" % (self.value, self.value)
        elif self.mode == Definitions.addressingModes[self.REGISTER]:
            disass = Parameter.findRegister(self.value)
        elif self.mode == Definitions.addressingModes[self.REF]:
            disass = "[" + Parameter.findRegister(self.value) + "]"
        else:
            disass = "(ERROR)"
        return disass
