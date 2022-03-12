import sys
sys.path.insert(0, '../lox')

import Scanner
import Parser
import Interpreter
import Expr

simpleBinaryFalse = """
if (1 != 1) {
  print "true";
} else {
  print "false";
}
"""

simpleBinaryTrue = """
if (1 == 1) {
  print "true";
} else {
  print "false";
}
"""

variables = """
var variable1 = 2;
var variable2 = 1 + 2;
var variable3 = variable1 + variable2;
print variable1;
print variable2;
print variable3;
"""

forStatement = """
for (var a = 10; a < 10; a = a + 1) {
  print a;
}
"""

testCases = [forStatement] #, simpleBinaryFalse, simpleBinaryTrue, variables]

def interpretInput(input: str):
    scanner = Scanner.Scanner(input)
    tokenList = scanner.scanTokens()
    parser = Parser.Parser(tokenList)
    statements = parser.parse()
    interpreter = Interpreter.Interpreter()
    value = interpreter.interpret(statements)

for testCase in testCases:
    value = interpretInput(testCase)
    print(value) # print None if no return value
