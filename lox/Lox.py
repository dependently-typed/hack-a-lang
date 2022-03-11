import sys

# import Interpreter
import Parser
import Scanner
import Token
from TokenType import TokenType

class Lox:
    def __init__(self):
        # interpreter = Interpreter()
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
        scanner = Scanner(source)
        tokens = scanner.scanTokens()
        parser = Parser(tokens)
        statements = parser.parse()
        if self.hadError: return
        if self.hadRuntimeError: return
        # self.interpreter.interpret(statements)

    def lineError(self, line: int, message: str) -> None:
        self.report(line, "", message)

    def report(self, line: int, where: str, message: str) -> None:
        print(f"[line {line}] Error{where}: {message}")
        self.hadError = True

    def tokenError(self, token: Token.Token, message: str) -> None:
        if token.type == TokenType.TokenType.EOF:
            report(token.line, " at end", message)
        else:
            report(token.line, " at '" + token.lexeme + "'" + message)

    def runtimeError(self, error: RuntimeError) -> None:
        print(f"{str(e)}\n[line {error.token.line}]")
        self.hadRuntimeError = True


if __name__ == "__main__":
    if len(sys.argv) == 2:
        Lox().runFile(sys.argv[1])
    else:
        sys.exit("Usage: python -m Lox <filename>")