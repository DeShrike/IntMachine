from typing import List, Optional

class Label():

    def __init__(self, name: str, datatype: Optional[str], size: int, value):
        self.name = name
        self.datatype = datatype
        self.size = size
        self.value = value
        self.position = 0

    def __repr__(self) -> str:
        if self.datatype == "string":
            return f"Label('{self.name}', '{self.datatype}', {self.size}, '{self.value}')"
        else:
            return f"Label('{self.name}', '{self.datatype}', {self.size}, {self.value})"

    def getBytes(self) -> List[int]:
        if self.datatype == "string":
            ret = [ord(x) for x in self.value]
            padding = [0 for _ in range(self.size - len(self.value))]
            return ret + padding
        else:
            return [self.value for _ in range(self.size)]

