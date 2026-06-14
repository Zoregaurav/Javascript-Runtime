from __future__ import annotations

import sys
from pathlib import Path

from interpreter import Interpreter
from lexer import Lexer
from parser import Parser


def execute(source: str) -> None:
    tokens = Lexer(source).tokenize()
    program = Parser(tokens).parse()
    Interpreter().run(program)


def main(argv: list[str] | None = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    if len(argv) != 1:
        print("Usage: python main.py <file.js>", file=sys.stderr)
        return 2
    path = Path(argv[0])
    try:
        execute(path.read_text(encoding="utf-8"))
        return 0
    except Exception as exc:
        print(f"Runtime error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
