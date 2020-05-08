from Exceptions import ExcecutionError
from Cpu import *
from Program import *
from Computer import *
from Ansi import *
import time

class Debugger():

    INSTRUCTIONMODE = 1
    VARIABLEMODE = 2
    SLOW = 1
    FAST = 0.1
    MEMORYMODE = 1
    TEXTDISPLAYMODE = 2

    def __init__(self, computer: Computer, program: Program):
        self.computer = computer
        self.program = program
        self.mode = self.INSTRUCTIONMODE
        self.mode2 = self.MEMORYMODE
        self.scrollOffset = 0
        self.currentVariableStart = 0
        self.currectVariableSize = 0
        self.halted = False
        Ansi.Init()

    def stripFolderName(self, filename: str) -> str:
        return os.path.basename(filename)

    def updateDisplay(self):
        if self.mode == self.INSTRUCTIONMODE:
            self.showCurrentInstruction()
        elif self.mode == self.VARIABLEMODE:
            self.showVariables()

        if self.mode2 == self.MEMORYMODE:
            self.showMemory()
            print(Ansi.MoveCursor(1, 18) + Ansi.ClearLine, end = "")

        elif self.mode2 == self.TEXTDISPLAYMODE:
            self.showTextDisplay()

        self.showRegister("IP", self.computer.cpu.IP, 19, 1, Ansi.BrightYellow)
        self.showRegister("SP", self.computer.cpu.SP, 19, 19, Ansi.BrightMagenta)
        self.showRegister("IX", self.computer.cpu.IX, 19, 37)

        self.showRegister("AX", self.computer.cpu.AX, 20, 1)
        self.showRegister("BX", self.computer.cpu.BX, 20, 19)
        self.showRegister("CX", self.computer.cpu.CX, 20, 37)
        self.showRegister("DX", self.computer.cpu.DX, 20, 55)

        self.showFlags("SF", self.computer.cpu.SF(), 19, 57)
        self.showFlags("OF", self.computer.cpu.OF(), 19, 62)
        self.showFlags("ZF", self.computer.cpu.ZF(), 19, 67)
        self.showFlags("CF", self.computer.cpu.CF(), 19, 72)
        self.showFlags("PF", self.computer.cpu.PF(), 19, 77)
        self.showFlags("IF", self.computer.cpu.IF(), 20, 77)

        self.showKeys()
        print(Ansi.MoveCursor(1, 1), end = "")

        Ansi.Flush()

    def showTextDisplay(self):
        self.computer.display.render()

    def showCurrentInstruction(self):
        print(Ansi.MoveCursor(1, 21) + Ansi.ClearLine, end = "")
        print(Ansi.MoveCursor(1, 22) + Ansi.ClearLine, end = "")
        for i in self.program.instructions:
            if i.position == self.computer.cpu.IP:
                disass = i.disassemble()
                label = i.labelName if i.labelName != None else ""
                print(Ansi.MoveCursor(1, 21) + Ansi.White + "%12s " % label, end = "")
                print(Ansi.BrightYellow + "%04X " % i.position + Ansi.Reset, end = "")
                print(Ansi.Yellow + "%-30s" % disass + " " + Ansi.Reset, end = "")

                print(Ansi.MoveCursor(55, 21), end ="")
                print(Ansi.Green + "%20s " % self.stripFolderName(i.sourceFile) + Ansi.Reset, end = "")
                print("(" + Ansi.BrightGreen + "%d" % i.lineNumber + Ansi.Reset + ")", end = "")
                bb = i.getBytes()
                print(Ansi.MoveCursor(19, 22) + Ansi.Yellow, end = "")
                for b in bb:
                    print("%04X " % b, end = "")
                break

    def showVariable(self, line: int, label: Label):
        print(Ansi.MoveCursor(1, line) + Ansi.Yellow + ("-> " if line == 21 else "   "), end = "")
        print(Ansi.White + "%12s " % label.name, end = "")
        print("[" + (Ansi.BrightGreen if line == 21 else Ansi.BrightWhite) + "%04X" % label.position + Ansi.Reset + Ansi.White + "] ", end = "")
        if label.datatype != None:
            print("(%s[%d]) = " % (label.datatype, label.size), end = "")

        print(Ansi.MoveCursor(55, line), end ="")
        print(Ansi.Green + "%20s " % self.stripFolderName(label.sourceFile) + Ansi.Reset, end = "")
        print("(" + Ansi.BrightGreen + "%d" % label.lineNumber + Ansi.Reset + ")", end = "")

    def showVariables(self):
        print(Ansi.MoveCursor(1, 21) + Ansi.ClearLine, end = "")
        print(Ansi.MoveCursor(1, 22) + Ansi.ClearLine, end = "")
        self.scrollOffset = max(0, min(len(self.program.labels) - 1, self.scrollOffset))

        label = self.program.labels[self.scrollOffset]
        self.showVariable(21, label)

        self.currentVariableStart = label.position
        self.currectVariableSize = label.size

        if len(self.program.labels) >= self.scrollOffset + 2:
            label = self.program.labels[self.scrollOffset + 1]
            self.showVariable(22, label)

    def showRegister(self, name: str, value: int, line: int, col: int, color: str = Ansi.BrightWhite):
        print(Ansi.MoveCursor(col, line) + Ansi.GreenBackground + Ansi.BrightWhite + " %s " % name + Ansi.Reset, end = "")
        print(color + " %04X" % value + Ansi.Reset + " (" + color + "%5d" % value + Ansi.Reset + ")", end = "")

    def showFlags(self, name: str, value: bool, line: int, col: int):
        print(Ansi.MoveCursor(col, line), end = "")
        if value:
            print(Ansi.GreenBackground + Ansi.BrightWhite + " %s " % name + Ansi.Reset, end = "")
        else:
            print(Ansi.RedBackground + " %s " % name + Ansi.Reset, end = "")

    def showKeys(self):
        keys = { 
            "M": "Scrn" if self.mode2 == self.MEMORYMODE else "Memo", 
            "C": "Code", 
            "V": "Vars", 
            "W": "Slow", 
            "F": "Fast", 
            "R": "Run" if self.halted == False else "   ", 
            "S": "Step" if self.halted == False else "    ", 
            "T": "Reset", 
            "Q": "Quit" 
            }
        print(Ansi.MoveCursor(1, 23), end = "")
        for k in keys:
            print(Ansi.RedBackground + Ansi.BrightBlue + " %s " % k + Ansi.Black + "%s " % keys[k] + Ansi.Reset + " ", end = "")

    def showMemory(self):
        for x in range(16):
            c = x * 5 + 1
            print(Ansi.MoveCursor(c, 1) + Ansi.BlueBackground + Ansi.BrightWhite + (" %4X" % x) + Ansi.Reset, end = "")
            for y in range(16):
                pos = y * 16 + x
                l = y + 2

                print(Ansi.MoveCursor(1, l) + Ansi.BlueBackground + Ansi.BrightWhite + ("%1X" % y) + Ansi.Reset, end = "")
                memValue = self.computer.memory[pos]
                color = Ansi.White
                if self.computer.cpu.IP == pos:
                    color = Ansi.BrightYellow
                elif self.computer.cpu.SP == pos:
                    color = Ansi.BrightMagenta
                elif self.mode == self.VARIABLEMODE and pos >= self.currentVariableStart and pos < self.currentVariableStart + self.currectVariableSize:
                    color = Ansi.BrightGreen

                print(Ansi.MoveCursor(c, l) + color + (" %04X " % memValue) + Ansi.Reset, end = "")

    def run(self):
        print(Ansi.HideCursor + Ansi.Clear, end = "")
        self.computer.cpu.reset()
        self.updateDisplay()
        delayTime = 1
        stepMode = True
        self.halted = False
        while True:
            ch = Ansi.GetKey()
            if ch == Ansi.ESC:
                pass
            elif ch == Ansi.ENTER:
                pass
            elif ch == Ansi.ARROWDOWN or ch == ord("U") or ch == ord("u"):
                if self.mode == self.VARIABLEMODE:
                    self.scrollOffset += 1
                    self.updateDisplay()
            elif ch == Ansi.ARROWUP or ch == ord("D") or ch == ord("d"):
                if self.mode == self.VARIABLEMODE:
                    self.scrollOffset -= 1
                    self.updateDisplay()
            elif ch == ord("Q") or ch == ord("q"):
                break
            elif ch == ord("R") or ch == ord("r"):
                stepMode = False
            elif ch == ord("S") or ch == ord("s"):
                stepMode = True
                if self.halted == False:
                    if self.computer.cpu.cycle() == False:
                        self.halted = True
                self.updateDisplay()
            elif ch == ord("C") or ch == ord("c"):
                self.mode = self.INSTRUCTIONMODE
                self.updateDisplay()
            elif ch == ord("V") or ch == ord("v"):
                self.mode = self.VARIABLEMODE
                self.updateDisplay()
            elif ch == ord("M") or ch == ord("m"):
                self.mode2 = self.TEXTDISPLAYMODE if self.mode2 == self.MEMORYMODE else self.MEMORYMODE
                self.updateDisplay()
            elif ch == ord("F") or ch == ord("f"):
                delayTime = self.FAST
            elif ch == ord("W") or ch == ord("w"):
                delayTime = self.SLOW
            elif ch == ord("T") or ch == ord("t"):
                self.computer.cpu.reset()
                stepMode = True
                delayTime = self.SLOW
                self.halted = False
                self.updateDisplay()
            else:
                if ch != None:
                    print(Ansi.MoveCursor(1, 23) + "%d  " % ch, end = "")

            if stepMode == False:
                if self.halted == False:
                    if self.computer.cpu.cycle() == False:
                        self.halted = True
                    self.updateDisplay()
                    time.sleep(delayTime)
                else:
                    time.sleep(0.1)

            else:
                time.sleep(0.1)

        print(Ansi.MoveCursor(1, 25) + Ansi.Reset + Ansi.ShowCursor, end = "")
