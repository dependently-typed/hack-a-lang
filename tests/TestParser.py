import sys
sys.path.insert(0, '../lox')

import Scanner
import Parser
import Interpreter
import Expr

simpleBinary = "1 + 2/3;"
scanner = Scanner.Scanner(simpleBinary)
tokenList = scanner.scanTokens()
parser = Parser.Parser(tokenList)
statements = parser.parse()
print(statements)
Interpreter = Interpreter.Interpreter()
for statement in statements:
    print(Interpreter.interpret(statement))


