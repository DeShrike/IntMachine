from Definitions import *

class Parameter():

    def __init__(self, mode: int, value: int):
        self.mode = mode
        self.value = value

    @classmethod
    def fromDirect(cls, value: int) -> Parameter:
        return cls(addressingModes["direct"], value)

    @classmethod
    def fromRef(cls, ref: int) -> Parameter:
        return cls(addressingModes["ref"], ref)

    @classmethod
    def fromRegister(cls, register: int) -> Parameter:
        return cls(addressingModes[register], 0)
