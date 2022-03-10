import Expr
import Scanner
import TokenType
import Expr
import Stmt

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

    def unary(self):
        if self.match(TokenType.TokenType.BANG, TokenType.TokenType.MINUS):
            operator = self.previous()
            right = self.unary()
            return Expr.Unary(operator, right)
        return self.primary()

    def primary(self):
        if self.match(TokenType.TokenType.FALSE):
            return Expr.Literal(False)
        elif self.match(TokenType.TokenType.TRUE):
            return Expr.Literal(True)
        elif self.match(TokenType.TokenType.NIL):
            return Expr.Literal(None)
        elif self.match(TokenType.TokenType.NUMBER, TokenType.TokenType.STRING):
            return Expr.Literal(self.previous().literal)
        elif self.match(TokenType.TokenType.LEFT_PAREN):
            pass
            #to implement

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







