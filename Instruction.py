from Exceptions import AssemblerError, ExcecutionError
from Parameter import *
from typing import List, Union

class Instruction():

	def __init__(self, mnemonic: str, opcode: int, parameterCount: int):
		self.mnemonic: str = mnemonic
		self.opcode: int = opcode
		self.parameterCount : int = parameterCount
		self.parameters: List[Parameter] = []
		self.lineNumber: int = 0
		self.sourceFile: str = ""
		self.labelName: Union[str, None] = None
		self.position: int = 0

	def __repr__(self) -> str:
		return f"Instruction('{self.mnemonic}', {hex(self.opcode)}, {self.parameterCount})"

	def clone(self):
		i = Instruction(self.mnemonic, self.opcode, self.parameterCount)
		i.parameters = self.parameters[:]
		return i

	def getBytes(self) -> List[int]:
		if len(self.parameters) != self.parameterCount:
			raise AssemblerError("Parameter mismatch", self.lineNumber, self.sourceFile)

		b = [ self.opcode ]

		if self.parameterCount >= 1:
			p = self.parameters[0]
			m = p.mode << 12
			b[0] = b[0] | m
			b.append(p.value)

		if self.parameterCount == 2:
			p = self.parameters[1]
			m = p.mode << 8
			b[0] = b[0] | m
			b.append(p.value)

		return b

	def disassemble(self) -> str:
		disass = self.mnemonic + " "
		if len(self.parameters) >= 1:
			disass = disass + self.parameters[0].disassemble()
		if len(self.parameters) >= 2:
			disass = disass + ", " + self.parameters[1].disassemble()

		return disass