from Definitions import *
from Exceptions import PreprocessorError
from Program import *
from typing import List, Optional, Union
import re

class Preprocessor():
    """ 
    Processes IMPORT instructions and adds indicators with filename and linenumber :
    Like this:

    __source__ file.iasm
    __line__ 10

    The assembler uses these lines to keep track of the line/sourcefile

    """

    def __init__(self):
        pass

    def preprocess(self, program: Program) -> None:
        print(f"PREPROCESSING {program.sourceFile}")

        lines = program.source.replace("\t", " ").split("\n")

        program.preprocessed.clear()
        program.preprocessed.append(f"__source__ { program.sourceFile }")
        program.preprocessed.append(f"__line__ {1}")

        for ix, line in enumerate(lines):
            parts = line.split(" ")
            if parts[0] == "IMPORT":
                if len(parts) == 2:

                    include = Program(parts[1])
                    preproc = Preprocessor()
                    preproc.preprocess(include)

                    program.preprocessed = program.preprocessed + include.preprocessed
                    program.preprocessed.append(f"__source__ {program.sourceFile}")
                    program.preprocessed.append(f"__line__ {ix + 2}")
                    
                else:
                    raise PreprocessorError("SYNTEX ERROR", ix, program.sourceFile)
            else:
                program.preprocessed.append(line)
