from __future__ import annotations

from typing import Any

from ast_nodes import (
    ArrayExpression,
    ArrowFunctionExpression,
    AssignmentExpression,
    BinaryExpression,
    BlockStatement,
    BreakStatement,
    CallExpression,
    ConditionalExpression,
    ContinueStatement,
    ExpressionStatement,
    ForStatement,
    FunctionDeclaration,
    FunctionExpression,
    Identifier,
    IfStatement,
    Literal,
    LogicalExpression,
    MemberExpression,
    NewExpression,
    ObjectExpression,
    ObjectProperty,
    Program,
    ReturnStatement,
    SpreadElement,
    UnaryExpression,
    UpdateExpression,
    VariableDeclaration,
    VariableDeclarator,
    WhileStatement,
)
from lexer import Token


class ParserError(SyntaxError):
    pass


class Parser:
    PRECEDENCE = {
        "=": 1,
        "+=": 1,
        "-=": 1,
        "*=": 1,
        "/=": 1,
        "%=": 1,
        "||": 2,
        "&&": 3,
        "==": 4,
        "===": 4,
        "!=": 4,
        "!==": 4,
        "<": 5,
        ">": 5,
        "<=": 5,
        ">=": 5,
        "+": 6,
        "-": 6,
        "*": 7,
        "/": 7,
        "%": 7,
        "**": 8,
    }

    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.index = 0

    def parse(self) -> Program:
        body = []
        while not self._check("EOF"):
            body.append(self._statement())
        return Program(body)

    def _statement(self) -> Any:
        if self._match_value(";"):
            return ExpressionStatement(Literal(None))
        if self._match_keyword("let", "const", "var"):
            return self._variable_declaration(self._previous().value, consume_semicolon=True)
        if self._match_keyword("function"):
            return self._function_declaration()
        if self._match_keyword("return"):
            argument = None if self._check_value(";") or self._check_value("}") else self._expression()
            self._optional_semicolon()
            return ReturnStatement(argument)
        if self._match_keyword("if"):
            return self._if_statement()
        if self._match_keyword("while"):
            return self._while_statement()
        if self._match_keyword("for"):
            return self._for_statement()
        if self._match_keyword("break"):
            self._optional_semicolon()
            return BreakStatement()
        if self._match_keyword("continue"):
            self._optional_semicolon()
            return ContinueStatement()
        if self._match_value("{"):
            return self._block_after_open()
        expression = self._expression()
        self._optional_semicolon()
        return ExpressionStatement(expression)

    def _variable_declaration(self, kind: str, consume_semicolon: bool) -> VariableDeclaration:
        declarations = []
        while True:
            name = self._consume("IDENTIFIER", "Expected variable name")
            initializer = self._expression() if self._match_value("=") else None
            declarations.append(VariableDeclarator(Identifier(name.value), initializer))
            if not self._match_value(","):
                break
        if consume_semicolon:
            self._optional_semicolon()
        return VariableDeclaration(kind, declarations)

    def _function_declaration(self) -> FunctionDeclaration:
        name = Identifier(self._consume("IDENTIFIER", "Expected function name").value)
        params, body = self._function_tail()
        return FunctionDeclaration(name, params, body)

    def _function_expression(self) -> FunctionExpression:
        name = Identifier(self._advance().value) if self._check("IDENTIFIER") else None
        params, body = self._function_tail()
        return FunctionExpression(params, body, name)

    def _function_tail(self) -> tuple[list[Identifier], BlockStatement]:
        self._consume_value("(", "Expected '('")
        params = self._parameters()
        self._consume_value("{", "Expected function body")
        return params, self._block_after_open()

    def _parameters(self) -> list[Identifier]:
        params = []
        if not self._check_value(")"):
            while True:
                params.append(Identifier(self._consume("IDENTIFIER", "Expected parameter").value))
                if not self._match_value(","):
                    break
        self._consume_value(")", "Expected ')'")
        return params

    def _if_statement(self) -> IfStatement:
        self._consume_value("(", "Expected '(' after if")
        test = self._expression()
        self._consume_value(")", "Expected ')' after condition")
        consequent = self._statement()
        alternate = self._statement() if self._match_keyword("else") else None
        return IfStatement(test, consequent, alternate)

    def _while_statement(self) -> WhileStatement:
        self._consume_value("(", "Expected '(' after while")
        test = self._expression()
        self._consume_value(")", "Expected ')' after condition")
        return WhileStatement(test, self._statement())

    def _for_statement(self) -> ForStatement:
        self._consume_value("(", "Expected '(' after for")
        if self._match_value(";"):
            init = None
        elif self._match_keyword("let", "const", "var"):
            init = self._variable_declaration(self._previous().value, consume_semicolon=False)
            self._consume_value(";", "Expected ';' after for initializer")
        else:
            init = self._expression()
            self._consume_value(";", "Expected ';' after for initializer")
        test = None if self._check_value(";") else self._expression()
        self._consume_value(";", "Expected ';' after for condition")
        update = None if self._check_value(")") else self._expression()
        self._consume_value(")", "Expected ')' after for clauses")
        return ForStatement(init, test, update, self._statement())

    def _block_after_open(self) -> BlockStatement:
        body = []
        while not self._check_value("}") and not self._check("EOF"):
            body.append(self._statement())
        self._consume_value("}", "Expected '}'")
        return BlockStatement(body)

    def _expression(self, min_precedence: int = 1) -> Any:
        left = self._unary()
        while True:
            token = self._peek()
            op = token.value
            if op not in self.PRECEDENCE or self.PRECEDENCE[op] < min_precedence:
                break
            precedence = self.PRECEDENCE[op]
            self._advance()
            if op in ("=", "+=", "-=", "*=", "/=", "%="):
                right = self._expression(precedence)
                left = AssignmentExpression(left, op, right)
            else:
                next_min = precedence if op == "**" else precedence + 1
                right = self._expression(next_min)
                cls = LogicalExpression if op in ("&&", "||") else BinaryExpression
                left = cls(left, op, right)
        if min_precedence <= 1 and self._match_value("?"):
            consequent = self._expression()
            self._consume_value(":", "Expected ':' in conditional expression")
            alternate = self._expression()
            left = ConditionalExpression(left, consequent, alternate)
        return left

    def _unary(self) -> Any:
        if self._match_value("!", "-", "+", "++", "--"):
            op = self._previous().value
            argument = self._unary()
            return UpdateExpression(op, argument, True) if op in ("++", "--") else UnaryExpression(op, argument)
        return self._postfix()

    def _postfix(self) -> Any:
        expr = self._primary()
        while True:
            if self._match_value("("):
                expr = CallExpression(expr, self._arguments())
            elif self._match_value("."):
                expr = MemberExpression(expr, Identifier(self._consume("IDENTIFIER", "Expected property").value), False)
            elif self._match_value("["):
                prop = self._expression()
                self._consume_value("]", "Expected ']'")
                expr = MemberExpression(expr, prop, True)
            elif self._match_value("++", "--"):
                expr = UpdateExpression(self._previous().value, expr, False)
            else:
                break
        return expr

    def _primary(self) -> Any:
        if self._match("NUMBER", "STRING"):
            return Literal(self._previous().value)
        if self._match_keyword("true"):
            return Literal(True)
        if self._match_keyword("false"):
            return Literal(False)
        if self._match_keyword("null"):
            return Literal(None)
        if self._match_keyword("function"):
            return self._function_expression()
        if self._match_keyword("new"):
            callee = self._postfix()
            if isinstance(callee, CallExpression):
                return NewExpression(callee.callee, callee.arguments)
            return NewExpression(callee, [])
        if self._match("IDENTIFIER"):
            ident = Identifier(self._previous().value)
            if self._match_value("=>"):
                return self._arrow([ident])
            return ident
        if self._match_value("("):
            if self._looks_like_arrow_params():
                params = self._parameters()
                self._consume_value("=>", "Expected '=>'")
                return self._arrow(params)
            expr = self._expression()
            self._consume_value(")", "Expected ')'")
            return expr
        if self._match_value("["):
            return self._array()
        if self._match_value("{"):
            return self._object()
        raise self._error(self._peek(), "Expected expression")

    def _arrow(self, params: list[Identifier]) -> ArrowFunctionExpression:
        if self._match_value("{"):
            body = self._block_after_open()
        else:
            body = self._expression()
        return ArrowFunctionExpression(params, body)

    def _looks_like_arrow_params(self) -> bool:
        depth = 1
        pos = self.index
        while pos < len(self.tokens):
            value = self.tokens[pos].value
            if value == "(":
                depth += 1
            elif value == ")":
                depth -= 1
                if depth == 0:
                    return pos + 1 < len(self.tokens) and self.tokens[pos + 1].value == "=>"
            pos += 1
        return False

    def _arguments(self) -> list[Any]:
        args = []
        if not self._check_value(")"):
            while True:
                if self._match_value("..."):
                    args.append(SpreadElement(self._expression()))
                else:
                    args.append(self._expression())
                if not self._match_value(","):
                    break
        self._consume_value(")", "Expected ')'")
        return args

    def _array(self) -> ArrayExpression:
        elements = []
        if not self._check_value("]"):
            while True:
                if self._match_value("..."):
                    elements.append(SpreadElement(self._expression()))
                else:
                    elements.append(self._expression())
                if not self._match_value(","):
                    break
        self._consume_value("]", "Expected ']'")
        return ArrayExpression(elements)

    def _object(self) -> ObjectExpression:
        properties = []
        if not self._check_value("}"):
            while True:
                if self._match_value("..."):
                    properties.append(SpreadElement(self._expression()))
                else:
                    if self._match("IDENTIFIER", "STRING", "NUMBER"):
                        raw_key = self._previous().value
                        key = str(raw_key)
                    else:
                        raise self._error(self._peek(), "Expected object key")
                    value = Identifier(key)
                    if self._match_value(":"):
                        value = self._expression()
                    properties.append(ObjectProperty(key, value))
                if not self._match_value(","):
                    break
        self._consume_value("}", "Expected '}'")
        return ObjectExpression(properties)

    def _optional_semicolon(self) -> None:
        self._match_value(";")

    def _match(self, *types: str) -> bool:
        if self._peek().type in types:
            self._advance()
            return True
        return False

    def _match_keyword(self, *values: str) -> bool:
        if self._peek().type == "KEYWORD" and self._peek().value in values:
            self._advance()
            return True
        return False

    def _match_value(self, *values: str) -> bool:
        if self._peek().type in ("OPERATOR", "PUNCTUATION") and self._peek().value in values:
            self._advance()
            return True
        return False

    def _consume(self, token_type: str, message: str) -> Token:
        if self._peek().type == token_type:
            return self._advance()
        raise self._error(self._peek(), message)

    def _consume_value(self, value: str, message: str) -> Token:
        if self._peek().value == value:
            return self._advance()
        raise self._error(self._peek(), message)

    def _check(self, token_type: str) -> bool:
        return self._peek().type == token_type

    def _check_value(self, value: str) -> bool:
        return self._peek().type in ("OPERATOR", "PUNCTUATION") and self._peek().value == value

    def _advance(self) -> Token:
        token = self.tokens[self.index]
        self.index += 1
        return token

    def _peek(self) -> Token:
        return self.tokens[self.index]

    def _previous(self) -> Token:
        return self.tokens[self.index - 1]

    @staticmethod
    def _error(token: Token, message: str) -> ParserError:
        return ParserError(f"{message} at {token.line}:{token.column}")
