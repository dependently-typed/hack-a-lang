import Expr
import Scanner
import TokenType

class Parser:

    def __init__(self, tokenList):
        self.tokenList = tokenList

    def advance(self):
        if not self.isAtEnd():
              self.current += 1
        return self.previous()

    def match(self, *tokenTypes):
        for token in tokenTypes:
              if self.check(token):
                    self.advance()
                    return True
        return False

    def check(self, tokenType):
        if self.isAtEnd():
              return False
        return self.peek()._type == tokenType

    def isAtEnd(self):
        return self.peek()._type == TokenType.EOF

    def peek(self):
        return self.tokenList[self.current]

    def previous(self):
        return self.tokenList[self.current - 1]







