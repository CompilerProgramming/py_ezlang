import os, sys
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(base_dir)
# ^^^ Makes importing from the higher level directory possible for the purpose of including common.CompilerException

from common.compiler_exception import CompilerException
from _token import Token

class Lexer():
    def __init__(self, source: str) -> None:
        self.input = list(source)
        self.position = 0
        self.line_number = 0

    def parse_number(self) -> Token:
        assert self.input[self.position].isdigit()

        start_position = self.position
        self.position += 1
        while self.position < len(self.input) and self.input[self.position].isdigit():
            self.position += 1
        if self.input[self.position] == '.':
            self.position += 1
            while self.position < len(self.input) and self.input[self.position].isdigit():
                self.position += 1

        num_str = self.input[start_position:self.position]
        num = int(num_str) if num_str.isnumeric() else float(num_str)
        
        return Token("NUM", num, self.line_number)
    
    def is_identifier_start(self, char: str) -> bool:
        return char.isalpha() or char == '_'
    
    def is_identifier_letter(self, char: str) -> bool:
        return char.isalnum() or char == '_'
    
    def parse_identifier(self) -> Token:
        assert self.is_identifier_start(self.input[self.position])

        start_position = self.position
        self.position += 1
        while self.position < len(self.input) and self.is_identifier_letter(self.input[self.position]):
            self.position += 1

        return Token("IDENT", self.input[start_position:self.position], self.line_number)
    
    def peek_char(self) -> str:
        pos = self.position
        while pos < len(self.input[pos]) and self.input[pos].isspace():
            pos += 1

        return self.input[pos]
    
    def scan(self) -> Token:
        while (True):
            if self.position >= len(self.input): return Token("EOF", None, self.line_number)
            match self.input[self.position]:
                case 0: Token("EOF", None, self.line_number)
                case ' ' | "\t":
                    self.position += 1
                    continue
                case '\r':
                    self.position += 1
                    if self.position < len(self.input) and self.input[self.position] == '\n':
                        self.line_number += 1
                        self.position += 1
                    continue
                case '\n':
                    self.line_number += 1
                    self.position += 1
                    continue
                case '&':
                    self.position += 1
                    if self.position < len(self.input) and self.input[self.position] == '&':
                        self.position += 1
                        return Token("PUNCT", "&&", self.line_number)
                    return Token("PUNCT", "&", self.line_number)
                case '|':
                    self.position += 1
                    if self.position < len(self.input) and self.input[self.position] == "|":
                        self.position += 1
                        return Token("PUNCT", "||", self.line_number)
                    return Token("PUNCT", "|", self.line_number)
                case "=":
                    self.position += 1
                    if self.position < len(self.input) and self.input[self.position] == "=":
                        self.position += 1
                        return Token("PUNCT", "==", self.line_number)
                    return Token("PUNCT", "=", self.line_number)
                case '<':
                    self.position += 1
                    if self.position < len(self.input) and self.input[self.position] == "=":
                        self.position += 1
                        return Token("PUNCT", "<=", self.line_number)
                    return Token("PUNCT", "<", self.line_number)
                case '>':
                    self.position += 1
                    if self.position < len(self.input) and self.input[self.position] == "=":
                        self.position += 1
                        return Token("PUNCT", ">=", self.line_number)
                    return Token("PUNCT", ">", self.line_number)
                case '!':
                    self.position += 1
                    if self.position < len(self.input) and self.input[self.position] == "=":
                        self.position += 1
                        return Token("PUNCT", "!=", self.line_number)
                    return Token("PUNCT", "!", self.line_number)
                case '-':
                    self.position += 1
                    if self.position < len(self.input) and self.input[self.position] == ">":
                        self.position += 1
                        return Token("PUNCT", "->", self.line_number)
                    return Token("PUNCT", "-", self.line_number)
                case '{' | '}' | '[' | ']' | '(' | ')' | ',' | '.' | '%' | '+' | '*' | ';' | ':' | '?':
                    self.position += 1
                    return Token("PUNCT", self.input[self.position-1], self.line_number)
                case '/':
                    self.position += 1
                    if self.position < len(self.input) and self.input[self.position] == "/":
                        self.position += 1
                        while self.position < len(self.input) and self.input[self.position] != "\n": self.position += 1
                        continue
                    return Token("PUNCT", '/', self.line_number)
                case _:
                    return self.scan_others()

    def scan_others(self):
        if self.input[self.position].isdigit(): return self.parse_number()
        elif self.is_identifier_letter(self.input[self.position]): return self.parse_identifier()

        raise CompilerException(f"Unexpected character: '{self.input[self.position]}' at line {self.line_number}")