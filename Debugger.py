from Exceptions import ExcecutionError
from Cpu import *
from Program import *
from Computer import *
import Ansi
import sys
import time

class Debugger():

    def __init__(self, computer: Computer, program: Program):
        self.computer = computer
        self.program = program
        Ansi.InitAnsi()

    def updateDisplay(self):
        self.showMemory()

        self.showRegister("IP", self.computer.cpu.IP, 19, 1)
        self.showRegister("SP", self.computer.cpu.SP, 19, 21)
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

        self.showCurrentInstruction()

        self.showKeys()
        print(Ansi.MoveCursor(1, 1), end = "")

        sys.stdout.flush()

    def showCurrentInstruction(self):
        for i in self.program.instructions:
            if i.position == self.computer.cpu.IP:
                disass = i.disassemble()
                label = i.labelName if i.labelName != None else ""
                print(Ansi.MoveCursor(1, 22) + Ansi.White + "%10s " % label, end = "")
                print(Ansi.BrightYellow + "%04X " % i.position + Ansi.Reset + Ansi.Yellow + disass + " " + Ansi.Reset, end = "")
                break

    def showRegister(self, name: str, value: int, line: int, col: int):
        print(Ansi.MoveCursor(col, line) + Ansi.GreenBackground + Ansi.BrightWhite + " %s " % name + Ansi.Reset, end = "")
        print(" 0x" + Ansi.BrightYellow + "%04X" % value + Ansi.Reset + " (" + Ansi.BrightYellow + "%5d" % value + Ansi.Reset + ")", end = "")

    def showFlags(self, name: str, value: bool, line: int, col: int):
        print(Ansi.MoveCursor(col, line), end = "")
        if value:
            print(Ansi.GreenBackground + Ansi.BrightWhite + " %s " % name + Ansi.Reset, end = "")
        else:
            print(Ansi.RedBackground + " %s " % name + Ansi.Reset, end = "")

    def showKeys(self):
        keys = { "A": "    ", "T": "Reset", "C": "Code", "V": "Vars", "W": "Slow", "F": "Fast", "R": "Run", "S": "Step", "Q": "Quit" }
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
                    color = Ansi.BrightWhite

                print(Ansi.MoveCursor(c, l) + color + (" %04X " % memValue) + Ansi.Reset, end = "")

    def run(self):
        print(Ansi.HideCursor + Ansi.Clear, end = "")
        self.computer.cpu.reset()
        self.updateDisplay()
        delayTime = 1
        stepMode = True
        SLOW = 1
        FAST = 0.001
        done = False
        while True:
            ch = Ansi.ReadChar()
            if ch == Ansi.ESC:
                break
            elif ch == Ansi.ENTER:
                pass
            elif ch == ord("Q") or ch == ord("q"):
                break
            elif ch == ord("R") or ch == ord("r"):
                stepMode = False
            elif ch == ord("S") or ch == ord("s"):
                stepMode = True
                if done == False:
                    if self.computer.cpu.cycle() == False:
                        done = True
                self.updateDisplay()
            elif ch == ord("C") or ch == ord("c"):
                pass
            elif ch == ord("V") or ch == ord("v"):
                pass
            elif ch == ord("F") or ch == ord("f"):
                delayTime = FAST
            elif ch == ord("w") or ch == ord("w"):
                delayTime = SLOW
            elif ch == ord("T") or ch == ord("t"):
                self.computer.cpu.reset()
                stepMode = True
                delayTime = SLOW
                done = False
                self.updateDisplay()
            else:
                if ch != None:
                    print(Ansi.MoveCursor(1, 23) + "%d  " % ch, end = "")

            if stepMode == False:
                if done == False:
                    if self.computer.cpu.cycle() == False:
                        done = True
                self.updateDisplay()
                time.sleep(delayTime)

            time.sleep(0.1)

        print(Ansi.MoveCursor(1, 25) + Ansi.Reset + Ansi.ShowCursor, end = "")

    def step(self):
        pass
