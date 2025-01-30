#This file is called _token because of the python main library module 'token' interfering with the import functionality.

TOKEN_KINDS = [
    "IDENT",
    "NUM",
    "PUNCT",
    "EOZ"
]

class Token():
    def __init__(self, kind: str, value: str | int | float, line_number: int) -> None:
        self.kind = kind
        self.value = value
        self.line_number = line_number

        if kind not in TOKEN_KINDS:
            raise ValueError(f"Invalid token kind: '{self.kind}'")
        
    def __str__(self) -> str:
        return self.value.__str__()