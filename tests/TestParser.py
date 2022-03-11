import sys
sys.path.insert(0, '../lox')

import Scanner
import Parser
import Interpreter
import Expr

simpleBinary = "\"123\" == 123;"
scanner = Scanner.Scanner(simpleBinary)
tokenList = scanner.scanTokens()
for i in tokenList:
    print(i)
parser = Parser.Parser(tokenList)
statements = parser.parse()
# print(statements)
Interpreter = Interpreter.Interpreter()
for statement in statements:
    print(Interpreter.interpret(statement))


