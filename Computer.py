from Exceptions import ExcecutionError
from Cpu import *
from Display import *
from Program import *

class Computer():

	def __init__(self):
		self.memorySize = 0xFFFF
		self.memory = [0 for _ in range(self.memorySize)]
		self.display = Display()
		self.cpu = Cpu(self)
	
	def loadProgram(self, program: Program) -> None:
		if program.assembled == False:
			raise ExcecutionError("Program not compiled", 0)

		for ix, byte in enumerate(program.binary):
			self.memory[ix] = byte

	def run(self) -> None:
		Ansi.Init()
		print(Ansi.HideCursor + Ansi.Clear)
		self.cpu.reset()
		while self.cpu.cycle():
			self.display.render()
			pass
		print(Ansi.ShowCursor)
