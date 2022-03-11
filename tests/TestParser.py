import sys
sys.path.insert(0, '../lox')

import Scanner
import Parser
import Interpreter
import Expr

simpleBinary = "1 + 2;"

# print(isinstance(Expr.Binary, Expr))
scanner = Scanner.Scanner(simpleBinary)
tokenList = scanner.scanTokens()
parser = Parser.Parser(tokenList)
statements = parser.parse()
for statement in statements:
    print(statement)

