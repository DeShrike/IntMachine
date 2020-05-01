from Definitions import *
from Exceptions import CompileError, ExcecutionError
from Instruction import *
from Label import *
from typing import List

class Program():

    def __init__(self, source: str):
        self.bootstrapSize: int = 4
        self.source = source
        self.compiled: bool = False
        self.instructions: List[Instruction] = []
        self.labels: List[Label] = []
        self.binary: List[int] = []

