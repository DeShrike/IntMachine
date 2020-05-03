from Exceptions import ExcecutionError
from Cpu import *
from Program import *
from Computer import *
import Ansi
import sys
import time

class Debugger():

    INSTRUCTIONMODE = 1
    VARIABLEMODE = 2
    SLOW = 1
    FAST = 0.1

    def __init__(self, computer: Computer, program: Program):
        self.computer = computer
        self.program = program
        self.mode = self.INSTRUCTIONMODE
        self.scrollOffset = 0
        self.currentVariableStart = 0
        self.currectVariableSize = 0
        self.halted = False
        Ansi.InitAnsi()

    def updateDisplay(self):
        if self.mode == self.INSTRUCTIONMODE:
            self.showCurrentInstruction()
        elif self.mode == self.VARIABLEMODE:
            self.showVariables()

        self.showMemory()

        self.showRegister("IP", self.computer.cpu.IP, 19, 1, Ansi.BrightYellow)
        self.showRegister("SP", self.computer.cpu.SP, 19, 21, Ansi.BrightMagenta)
        self.showRegister("AX", self.computer.cpu.AX, 20, 1)
        self.showRegister("BX", self.computer.cpu.BX, 20, 21)
        self.showRegister("CX", self.computer.cpu.CX, 20, 41)
        self.showRegister("DX", self.computer.cpu.DX, 20, 61)

        self.showFlags("SF", self.computer.cpu.SF(), 19, 42)
        self.showFlags("OF", self.computer.cpu.OF(), 19, 47)
        self.showFlags("ZF", self.computer.cpu.ZF(), 19, 52)
        self.showFlags("CF", self.computer.cpu.CF(), 19, 57)
        self.showFlags("PF", self.computer.cpu.PF(), 19, 62)
        self.showFlags("IF", self.computer.cpu.IF(), 19, 67)

        self.showKeys()
        print(Ansi.MoveCursor(1, 1), end = "")

        sys.stdout.flush()

    def showCurrentInstruction(self):
        print(Ansi.MoveCursor(1, 22) + Ansi.ClearLine, end = "")
        print(Ansi.MoveCursor(1, 23) + Ansi.ClearLine, end = "")
        for i in self.program.instructions:
            if i.position == self.computer.cpu.IP:
                disass = i.disassemble()
                label = i.labelName if i.labelName != None else ""
                print(Ansi.MoveCursor(1, 22) + Ansi.White + "%10s " % label, end = "")
                print(Ansi.BrightYellow + "%04X " % i.position + Ansi.Reset, end = "")
                print(Ansi.Yellow + "%-30s" % disass + " " + Ansi.Reset, end = "")

                print(Ansi.MoveCursor(55, 22), end ="")
                print(Ansi.Green + "%20s " % i.sourceFile + Ansi.Reset, end = "")
                print("(" + Ansi.BrightGreen + "%d" % i.lineNumber + Ansi.Reset + ")  ", end = "")
                bb = i.getBytes()
                print(Ansi.MoveCursor(17, 23) + Ansi.Yellow, end = "")
                for b in bb:
                    print("%04X " % b, end = "")
                break

    def showVariable(self, line: int, label: Label):
        print(Ansi.MoveCursor(1, line) + Ansi.Yellow + "-> " if line == 22 else "   ", end = "")
        print(Ansi.White + "%10s " % label.name, end = "")
        print("[" + (Ansi.BrightGreen if line == 22 else Ansi.BrightWhite) + "%04X" % label.position + Ansi.Reset + Ansi.White + "] ", end = "")
        if label.datatype != None:
            print("(%s[%d]) = " % (label.datatype, label.size), end = "")

        print(Ansi.MoveCursor(55, line), end ="")
        print(Ansi.Green + "%20s " % label.sourceFile + Ansi.Reset, end = "")
        print("(" + Ansi.BrightGreen + "%d" % label.lineNumber + Ansi.Reset + ")  ", end = "")

    def showVariables(self):
        print(Ansi.MoveCursor(1, 22) + Ansi.ClearLine, end = "")
        print(Ansi.MoveCursor(1, 23) + Ansi.ClearLine, end = "")
        self.scrollOffset = max(0, min(len(self.program.labels) - 1, self.scrollOffset))

        label = self.program.labels[self.scrollOffset]
        self.showVariable(22, label)

        self.currentVariableStart = label.position
        self.currectVariableSize = label.size

        if len(self.program.labels) >= self.scrollOffset + 2:
            label = self.program.labels[self.scrollOffset + 1]
            self.showVariable(23, label)

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
            "A": "    ", 
            "C": "Code", 
            "V": "Vars", 
            "W": "Slow", 
            "F": "Fast", 
            "R": "Run" if self.halted == False else "   ", 
            "S": "Step" if self.halted == False else "    ", 
            "T": "Reset", 
            "Q": "Quit" 
            }
        print(Ansi.MoveCursor(1, 25), end = "")
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

                if self.mode == self.VARIABLEMODE and pos >= self.currentVariableStart and pos < self.currentVariableStart + self.currectVariableSize:
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
            ch = Ansi.ReadChar()
            if ch == Ansi.ESC:
                pass
            elif ch == Ansi.ENTER:
                pass
            elif ch == Ansi.ARROWDOWN:
                if self.mode == self.VARIABLEMODE:
                    self.scrollOffset += 1
                    self.updateDisplay()
            elif ch == Ansi.ARROWUP:
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
            elif ch == ord("F") or ch == ord("f"):
                delayTime = self.FAST
            elif ch == ord("w") or ch == ord("w"):
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
