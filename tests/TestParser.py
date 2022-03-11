import sys
sys.path.insert(0, '../lox')

import Scanner
import Parser
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

forStatment = """
for (var a = 1; a < 10; a = a + 1) {
  print a;
}
"""

def parseInput(input: str) -> list:
    scanner = Scanner.Scanner(input)
    tokenList = scanner.scanTokens()
    parser = Parser.Parser(tokenList)
    return parser.parse()

testCases = [simpleBinaryFalse, simpleBinaryTrue, variables, forStatement]
for testCase in testCases:
    statements = parseInput(testCase)
    for statement in statements:
        print(statement)

