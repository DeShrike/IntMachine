import Definitions

class Parameter():

    def __init__(self, mode: int, value: int):
        self.mode = mode
        self.value = value

    @classmethod
    def fromDirect(cls, value: int):
        return cls(Definitions.addressingModes["direct"], value)

    @classmethod
    def fromRef(cls, ref: int):
        return cls(Definitions.addressingModes["ref"], ref)

    @classmethod
    def fromRegister(cls, register: int):
        return cls(Definitions.addressingModes["register"], register)
