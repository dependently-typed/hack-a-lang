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
printSum(1,2);
"""

functionReturnStatement = """
fun returnSum(a, b) {
  return a + b;
}
print returnSum(1,2);
"""

fibonacci = """
fun fibonacci(n) {
  if (n <= 1) {
    return n;
  }
  return n+fibonacci(n-1);
}
print fibonacci(1);
"""

testCases = [simpleBinaryFalse, simpleBinaryTrue, variables, forStatement, whileStatement, functionStatement, functionReturnStatement, fibonacci]

def parseInput(input: str) -> list:
    scanner = Scanner.Scanner(input)
    tokenList = scanner.scanTokens()
    parser = Parser.Parser(tokenList)
    return parser.parse()

testCases = [fibonacci] #simpleBinaryFalse, simpleBinaryTrue, variables, forStatement]

for testCase in testCases:
    statements = parseInput(testCase)
    print(statements)
    for statement in statements:
        print(statement)

