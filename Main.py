from Computer import *
from Preprocessor import *
from Assembler import *
from Compiler import *
from Exceptions import PreprocessorError, AssemblerError, CompilerError, ExcecutionError
from Cpu import *

# python -m mypy Main.py

if __name__ == "__main__":

    try:
        prog = Program("Prog0.iasm")

        preproc = Preprocessor()
        preproc.preprocess(prog)

        for l in prog.preprocessed:
            print(l)

        assembler = Assembler()
        assembler.assemble(prog)

        # for l in prog.labels:
        #    print(l)

        # for i in prog.instructions:
        #    print(i)

        #computer = Computer()
        #computer.loadProgram(prog)
        #computer.run()

    except PreprocessorError as e:
        print(e)

    except AssemblerError as e:
        print(e)

    except CompilerError as e:
        print(e)

    except Exception as e:
        raise e

