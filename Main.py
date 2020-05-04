from Computer import *
from Debugger import *
from Preprocessor import *
from Assembler import *
from Compiler import *
from Exceptions import PreprocessorError, AssemblerError, CompilerError, ExcecutionError
from Cpu import *
import sys

# python -m mypy Main.py

def Run(source: str, debug: bool):

    try:
        prog = Program(source)

        preproc = Preprocessor()
        preproc.preprocess(prog)

        # for l in prog.preprocessed:
        #    print(l)

        assembler = Assembler()
        assembler.assemble(prog)

        # for l in prog.labels:
        #     print(l, f" Position: {l.position}")

        # for i in prog.instructions:
        #     print(i, f" Position: {i.position}  Label: {i.labelName}")
        #     for p in i.parameters:
        #         print(" ", p, end = "")
        #         if p.labelName != None:
        #             print(f"   {p.labelName}")
        #         else:
        #             print("")

        # for b in prog.binary:
        #     print("%04X " % b, end = "")

        # print("")

        computer = Computer()
        computer.loadProgram(prog)

        if debug == False:
            computer.run()
        else:
            debugger = Debugger(computer, prog)
            debugger.run()

    except PreprocessorError as e:
        print(e)

    except AssemblerError as e:
        print(e)

    except CompilerError as e:
        print(e)

    except Exception as e:
        raise e

if __name__ == "__main__":

    useDebugger = False
    source = None

    for i, arg in enumerate(sys.argv):
        if arg == "--debug":
            useDebugger = True
        elif arg[-5:] == ".iasm":
            source = arg
        
    if source == None:
        print("Usage: python Main.py <source> [--debug]")
    else:
        Run(source, useDebugger)

