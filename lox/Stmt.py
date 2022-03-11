import Scanner
import Token
import Expr

class Stmt:
    pass

class Block(Stmt):
    def __init__(self, statements):
        assert isinstance(statements, list)

        self.statement = statements
    
    def accept(self, visitor):
        return visitor.visitBlockStmt(self)


class Expression(Stmt):
    def __init__(self, expression):
        assert isinstance(expression, Expr.Expr)

        self.expression = expression

    def accept(self, visitor):
        return visitor.visitExpression(self)


class Function(Stmt):
    def __init__(self, name, params, body):
        assert isinstance(name, Token.Token)
        assert isinstance(params, list)
        assert isinstance(body, list)

        self.name = name
        self.params = params
        self.body = body

    def accept(self, visitor):
        return visitor.visitFunction(self)


class If(Stmt):
    def __init__(self, condition, thenBranch, elseBranch):
        assert isinstance(condition, Expr.Expr)
        assert isinstance(thenBranch, Stmt)
        assert isinstance(elseBranch, Stmt)

        self.condition = condition
        self.thenBranch = thenBranch
        self.elseBranch = elseBranch

    def accept(self, visitor):
        return visitor.visitIf(self)


class Print(Stmt):
    def __init__(self, expression):
        assert isinstance(expression, Expr.Expr)

        self.expression = expression

    def accept(self, visitor):
        return visitor.visitPrint(self)


class Return(Stmt):
    def __init__(self, keyword, value):
        assert isinstance(keyword, Token.Token)
        assert isinstance(value, Expr.Expr)

        self.keyword = keyword
        self.value = value

    def accept(self, visitor):
        return visitor.visitReturn(self)


class Var(Stmt):
    def __init__(self, name, initializer):
        assert isinstance(name, Token.Token)
        assert isinstance(initializer, Expr.Expr)

        self.name = name
        self.initializer = initializer

    def accept(self, visitor):
        return visitor.visitVar(self)


class While(Stmt):
    def __init__(self, condition, body):
        assert isinstance(condition, Expr.Expr)
        assert isinstance(body, Stmt)

        self.condition = condition
        self.body = body

    def accept(self, visitor):
        return visitor.visitWhile(self)

