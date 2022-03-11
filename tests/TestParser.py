import sys
sys.path.insert(0, '../lox')

import Scanner
import Parser

simpleBinary = "1 + 2;"



scanner = Scanner.Scanner(input)
tokenList = scanner.scanTokens()
parser = Parser.Parser(tokenList)
statements = parser.parse()
for statement in statements:
    print(statement)

