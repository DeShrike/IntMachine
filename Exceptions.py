class CompileError(Exception):

    def __init__(self, message: str, lineNumber: int):
        super().__init__()
        self.message = message
        self.lineNumber = lineNumber

    def __str__(self) -> str:
        return f"ERROR: Line {self.lineNumber}: {self.message}"


class ExcecutionError(Exception):

    def __init__(self, message: str, lineNumber: int):
        super().__init__()
        self.message = message
        self.lineNumber = lineNumber

    def __str__(self) -> str:
        return f"ERROR: Line {self.lineNumber}: {self.message}"
