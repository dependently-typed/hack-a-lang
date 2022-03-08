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
        name = self.consume("IDENTIFIER", "Expect " + kind + " name.")
        self.consume("LEFT_PAREN", "Expect '(' after " + kind + " name.")
        parameters = []
        if not self.check("RIGHT_PAREN"):
            start = True
            while start or self.match("COMMA"):
                start = False
                if len(parameters) >= 255:
                    self.error(self.peek(), "Can't have more than 255 parameters")
                parameters.append(self.consume("IDENTIFIER", "Expect parameter name."))
        self.consume("RIGHT_PAREN", "Expect ')' after parameters.")
        self.consume("LEFT_BRACE", "Expect '{' before " + kind + " body.")
        body = self.block()
        #return Stmt.Function

    def block(self):
        statements = []

        while (not self.check("RIGHT_BRACE") and not self.isAtEnd()):
            statements.append(self.declaration())
        self.consume("RIGHT_BRACE", "Expect '}' after block.")
        return statements

    def assignment(self):
        expr = self.orOperator()
        if self.match("EQUAL"):
            equals = self.previous()
            value = self.assignment()
            if isinstance(expr, Expr.Variable):
                name = expr.name
                return Expr.Assign(name, value)
            if isinstance(expr, Expr.Get):
                return Expr.Set(expr.object, expr.name, value)
            self.error(equals, "Invalid assignment target.")
        return expr

    def orOperator(self):
        expr = self.andOperator()
        while self.match("OR"):
            operator = self.previous()
            right = self.andOperator()
            expr = Expr.Logical(expr, operator, right)
        return expr

    def andOperator(self):
        expr = self.equality()
        while self.match("AND"):
            operator = self.previous()
            right = self.equality()
            expr = Expr.Logical(expr, operator, right)
        return expr

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
