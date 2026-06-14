from __future__ import annotations

from dataclasses import dataclass
from typing import Any


KEYWORDS = {
    "let",
    "const",
    "var",
    "if",
    "else",
    "while",
    "for",
    "function",
    "return",
    "true",
    "false",
    "null",
    "new",
    "break",
    "continue",
}


@dataclass(frozen=True)
class Token:
    type: str
    value: Any
    line: int
    column: int

    def is_value(self, value: str) -> bool:
        return self.value == value


class LexerError(SyntaxError):
    pass


class Lexer:
    MULTI_CHAR_OPERATORS = (
        "...",
        "===",
        "!==",
        "=>",
        "**",
        "==",
        "!=",
        "<=",
        ">=",
        "&&",
        "||",
        "++",
        "--",
        "+=",
        "-=",
        "*=",
        "/=",
        "%=",
    )
    SINGLE_CHAR = set("+-*/%=<>!;,.?:(){}[]")

    def __init__(self, source: str):
        self.source = source
        self.index = 0
        self.line = 1
        self.column = 1

    def tokenize(self) -> list[Token]:
        tokens: list[Token] = []
        while not self._at_end():
            char = self._peek()
            if char in " \t\r":
                self._advance()
            elif char == "\n":
                self._advance_line()
            elif char == "/" and self._peek(1) == "/":
                self._skip_line_comment()
            elif char == "/" and self._peek(1) == "*":
                self._skip_block_comment()
            elif char.isdigit():
                tokens.append(self._number())
            elif char in ("'", '"'):
                tokens.append(self._string(char))
            elif self._is_identifier_start(char):
                tokens.append(self._identifier())
            else:
                tokens.append(self._operator_or_punctuation())
        tokens.append(Token("EOF", "EOF", self.line, self.column))
        return tokens

    def _number(self) -> Token:
        line, column = self.line, self.column
        start = self.index
        while self._peek().isdigit():
            self._advance()
        if self._peek() == "." and self._peek(1).isdigit():
            self._advance()
            while self._peek().isdigit():
                self._advance()
        text = self.source[start:self.index]
        value: int | float = float(text) if "." in text else int(text)
        return Token("NUMBER", value, line, column)

    def _string(self, quote: str) -> Token:
        line, column = self.line, self.column
        self._advance()
        chars: list[str] = []
        escapes = {"n": "\n", "t": "\t", "r": "\r", "\\": "\\", '"': '"', "'": "'"}
        while not self._at_end() and self._peek() != quote:
            if self._peek() == "\\":
                self._advance()
                escaped = self._peek()
                chars.append(escapes.get(escaped, escaped))
                self._advance()
            else:
                chars.append(self._peek())
                if self._peek() == "\n":
                    self._advance_line()
                else:
                    self._advance()
        if self._at_end():
            raise LexerError(f"Unterminated string at {line}:{column}")
        self._advance()
        return Token("STRING", "".join(chars), line, column)

    def _identifier(self) -> Token:
        line, column = self.line, self.column
        start = self.index
        while self._is_identifier_part(self._peek()):
            self._advance()
        text = self.source[start:self.index]
        return Token("KEYWORD" if text in KEYWORDS else "IDENTIFIER", text, line, column)

    def _operator_or_punctuation(self) -> Token:
        line, column = self.line, self.column
        for op in self.MULTI_CHAR_OPERATORS:
            if self.source.startswith(op, self.index):
                self._advance_many(len(op))
                return Token("OPERATOR" if op not in ("=>", "...") else "PUNCTUATION", op, line, column)
        char = self._peek()
        if char not in self.SINGLE_CHAR:
            raise LexerError(f"Unexpected character {char!r} at {line}:{column}")
        self._advance()
        token_type = "PUNCTUATION" if char in ";,.:(){}[]" else "OPERATOR"
        return Token(token_type, char, line, column)

    def _skip_line_comment(self) -> None:
        while not self._at_end() and self._peek() != "\n":
            self._advance()

    def _skip_block_comment(self) -> None:
        self._advance_many(2)
        while not self._at_end():
            if self._peek() == "*" and self._peek(1) == "/":
                self._advance_many(2)
                return
            if self._peek() == "\n":
                self._advance_line()
            else:
                self._advance()
        raise LexerError("Unterminated block comment")

    def _peek(self, offset: int = 0) -> str:
        pos = self.index + offset
        return "\0" if pos >= len(self.source) else self.source[pos]

    def _advance(self) -> str:
        char = self.source[self.index]
        self.index += 1
        self.column += 1
        return char

    def _advance_many(self, count: int) -> None:
        for _ in range(count):
            self._advance()

    def _advance_line(self) -> None:
        self.index += 1
        self.line += 1
        self.column = 1

    def _at_end(self) -> bool:
        return self.index >= len(self.source)

    @staticmethod
    def _is_identifier_start(char: str) -> bool:
        return char.isalpha() or char in "_$"

    @staticmethod
    def _is_identifier_part(char: str) -> bool:
        return char.isalnum() or char in "_$"
