from Assembler import *
from Computer import *
from Compiler import *
from Exceptions import AssemblerError, CompilerError, ExcecutionError
from Cpu import *

if __name__ == "__main__":

    try:
        prog = Program("Prog1.sasm")

        assembler = Assembler()
        assembler.assemble(prog)

        for l in prog.labels:
            print(l)

        for i in prog.instructions:
            print(i)

        computer = Computer()
        computer.loadProgram(prog)
        computer.run()

    except AssemblerError as e:
        print(e)

    except CompilerError as e:
        print(e)

    except Exception as e:
        raise e

