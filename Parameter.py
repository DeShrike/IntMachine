import Definitions
import re

class Parameter():

    def __init__(self, mode: int, value: int):
        self.mode = mode
        self.value = value
        self.labelName = None

    def __repr__(self) -> str:
        return f"Parameter({self.mode}, {hex(self.value)})"

    @classmethod
    def fromDirect(cls, value: int) -> "Parameter":
        return cls(Definitions.addressingModes["direct"], value)

    @classmethod
    def fromLabel(cls, name: str) -> "Parameter":
        ret = cls(Definitions.addressingModes["direct"], 0)
        ret.labelName = name
        return ret

    @classmethod
    def fromRef(cls, register: int) -> "Parameter":
        return cls(Definitions.addressingModes["reference"], register)

    @classmethod
    def fromRegister(cls, register: int) -> "Parameter":
        return cls(Definitions.addressingModes["register"], register)

    @staticmethod
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

    @classmethod
    def fromString(cls, val: str) -> "Parameter":
        if val in Definitions.registers:
            return Parameter.fromRegister(Definitions.registers[val])

        if re.match("^\\[([A-D]X|SP|IP)\\]$", val):
            val = val[1:-1]
            return Parameter.fromRef(Definitions.registers[val])

        n = Parameter.ParseNumber(val)
        if n != None:
            return Parameter.fromDirect(n)

        if re.match("^([0-9a-zA-Z_]{1,32})$", val):
            return Parameter.fromLabel(val)

        return None
