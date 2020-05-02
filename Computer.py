from Exceptions import ExcecutionError
from Cpu import *
from Program import *

class Computer():

	def __init__(self):
		self.memorySize = 1024
		self.memory = [0 for _ in range(self.memorySize)]
		self.cpu = Cpu(self.memory)

	def loadProgram(self, program: Program) -> None:
		if program.assembled == False:
			raise ExcecutionError("Program not compiled", 0)

		for ix, byte in enumerate(program.binary):
			self.memory[ix] = byte

	def run(self) -> None:
		self.cpu.reset()
		while self.cpu.cycle():
			pass

