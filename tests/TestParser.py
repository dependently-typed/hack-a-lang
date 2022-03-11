import sys
sys.path.insert(0, '../lox')

import Scanner
import Parser
import Interpreter
import Expr

simpleBinary = """
for (var a = 1; a < 10; a=a + 1) {
  print a;
}
"""
scanner = Scanner.Scanner(simpleBinary)
tokenList = scanner.scanTokens()
# for i in tokenList:
#     print(i)
parser = Parser.Parser(tokenList)
statements = parser.parse()
Interpreter = Interpreter.Interpreter()
Interpreter.interpret(statements)


