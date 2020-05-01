from Computer import *
from Compiler import *
from Exceptions import CompileError, RunError
from Cpu import *

def LoadFile(filename: str) -> str:
    source: str = ""
    file = open(filename, "r") 
    for line in file:
        source.append(line)
    file.close()
    return source


if __name__ == "__main__":

    try:
        source = LoadFile("Prog1.sasm")
        prog = Program(source)

        compiler = Compiler()
        compiler.compile(prog)

        for l in prog.labels:
            print(l)

        for i in prog.instructions:
            print(i)

        computer = Computer()
        computer.loadProgram(prog)
        computer.run()

    except CompileError as e:
        print(e)

    except Exception as e:
        raise e

