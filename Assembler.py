from Definitions import *
from Exceptions import AssemblerError, ExcecutionError
from Program import *
from Instruction import *
from Label import *
from Parameter import *
from typing import List, Optional, Union
import re

class Assembler():

    def __init__(self):
        self.block: str = ""
        self.currentSourceFile: str = ""
        self.currentLineNumber: int = 0
        self.lastLabel = None

    def removeComment(self, line: str) -> str:
        ix = line.find("//")
        if ix >= 0:
            return line[:ix]
        return line

    def assemble(self, program: Program) -> None:
        self.program = program

        self.pass1()
        self.pass2()
        
        self.program.assembled = True

    def findLabel(self, name: Optional[str]):
        for l in self.program.labels:
            if l.name == name:
                return l
        return None

    def parseLine(self, line: str):
        line = self.removeComment(line)
        line = line.strip(" ")
        if line == "":
            return line, None

        inquote = False
        parts = []
        part = ""
        for char in line:
            if char.isspace() or char == ",":
                if inquote:
                    part = part + char
                else:
                    parts.append(part)
                    part = ""
            elif char == "\"":
                inquote = not inquote
            else:
                part = part + char

        parts.append(part)
        parts = list(filter(lambda w: w != "", parts))
        return line, parts

    def compileLine(self, lineNumber: int, parts) -> bool:
        partCount = len(parts)
        part0: str = parts[0].strip()

        if part0.endswith(":"):
            part0 = part0[:-1]
            datatype: Union[None, str] = None
            value: int = 0
            size: int = 0

            if partCount == 1:
                if self.block != "CODE":
                    raise AssemblerError("Label declaration not in CODE block", self.currentLineNumber + lineNumber, self.currentSourceFile)

                self.lastLabel = part0[:Definitions.MAXLABELNAMELENGTH]

            elif partCount == 3:
                if self.block != "DATA":
                    raise AssemblerError("Variable declaration not in DATA block", self.currentLineNumber + lineNumber, self.currentSourceFile)

                dt = parts[2]

                result = re.match("^([a-zA-Z]*)\\[([0-9]*)\\]$", dt)
                if result:
                    datatype = result.group(1)
                    size = int(result.group(2))

                    if datatype not in datatypes:
                        raise AssemblerError(f"Unknown datatype: '{datatype}'", self.currentLineNumber + lineNumber, self.currentSourceFile)

                    if size < 1 or size > 255:
                        raise AssemblerError("Bad data length", self.currentLineNumber + lineNumber, self.currentSourceFile)

                    if datatype == "string":
                        value = parts[1]
                    else:
                        value = Definitions.parseNumber(parts[1])
                    
                    if value == None:
                        raise AssemblerError(f"Bad Variable value: {parts[1]}", self.currentLineNumber + lineNumber, self.currentSourceFile)

                else:
                    raise AssemblerError("Syntax error: datatype", self.currentLineNumber + lineNumber, self.currentSourceFile)

            else:
                raise AssemblerError("Syntax error", self.currentLineNumber + lineNumber, self.currentSourceFile)

            label = Label(part0[:Definitions.MAXLABELNAMELENGTH], datatype, size, value)
            label.lineNumber = self.currentLineNumber + lineNumber
            label.sourceFile = self.currentSourceFile
            
            self.program.labels.append(label)

        elif part0 == "CODE":
            self.block = part0

        elif part0 == "DATA":
            self.block = part0

        elif part0 == "__source__":
            self.currentSourceFile = parts[1]

        elif part0 == "__line__":
            self.currentLineNumber = int(parts[1]) - lineNumber - 1

        elif part0 in instructions:
            instruction = instructions[part0].clone()
            instruction.sourceFile = self.currentSourceFile
            instruction.lineNumber = self.currentLineNumber + lineNumber
            instruction.labelName = self.lastLabel
            self.lastLabel = None

            if instruction.parameterCount != len(parts) - 1:
                raise AssemblerError(f"Incorrect argumentcount. Expected {instruction.parameterCount} got {len(parts) - 1}", self.currentLineNumber + lineNumber, self.currentSourceFile)
            
            if instruction.parameterCount >= 1:
                param = Parameter.fromString(parts[1])
                if param == None:
                    raise AssemblerError(f"Bad parameter: {parts[1]}", self.currentLineNumber + lineNumber, self.currentSourceFile)

                instruction.parameters.append(param)

            if instruction.parameterCount >= 2:
                param = Parameter.fromString(parts[2])
                if param == None:
                    raise AssemblerError(f"Bad parameter: {parts[2]}", self.currentLineNumber + lineNumber, self.currentSourceFile)

                instruction.parameters.append(param)

            self.program.instructions.append(instruction)

        else:
            raise AssemblerError("Syntax error", self.currentLineNumber + lineNumber, self.currentSourceFile)

        return True

    def addBootstrap(self):
        instruction = instructions["JMP"].clone()
        instruction.sourceFile = self.currentSourceFile
        instruction.lineNumber = 0
        param = Parameter.fromString("Main")
        instruction.parameters.append(param)
        self.program.instructions.insert(0, instruction)

        instruction = instructions["MOV"].clone()
        instruction.sourceFile = self.currentSourceFile
        instruction.lineNumber = 0
        param = Parameter.fromString("SP")
        instruction.parameters.append(param)
        param = Parameter.fromString("Stack")
        instruction.parameters.append(param)
        self.program.instructions.insert(0, instruction)

    def pass1(self) -> None:
        ''' Parse the lines and make Instructions and Labels '''
        
        self.program.instructions.clear()
        self.program.labels.clear()
        self.codeIndex = 0
        self.dataIndex = 0
        self.block = ""

        for ix, line in enumerate(self.program.preprocessed):
            line, parts = self.parseLine(line)
            if parts == None:
                continue
            
            if self.compileLine(ix, parts) == False:
                break

        self.addBootstrap()

        # print(f"PASS 1 - {len(self.program.instructions)} instructions - {len(self.program.labels)} variables")

    def pass2(self) -> None:
        ''' Convert the Labels and Instructions to binary '''

        self.program.binary.clear()

        # First calculate size of program
        codeSize: int = 0
        for i in self.program.instructions:
            i.position = codeSize
            codeSize += i.parameterCount + 1
            if i.labelName != None:
                l = self.findLabel(i.labelName)
                if l != None:
                    l.position = i.position

        # Now calculate size of data
        dataSize: int = 0
        positionInMemory: int = codeSize

        for l in self.program.labels:
            if l.size == 0:
                continue

            dataSize += l.size
            l.position = positionInMemory
            positionInMemory += l.size

        # Now correct instructions with position of labels
        for i in self.program.instructions:
            for p in i.parameters:
                if p.labelName != None:
                    l = self.findLabel(p.labelName)
                    if l == None:
                        raise AssemblerError(f"Unknown name: {p.labelName}", i.lineNumber, i.sourceFile)
                    else:
                        p.value = l.position

        # First add the instructions
        for i in self.program.instructions:
            b = i.getBytes()
            self.program.binary = self.program.binary + b

        # Now add the data
        for l in self.program.labels:
            b = l.getBytes()
            self.program.binary = self.program.binary + b

        # print(f"PASS 2 - Code Size: {codeSize} Data Size: {dataSize}")
