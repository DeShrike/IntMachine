from Instruction import *
from Label import *
from typing import List
from Exceptions import PreprocessorError
import os.path

class Program():

    def __init__(self, sourceFile: str):
        self.sourceFile: str = sourceFile
        self.bootstrapSize: int = 4
        self.assembled: bool = False
        self.instructions: List[Instruction] = []
        self.labels: List[Label] = []
        self.binary: List[int] = []

        self.source = Program.LoadFile(self.sourceFile)
        self.preprocessed: List[str] = []
        
    @staticmethod
    def LoadFile(filename: str) -> str:
        if os.path.isfile(filename) == False:
            raise PreprocessorError(f"File not found : {filename}", 0, "")

        source: str = ""
        with open(filename, "r") as file:
            source = file.read()

        return source
