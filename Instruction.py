from Exceptions import CompileError, RunError

class Instruction():

	def __init__(self, mnemonic: str, opcode: int, parameterCount: int):
		self.mnemonic = mnemonic
		self.opcode = opcode
		self.parameterCount = parameterCount
		self.parameters = []
		self.memIndex = 0
		self.lineNumber = 0

	def __repr__(self) -> str:
		return f"Instruction('{self.mnemonic}', {hex(self.opcode)}, {self.parameterCount})"

	def clone(self) -> Instruction:
		i = Instruction(self.mnemonic, self.opcode, self.parameterCount, self.cycles)
		i.parameters = self.parameters[:]
		i.memIndex = self.memIndex
		return i

	def getBytes(self) -> List[int]:
		if len(self.parameters) != self.parameterCount:
			raise CompileError("Paramete mismatch", self.lineNumber)

		b = [ self.opcode ]

		if self.parameterCount >= 1:
			p = self.parameters[0]
			m = p.mode << 8
			b[0] = b[0] | m
			b.append(p.value)

		if self.parameterCount == 2:
			p = self.parameters[1]
			m = p.mode << 12
			b[0] = b[0] | m
			b.append(p.value)

		return b
