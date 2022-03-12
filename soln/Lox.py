import sys

import Interpreter
import Parser
import Scanner
import Token
from TokenType import TokenType

class Lox:
    def __init__(self):
        self.interpreter = Interpreter.Interpreter()
        self.hadError = False
        self.hadRuntimeError = False


    def runFile(self, path: str) -> None:
        source = None
        try:
            with open(path, 'r') as f:
                source = f.read() # Probably not safe
        except FileNotFoundError:
            sys.exit(f"FileNotFoundError: No such file or directory: {path}")
        self.run(source)
        if self.hadError: exit(65)
        if self.hadRuntimeError: exit(70)


    def runPrompt(self) -> None:
        pass # maybe in the future


    def run(self, source: str) -> None:
        scanner = Scanner.Scanner(source)
        tokens = scanner.scanTokens()
        parser = Parser.Parser(tokens)
        statements = parser.parse()
        if self.hadError: return
        if self.hadRuntimeError: return
        self.interpreter.interpret(statements)

    def lineError(self, line: int, message: str) -> None:
        self.report(line, "", message)

    def report(self, line: int, where: str, message: str) -> None:
        print(f"[line {line}] Error{where}: {message}")
        self.hadError = True

    def tokenError(self, token: Token.Token, message: str) -> None:
        if token.type == TokenType.TokenType.EOF:
            self.report(token.line, " at end", message)
        else:
            self.report(token.line, " at '" + token.lexeme + "'" + message)

    def runtimeError(self, error: RuntimeError) -> None:
        print(f"{str(error)}\n[line {error.token.line}]")
        self.hadRuntimeError = True

