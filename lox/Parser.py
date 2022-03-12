import Expr
import Scanner
import Expr
import Stmt
import Lox
from TokenType import TokenType


class Parser:
    def __init__(self, tokenList):
        self.current = 0
        self.tokenList = tokenList

    def parse(self) -> list:
        statements = []
        while not self.isAtEnd():
            statements.append(self.declaration())
        return statements

    def expression(self):
        return self.assignment()

    def declaration(self): # return statement
        try:
            if self.match(TokenType.CLASS): return self.classDeclaration()
            if self.match(TokenType.FUN): return self.function("function")
            if self.match(TokenType.VAR): return self.varDeclaration()
            return self.statement()
        except Exception: # create ParseError?
            self.synchronise()
            return None

    # def classDeclaration(self):
    #     name = self.consume(TokenType.IDENTIFIER, "Expect class name.")
    #     superclass = None
    #     if self.match(TokenType.LESS):
    #         self.consume(TokenType.IDENTIFIER, "Expect class name.")
    #         superclass = Expr.Variable(self.previous())
    #     self.consume(TokenType.LEFT_BRACE, "Expect '{' before class body.")
    #     methods = []
    #     while not self.check(TokenType.RIGHT_BRACE) and not self.isAtEnd():
    #         methods.append(self.function("method"))
    #     self.consume(TokenType.RIGHT_BRACE, "Expect '}' after class body.")
    #     return name, superclass, methods # as statement Class

    def statement(self):
        if self.match(TokenType.FOR):
            return self.forStatement()
        if self.match(TokenType.IF):
            return self.ifStatement()
        if self.match(TokenType.PRINT):
            return self. printStatement()
        if self.match(TokenType.RETURN):
            return self.returnStatement()
        if self.match(TokenType.WHILE):
            return self.whileStatement()
        if self.match(TokenType.LEFT_BRACE):
            temp = self.block()
            return Stmt.Block(temp)
        expr = self.expressionStatement()
        return expr

    def forStatement(self):
        self.consume(TokenType.LEFT_PAREN, "Expect '(' after 'for'.")
        initializer = None
        if self.match(TokenType.SEMICOLON): initializer = None
        elif self.match(TokenType.VAR): initializer = self.varDeclaration()
        else: initializer = self.expressionStatement()

        condition = None
        if not self.check(TokenType.SEMICOLON):
            condition = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after loop condition.")
        increment = None
        if not self.check(TokenType.RIGHT_PAREN):
            increment = self.expression()
        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after for clauses.")

        body = self.statement()
        if increment is not None:
           body = Stmt.Block([body, Stmt.Expression(increment)])

        if condition is None:
            condition = Expr.Literal(True)
        body = Stmt.While(condition, body)

        if initializer is not None:
            body = Stmt.Block([initializer, body])

        return body

    def ifStatement(self):
        self.consume(TokenType.LEFT_PAREN, "Expect '(' after 'if'.")
        condition = self.expression()
        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after if condition.")
        thenBranch = self.statement()
        elseBranch = None
        if self.match(TokenType.ELSE):
            elseBranch = self.statement()
        return Stmt.If(condition, thenBranch, elseBranch)

    def printStatement(self):
        value = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after value.")
        return Stmt.Print(value)

    def returnStatement(self):
        keyword = self.previous()
        value = None
        if not self.check(TokenType.SEMICOLON):
            value = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after return value.")
        return Stmt.Return(keyword, value)

    def varDeclaration(self):
        name = self.consume(TokenType.IDENTIFIER, "Expect variable name.")
        initializer = None
        if self.match(TokenType.EQUAL):
            initializer = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after variable declaration.")
        return Stmt.Var(name, initializer)

    def whileStatement(self):
        self.consume(TokenType.LEFT_PAREN, "Expect '(' after 'while'.")
        condition = self.expression()
        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after condition.")
        body = self.statement()
        return Stmt.While(condition, body)

    def expressionStatement(self):
        expr = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after expression.")
        statement = Stmt.Expression(expr)
        return statement

    def function(self, kind):
        name = self.consume(TokenType.IDENTIFIER, "Expect " + kind + " name.")
        self.consume(TokenType.LEFT_PAREN, "Expect '(' after " + kind + " name.")
        parameters = []
        if not self.check(TokenType.RIGHT_PAREN):
            start = True
            while start or self.match(TokenType.COMMA):
                start = False
                if len(parameters) >= 255:
                    self.error(self.peek(), "Can't have more than 255 parameters")
                parameters.append(self.consume(TokenType.IDENTIFIER, "Expect parameter name."))
        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after parameters.")
        self.consume(TokenType.LEFT_BRACE, "Expect '{' before " + kind + " body.")
        body = self.block()
        return Stmt.Function(name, parameters, body)

    def block(self):
        statements = []
        while (not self.check(TokenType.RIGHT_BRACE) and not self.isAtEnd()):
            statements.append(self.declaration())
        self.consume(TokenType.RIGHT_BRACE, "Expect '}' after block.")
        return statements

    def assignment(self):
        expr = self.orOperator()
        if self.match(TokenType.EQUAL):
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
        while self.match(TokenType.OR):
            operator = self.previous()
            right = self.andOperator()
            expr = Expr.Logical(expr, operator, right)
        return expr

    def andOperator(self):
        expr = self.equality()
        while self.match(TokenType.AND):
            operator = self.previous()
            right = self.equality()
            expr = Expr.Logical(expr, operator, right)
        return expr

    def equality(self):
        expr = self.comparison()
        while self.match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
            operator = self.previous()
            right = self.comparison()
            expr = Expr.Binary(expr, operator, right)

        return expr

    def comparison(self):
        expr = self.term()
        while self.match(TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL):
            operator = self.previous()
            right = self.term()
            expr = Expr.Binary(expr, operator, right)

        return expr

    def term(self):
        expr = self.factor()

        while self.match(TokenType.MINUS, TokenType.PLUS):
            operator = self.previous()
            right = self.factor()
            expr = Expr.Binary(expr, operator, right)
        return expr

    def factor(self):
        expr = self.unary()

        while self.match(TokenType.SLASH, TokenType.STAR):
            operator = self.previous()
            right = self.unary()
            expr = Expr.Binary(expr, operator, right)

        return expr

    def unary(self):
        if self.match(TokenType.BANG, TokenType.MINUS):
            operator = self.previous()
            right = self.unary()
            return Expr.Unary(operator, right)
        return self.call()

    def finishCall(self, callee):
        arguments = []
        if not self.check(TokenType.RIGHT_PAREN):
            while True:
                if len(arguments) >= 255:
                    self.error(self.peek(), "Can't have more than 255 arguments.")
                arguments.append(self.expression())
                if not self.match(TokenType.COMMA):
                    break
        paren = self.consume(TokenType.RIGHT_PAREN, "Expect ')' after arguments.")
        return Expr.Call(callee, paren, arguments)

    def call(self):
        expr = self.primary()
        while True:
            if self.match(TokenType.LEFT_PAREN):
                expr = self.finishCall(expr)
            elif self.match(TokenType.DOT):
                name = self.consume(TokenType.IDENTIFIER, "Expect property name after '.'.")
                expr = Expr.Get(expr, name)
            else:
                break
        return expr

    def primary(self):
        if self.match(TokenType.FALSE):
            return Expr.Literal(False)
        if self.match(TokenType.TRUE):
            return Expr.Literal(True)
        if self.match(TokenType.NIL):
            return Expr.Literal(None)
        if self.match(TokenType.NUMBER, TokenType.STRING):
            return Expr.Literal(self.previous().literal)

        if self.match(TokenType.SUPER):
            keyword = self.previous()
            self.consume(TokenType.DOT, "Expect '.' after 'super'.")
            method = self.consume(TokenType.IDENTIFIER, "Expect superclass method name.")
            return Expr.Super(keyword, method)

        if self.match(TokenType.THIS):
            return Expr.This(self.previous())

        if self.match(TokenType.IDENTIFIER):
            return Expr.Variable(self.previous())

        if self.match(TokenType.LEFT_PAREN):
            expr = self.expression()
            self.consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
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
        return self.peek().type == tokenType

    def isAtEnd(self):
        return self.peek().type == TokenType.EOF

    def peek(self):
        return self.tokenList[self.current]

    def previous(self):
        return self.tokenList[self.current - 1]

    def error(self, token, msg):
        Lox.tokenError(token, msg)
        return Exception()

    def synchronise(self):
        self.advance()
        types = [
            TokenType.CLASS,
            TokenType.FUN,
            TokenType.VAR,
            TokenType.FOR,
            TokenType.IF,
            TokenType.WHILE,
            TokenType.PRINT,
            TokenType.RETURN]

        while not self.isAtEnd():
            if self.previous().type == TokenType.SEMICOLON or self.peek().type in types:
                return

            self.advance()
