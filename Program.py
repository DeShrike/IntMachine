from Definitions import *
from Exceptions import CompileError, RunError
from Instruction import *
from Label import *
from Parameter import *
import re

class Program():

    def __init__(self, source: str):
        self.bootstrapSize: int = 4
        self.source = source
        self.compiled: bool = False
        self.instructions = []
        self.labels = []
        self.binary = []

