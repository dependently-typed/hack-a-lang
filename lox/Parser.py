import Expr
import Stmt
import Lox
from TokenType import TokenType

from typing import List

class Parser:
    def __init__(self, tokenList):
        self.current = 0
        self.tokenList = tokenList

    def parse(self) -> List[Stmt.Stmt]:
        statements = []
        while not self.isAtEnd():
            statements.append(self.declaration())
        return statements

    def expression(self):
        return self.assignment()

    def declaration(self) -> Stmt.Stmt:
        try:
            if self.match(TokenType.CLASS): return self.classDeclaration()
            if self.match(TokenType.FUN): return self.function("function")
            if self.match(TokenType.VAR): return self.varDeclaration()
            return self.statement()
        except Exception:
            self.synchronize()
            return None

    def classDeclaration(self):
        name = self.consume(TokenType.IDENTIFIER, "Expect class name.")
        superclass = None
        if self.match(TokenType.LESS):
            self.consume(TokenType.IDENTIFIER, "Expect class name.")
            superclass = Expr.Variable(self.previous())
        self.consume(TokenType.LEFT_BRACE, "Expect '{' before class body.")
        methods = []
        while not self.check(TokenType.RIGHT_BRACE) and not self.isAtEnd():
            methods.append(self.function("method"))
        self.consume(TokenType.RIGHT_BRACE, "Expect '}' after class body.")
        return name, superclass, methods # as statement Class

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
        return self.expressionStatement()

    def forStatement(self) -> Stmt.Block:
        """
        This is a long implementation
        The syntax for a for loop is as following:
        for (initializer; condition; increment) { body }
        The initializer, condition, and increment can all technically be empty.
        The initializer can have a variable declaration or some expression statement
        The condition and increment are some expressions
        The body of the for loop is a statement
        Now if the incremement exists you want to create a block with the body with the
        increment added to the end of the body
        If the condition does not exist then we essentially have a while loop statement,
        we set the condition accordingly
        If the initializer is exists then we add it to the front of the body as a new block
        Finally we return this
        """
        ######################################################
        # TODO: Write your implementation here               #
        ######################################################















        ######################################################
        # End of your implementation                         #
        ######################################################

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
        return Stmt.Expression(expr)

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

    def block(self) -> List[Stmt.Stmt]:
        """
        Parse a code block -> { this part }
        While you are not at the end of a file right brace you want to
        parse each statement in the block and return it as a list
        """
        ######################################################
        # TODO: Write your implementation here               #
        ######################################################





        ######################################################
        # End of your implementation                         #
        ######################################################

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

    def andOperator(self) -> Expr.Expr:
        """
        Implement the AND operator parsing
        While the token type is the AND operator, we extract the operator and the recurse down
        to the function below for the right hand side.
        With this we update the current expression.
        """
        expr = self.equality()
        ######################################################
        # TODO: Write your implementation here               #
        ######################################################





        ######################################################
        # End of your implementation                         #
        ######################################################
        return expr

    def equality(self):
        expr = self.comparison()
        while self.match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
            operator = self.previous()
            right = self.comparison()
            expr = Expr.Binary(expr, operator, right)

        return expr

    def comparison(self) -> Expr.Expr:
        """
        Implement the comparison expression parsing
        While the token type is some comparison operator, we extract the opertaor and recurse down
        to the function below for the right hand side.
        With this we update the current expression.
        """
        expr = self.term()
        ######################################################
        # TODO: Write your implementation here               #
        ######################################################





        ######################################################
        # End of your implementation                         #
        ######################################################
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

    def synchronize(self):
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
