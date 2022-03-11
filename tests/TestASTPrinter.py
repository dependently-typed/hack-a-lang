import sys
sys.path.insert(0, '../lox')

import Scanner
import Parser
import Expr
import Token
from TokenType import TokenType
from ASTPrinter import AstPrinter

simpleBinaryFalse = """
if (1 != 1) {
  print "true";
} else {
  print "false";
}
"""

expression = Expr.Binary(
    Expr.Unary(
        Token.Token(TokenType.MINUS, "-", None, 1), Expr.Literal(123)),
        Token.Token(TokenType.STAR, "*", None, 1),
        Expr.Grouping(Expr.Literal(45.67)
    )
)

def parseInput(input: str) -> list:
    scanner = Scanner.Scanner(input)
    tokenList = scanner.scanTokens()
    parser = Parser.Parser(tokenList)
    return parser.parse()


# print(Token.Token(TokenType.MINUS, "-", None, 1))
print(AstPrinter().printast(expression))
statements = parseInput(simpleBinaryFalse)
for statement in statements:
    print(AstPrinter().printast(statement))