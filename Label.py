from typing import List, Optional

class Label():

    def __init__(self, name: str, position: int, datatype: Optional[str], size: int, value):
        self.name = name
        self.position = position
        self.datatype = datatype
        self.size = size
        self.value = value

    def __repr__(self) -> str:
        if self.datatype == "string":
            return f"Label('{self.name}', {self.position}, '{self.datatype}', {self.size}, '{self.value}')"
        else:
            return f"Label('{self.name}', {self.position}, '{self.datatype}', {self.size}, {self.value})"

    def getBytes(self) -> List[int]:
        return [0 for _ in range(self.size)]
