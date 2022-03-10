import Expr
import Scanner
import TokenType
import Expr
import Stmt


class Parser:
    def __init__(self, tokenList):
        self.current = 0
        self.tokenList = tokenList

    def parse(self):
        statements = []
        while not self.isAtEnd():
            statements.append(self.declaration())
        return statements

    def expression(self):
        return self.assignment()

    def declaration(self):
        try:
            if self.match("CLASS"): return self.classDeclaration()
            if self.match("FUN"): return self.function("function")
            if self.match("VAR"): return self.varDeclaration()
            return self.statement()
        except Exception: # create ParseError?
            self.synchronise()
            return None

    def classDeclaration(self):
        name = self.consume("IDENTIFIER", "Expect class name.")
        superclass = None
        if self.match("LESS"):
            self.consume("IDENTIFIER", "Expect class name.")
            superclass = self.previous() # as Expr.Variable
        self.consume("LEFT_BRACE", "Expect '{' before class body.")
        methods = []
        while not self.check("RIGHT_BRACE") and not self.isAtEnd():
            methods.append(self.function("method"))
        self.consume("RIGHT_BRACE", "Expect '}' after class body.")
        return name, superclass, methods # as statement

    def statement(self):
        if self.match("FOR"): self.forStatement()
        if self.match("IF"): self.ifStatement()
        if self.match("PRINT"): self. printStatement()
        if self.match("RETURN"): self.returnStatement()
        if self.match("WHILE"): self.whileStatement()
        if self.match("LEFT_BRACE"): self.block() # as statement
        return self.expressionStatement()

    def forStatement(self):
        self.consume("LEFT_PAREN", "Expect '(' after 'for'.")
        initializer = None
        if self.match("SEMICOLON"): initializer = None
        elif self.match("VAR"): initializer = self.varDeclaration()
        else: initializer = expressionStatement()

        condition = None
        if not self.check("SEMICOLON"):
            condition = self.expression()
        self.consume("SEMICOLON", "Expect ';' after loop condition.")

        increment = None
        if not self.check("RIGHT_PAREN"):
            increment = self.expression()
        self.consume("RIGHT_PAREN", "Expect ')' after for clauses.")

        body = self.statement()
        if increment is not None:
            body = [body, increment] # refer to line 165 in Parser.java, Need Statement Block

        if condition is None: condition = Expr.Literal(True)
        body - (condition, body) # as statement

        if initializer is not None:
            body = [initializer, body] # as statement block

        return body

    def ifStatement(self):
        self.consume("LEFT_PAREN", "Expect '(' after 'if'.")
        condition = self.expression()
        self.consume("RIGHT_PAREN", "Expect ')' after if condition.")
        thenBranch = self.statement()
        elseBranch = None
        if self.match("ELSE"):
            elseBranch = self.statement()
        return condition, thenBranch, elseBranch # as statement

    def printStatement(self):
        value = self.expression()
        self.consume("SEMICOLON", "Expect ';' after value.")
        return value # as statement

    def returnStatement(self):
        keyword = self.previous()
        value = None
        if not self.check("SEMICOLON"):
            value = self.expression()
        self.consume("SEMICOLON", "Expect ';' after return value.")
        return keyword, value # as statement

    def varDeclaration(self):
        name = self.consume("IDENTIFIER", "Expect variable name.")
        initializer = None
        if self.match("EQUAL"):
            initializer = self.expression()
        self.consume("SEMICOLON", "Expect ';' after variable declaration.")
        return name, initializer # as statement

    def whileStatement(self):
        self.consume("LEFT_PAREN", "Expect '(' after 'while'.")
        condition = self.expression()
        self.consume("RIGHT_PAREN", "Expect ')' after condition.")
        body = self.statement()
        return condition, body # as statement

    def expressionStatement(self):
        expr = self.expression()
        self.consume("SEMICOLON", "Expect ';' after expression.")
        return expr # as statement

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
