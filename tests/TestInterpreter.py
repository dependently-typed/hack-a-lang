import sys
sys.path.insert(0, '../lox')

import Scanner
import Parser
import Interpreter
import Expr
from Stmt import Stmt
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
for (var a = 1; a < 10; a = a + 1) {
  print a;
}
"""

whileStatement = """
var a = 1;
while (a < 10) {
  print a;
  a = a + 1;
}
"""

functionStatement = """
fun printSum(a, b) {
  print a + b;
}
printSum(2,5);
"""

functionReturnStatement = """
fun returnSum(a, b) {
  return a + b;
}
print returnSum(1,3);
"""

fibonacci = """
fun fibonacci(n) {
  if (n <= 0) {
    return 0;
  }
  if (n == 1) {
    return 1;
  }
  return fibonacci(n-1) + fibonacci(n-2);
}
print fibonacci(20);
"""

testCases = [simpleBinaryFalse, simpleBinaryTrue, variables, forStatement, whileStatement, functionStatement, functionReturnStatement, fibonacci]
# testCases = [fibonacci]


def interpretInput(input: str):
    scanner = Scanner.Scanner(input)
    tokenList = scanner.scanTokens()
    parser = Parser.Parser(tokenList)
    statements = parser.parse()
    # print(statements)
    interpreter = Interpreter.Interpreter()
    value = interpreter.interpret(statements)


for testCase in testCases:
    value = interpretInput(testCase)
    print(value) # print None if no return value
