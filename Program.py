from Instruction import *
from Label import *
from typing import List

class Program():

    def __init__(self, sourceFile: str):
        self.sourceFile: str = sourceFile
        self.bootstrapSize: int = 4
        self.assembled: bool = False
        self.instructions: List[Instruction] = []
        self.labels: List[Label] = []
        self.binary: List[int] = []

        self.source = Program.LoadFile(self.sourceFile)

    @staticmethod
    def LoadFile(filename: str) -> str:
        source: str = ""
        file = open(filename, "r")
        source = file.read()
        file.close()
        return source
