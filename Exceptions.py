class AssemblerError(Exception):

    def __init__(self, message: str, lineNumber: int):
        super().__init__()
        self.message = message
        self.lineNumber = lineNumber

    def __str__(self) -> str:
        return f"ASSEMBLER ERROR: Line {self.lineNumber}: {self.message}"

class CompilerError(Exception):

    def __init__(self, message: str, lineNumber: int):
        super().__init__()
        self.message = message
        self.lineNumber = lineNumber

    def __str__(self) -> str:
        return f"COMPILER ERROR: Line {self.lineNumber}: {self.message}"


class ExcecutionError(Exception):

    def __init__(self, message: str, lineNumber: int):
        super().__init__()
        self.message = message
        self.lineNumber = lineNumber

    def __str__(self) -> str:
        return f"ERROR: Line {self.lineNumber}: {self.message}"
