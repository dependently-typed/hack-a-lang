import sys
sys.path.insert(0, '../lox')

import Scanner
import Parser
import Interpreter
import Expr

simpleBinary = """
if (1 != 1) {
  1 == 1;
} else {
  1 == 2;
}
"""
scanner = Scanner.Scanner(simpleBinary)
tokenList = scanner.scanTokens()
# for i in tokenList:
#     print(i)
parser = Parser.Parser(tokenList)
statements = parser.parse()
Interpreter = Interpreter.Interpreter()
print(Interpreter.interpret(statements))


