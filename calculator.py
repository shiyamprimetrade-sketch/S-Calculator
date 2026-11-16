"""Offline calculator expression evaluator; no eval or external services."""
from __future__ import annotations

from decimal import Decimal, DivisionByZero, InvalidOperation, localcontext
import re


class CalculatorError(ValueError):
    """An invalid or unsupported calculator expression."""


class CalculatorZeroDivisionError(CalculatorError):
    """Division by zero is undefined."""


_TOKEN = re.compile(r"\s*(?:(\d+(?:\.\d*)?|\.\d+)|([+\-*/()%√]))")
_MAX_LENGTH = 512
_MAX_DEPTH = 64


def tokenize(expression: str) -> list[str]:
    if not expression.strip():
        raise CalculatorError("Enter an expression")
    if len(expression) > _MAX_LENGTH:
        raise CalculatorError("Expression is too long")
    tokens = []
    pos = 0
    while pos < len(expression):
        match = _TOKEN.match(expression, pos)
        if not match:
            if not expression[pos:].strip():
                break
            raise CalculatorError("Unsupported character")
        tokens.append(match.group(1) or match.group(2))
        pos = match.end()
    return tokens


class _Parser:
    def __init__(self, tokens: list[str]):
        self.tokens = tokens
        self.pos = 0
        self.depth = 0

    def peek(self) -> str | None:
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def take(self) -> str:
        token = self.peek()
        if token is None:
            raise CalculatorError("Incomplete expression")
        self.pos += 1
        return token

    def expression(self) -> Decimal:
        value = self.term()
        while self.peek() in ('+', '-'):
            op = self.take()
            right = self.term()
            value = value + right if op == '+' else value - right
        return value

    def term(self) -> Decimal:
        value = self.unary()
        while self.peek() in ('*', '/'):
            op = self.take()
            right = self.unary()
            if op == '/':
                if right == 0:
                    raise CalculatorZeroDivisionError("Cannot divide by zero")
                value /= right
            else:
                value *= right
        return value

    def unary(self) -> Decimal:
        if self.peek() in ('+', '-'):
            op = self.take()
            value = self.unary()
            return value if op == '+' else -value
        if self.peek() == '√':
            self.take()
            value = self.unary()
            if value < 0:
                raise CalculatorError("Cannot take square root of a negative number")
            return value.sqrt()
        return self.postfix()

    def postfix(self) -> Decimal:
        value = self.primary()
        while self.peek() == '%':
            self.take()
            value /= Decimal(100)
        return value

    def primary(self) -> Decimal:
        token = self.take()
        if token == '(':
            self.depth += 1
            if self.depth > _MAX_DEPTH:
                raise CalculatorError("Too many nested parentheses")
            value = self.expression()
            if self.take() != ')':
                raise CalculatorError("Missing closing parenthesis")
            self.depth -= 1
            return value
        if token[0].isdigit() or token[0] == '.':
            return Decimal(token)
        raise CalculatorError("Expected a number")


def calculate(expression: str) -> str:
    """Evaluate a bounded arithmetic expression; percent is postfix /100."""
    tokens = tokenize(expression)
    try:
        with localcontext() as context:
            context.prec = 28
            context.Emax = 999
            context.Emin = -999
            parser = _Parser(tokens)
            result = parser.expression()
            if parser.peek() is not None:
                raise CalculatorError("Unexpected input")
            if not result.is_finite():
                raise CalculatorError("Result is not finite")
            if result == 0:
                return '0'
            # Avoid displaying excessively long strings from extreme input.
            formatted = format(result.normalize(), 'f')
            if len(formatted) > 100:
                formatted = format(result.normalize(), '.12E')
            return formatted
    except CalculatorError:
        raise
    except (DivisionByZero, InvalidOperation, OverflowError, RecursionError) as exc:
        raise CalculatorError("Calculation cannot be completed") from exc
