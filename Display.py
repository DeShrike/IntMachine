from Ansi import *

class Display():
	lines = 16
	columns = 64

	startAddress = 0xF000
	memorySize = lines * columns * 2

	# uses 2 words per character (2 bytes) 2K words total
	# first byte is the color/style
	# second byte is the character

	def __init__(self):
		self.memory = [0 for _ in range(self.memorySize)]
		# set all color to White
		for c in range(self.memorySize // 2):
			self.memory[c * 2] = 7
		self.needsRefresh = True

	def render(self):
		if self.needsRefresh == False:
			return

		lastcol = -1
		print(Ansi.MoveCursor(1, 1) + Ansi.BlueBackground + Ansi.BrightWhite, end = "")
		print("+" + ("-" * self.columns) + "+", end = "")
		for l in range(self.lines):
			print(Ansi.MoveCursor(1, 2 + l) + Ansi.BlueBackground + Ansi.BrightWhite + "|" + Ansi.Reset, end = "")

			for c in range(self.columns):
				mempos = l * (self.columns * 2) + (c * 2)
				col = self.memory[mempos]
				if col != lastcol:
					lastcol = col
					print(Ansi.SetColor(col), end = "")

				cha = chr(self.memory[mempos + 1])
				print(cha, end = "")

			print(Ansi.MoveCursor(2 + self.columns, 2 + l) + Ansi.BlueBackground + Ansi.BrightWhite + "|" + Ansi.Reset, end = "")

		print(Ansi.MoveCursor(1, 2 + self.lines) + Ansi.BlueBackground + Ansi.BrightWhite, end = "")
		print("+" + ("-" * self.columns) + "+" + Ansi.Reset, end = "")

		self.needsRefresh = False

	def prepareRender(self):
		for l in range(self.lines + 2):
			print(Ansi.MoveCursor(1, l) + Ansi.ClearLine, end = "")

	def setMemory(self, position: int, value: int):
		oldValue = self.memory[position]
		if oldValue != value:
			self.memory[position] = value
			self.needsRefresh = True
