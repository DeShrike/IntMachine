class PreprocessorError(Exception):

    def __init__(self, message: str, lineNumber: int, sourceFile: str):
        super().__init__()
        self.message = message
        self.lineNumber = lineNumber
        self.sourceFile = sourceFile

    def __str__(self) -> str:
        return f"PREPROCESSOR ERROR: {self.sourceFile} Line {self.lineNumber}: {self.message}"

class AssemblerError(Exception):

    def __init__(self, message: str, lineNumber: int, sourceFile: str):
        super().__init__()
        self.message = message
        self.lineNumber = lineNumber
        self.sourceFile = sourceFile

    def __str__(self) -> str:
        return f"ASSEMBLER ERROR: {self.sourceFile} Line {self.lineNumber}: {self.message}"

class CompilerError(Exception):

    def __init__(self, message: str, lineNumber: int, sourceFile: str):
        super().__init__()
        self.message = message
        self.lineNumber = lineNumber
        self.sourceFile = sourceFile

    def __str__(self) -> str:
        return f"COMPILER ERROR: {self.sourceFile} Line {self.lineNumber}: {self.message}"

class ExcecutionError(Exception):

    def __init__(self, message: str, instructionPointer: int):
        super().__init__()
        self.message = message
        self.instructionPointer = instructionPointer

    def __str__(self) -> str:
        return f"ERROR: IP {self.instructionPointer}: {self.message}"
