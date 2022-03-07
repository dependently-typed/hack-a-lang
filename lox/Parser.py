import Expr
import Scanner
import TokenType


class Parser:

    def __init__(self, tokenList):
        self.current = 0
        self.tokenList = tokenList

    def parse(self):
        return

    def expression(self):
        return

    def declaration(self):
        return

    def classDeclaration(self):
        return

    def statement(self):
        return

    def forStatement(self):
        return

    def ifStatement(self):
        return

    def printStatement(self):
        return

    def returnStatement(self):
        return

    def varDeclaration(self):
        return

    def whileStatement(self):
        return

    def expressionStatement(self):
        return

    def function(self, kind):
        return

    def block(self):
        return

    def assignment(self):
        return

    def orOperator(self):
        return

    def andOperator(self):
        return

    def equality(self):
        expr = self.comparison()

        while self.match("BANG_EQUAL", "EQUAL_EQUAL"):
            operator = self.previous()
            right = self.comparison()
            expr = Expr.Binary(expr, operator, right)

        return expr

    def comparison(self):
        expr = self.term()

        while self.match("GREATER", "GREATER_EQUAL", "LESS", "LESS_EQUAL"):
            operator = self.previous()
            right = self.term()
            expr = Expr.Binary(expr, operator, right)

        return expr

    def term(self):
        expr = self.factor()

        while self.match("MINUS", "PLUS"):
            operator = self.previous()
            right = self.factor()
            expr = Expr.Binary(expr, operator, right)

        return expr

    def factor(self):
        expr = self.unary()

        while self.match("SLASH", "STAR"):
            operator = self.previous()
            right = self.unary()
            expr = Expr.Binary(expr, operator, right)

        return expr

    def unary(self):
        if self.match("BANG", "MINUS"):
            operator = self.previous()
            right = self.unary()
            return Expr.Unary(operator, right)
        return self.call()

    def finishCall(self, callee):
        return

    def call(self):
        return

    def primary(self):
        if self.match("FALSE"):
            return Expr.Literal(False)
        if self.match("TRUE"):
            return Expr.Literal(True)
        if self.match("NIL"):
            return Expr.Literal(None)
        if self.match("NUMBER", "STRING"):
            return Expr.Literal(self.previous.literal)

        if self.match("SUPER"):
            keyword = self.previous()
            self.consume("DOT", "Expect '.' after 'super'.")
            method = self.consume("IDENTIFIER", "Expect superclass method name.")
            return Expr.Super(keyword, method)

        if self.match("THIS"):
            return Expr.This(self.previous())

        if self.match("Identifier"):
            return Expr.Variable(self.previous())

        if self.match("LEFT_PAREN"):
            expr = self.expression()
            self.consume("RIGHT_PAREN", "Expect ')' after expression.")
            return Expr.Grouping(expr)

        raise self.error(self.peek(), "Expect expression.")

    def consume(self, tokenType, message):
        if self.check(tokenType):
            return self.advance()

        raise self.error(self.peek(), message)

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

    def error(self, token, msg):
        #Lox.error(token, msg)
        return Exception()

    def synchronise(self):
        self.advance()
        while not self.isAtEnd():
            if self.previous().type == "SEMICOLON" or ["CLASS", "FUN", "VAR", "FOR", "IF", "WHILE", "PRINT", "RETURN"].contains(self.peek().type):
                return

            self.advance()
