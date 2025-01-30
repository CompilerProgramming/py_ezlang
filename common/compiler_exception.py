class CompilerException(Exception):
    def __init__(self, message: str, cause: Exception = None) -> None:
        super().__init__(message)
        self.cause = cause

    def __str__(self):
        if self.cause:
            return f"{super().__str__()} (Caused by: {repr(self.cause)})"
        return super().__str__()