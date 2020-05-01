from Definitions import *
from Exceptions import CompileError, RunError
from Program import *
from Instruction import *
from Label import *
from Parameter import *
import re

class Compiler():

    def __init__(self):
        pass

    def removeComment(self, line: str) -> str:
        ix = line.find("//")
        if ix >= 0:
            return line[:ix]
        return line

    def compile(self, program: Program):
        self.program = program

        self.pass1()
        
        # add bootstrap code

        # JUMP to first program instruction
        i = instructions["JMP"].clone()
        i.parameters.append(Parameter.fromDirect(self.instructions[-1].memIndex))
        self.program.instructions.insert(0, i)

        # set SP
        i = instructions["MOV"].clone()
        i.parameters.append(Parameter.fromRegister("SP"))
        i.parameters.append(Parameter.fromDirect(self.instructions[-1].memIndex + self.instructions[-1].parameterCount + 1))
        self.program.instructions.insert(0, i)

        self.pass2()
        
        self.program.compiled = True

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
        part0 = parts[0].strip()

        if part0.endswith(":"):
            part0 = part0[:-1]
            datatype = None
            value = 0
            size = 0
            index = 0
            if partCount == 1:
                if self.block != "CODE":
                    raise CompileError("Label declaration not in CODE block", lineNumber)
                index = self.codeIndex
                # TODO self.codeIndex += 
            elif partCount == 3:
                if self.block != "DATA":
                    raise CompileError("Variable declaration not in DATA block", lineNumber)

                value = parts[1]
                dt = parts[2]

                result = re.match("([a-zA-Z]*)\\[([0-9]*)\\]", dt)
                if result:
                    datatype = result.group(1)
                    size = int(result.group(2))
                    if datatype not in datatypes:
                        raise CompileError(f"Unknown datatype: '{datatype}'", lineNumber)
                    if size < 1 or size > 128:
                        raise CompileError("Bad data length", lineNumber)
                else:
                    raise CompileError("Syntax error: datatype", lineNumber)

                index = self.dataIndex
                self.dataIndex += size
            else:
                raise CompileError("Syntax error", lineNumber)

            label = Label(part0, index, datatype, size, value) 
            self.labels.append(label)
        elif part0 == "CODE":
            self.block = part0
        elif part0 == "DATA":
            self.block = part0
        elif part0 == "IMPORT":
            pass
        elif part0 in instructions:
            instruction = instructions[part0].clone()
            instruction.memIndex = self.memIndex

            self.instructions.append(instruction)
        else:
            raise CompileError("Syntax error", lineNumber)

        return True

    def pass1(self) -> None:
        ''' Parse the lines and make Instructions '''
        lines = self.program.source.replace("\t", " ").split("\n")
        self.program.instructions.clear()
        self.program.labels.clear()
        self.program.binary.clear()
        self.codeIndex = self.bootstrapSize
        self.dataIndex = 0
        self.block = None

        for ix, line in enumerate(lines):
            line, parts = self.parseLine(line)
            if parts == None:
                continue
            
            if self.compileLine(ix, parts) == False:
                break

    def pass2(self) -> None:
        ''' Convert the Variables and Instructions to binary '''

        self.program.binary.clear()

        for i in self.program.instructions:
            b = i.getBytes()
            for ix, bb in enumerate(b):
                self.program.binary[ix + i.memIndex] = bb

        for l in self.program.labels:
            b = l.getBytes()
            for ix, bb in enumerate(b):
                self.program.binary[ix + l.position] = bb

