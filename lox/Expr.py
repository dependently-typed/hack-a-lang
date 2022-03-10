import Scanner
import Token

class Expr:
    pass


class Assign(Expr):
    def __init__(self, name, value):
        assert isinstance(name, Token)
        assert isinstance(value, Expr)

        self.name = name
        self.value = value

    def accept(self, visitor):
        return visitor.visitAssign(self)


class Chain(Expr):
    def __init__(self, left, right):
        assert isinstance(left, Expr)
        assert isinstance(right, Expr)

        self.left = left
        self.right = right

    def accept(self, visitor):
        return visitor.visitChain(self)


class Unary(Expr):
    def __init__(self, operator, right):
        assert isinstance(operator, Token)
        assert isinstance(right, Expr)

        self.operator = operator
        self.right = right

    def accept(self, visitor):
        return visitor.visitUnary(self)


class Binary(Expr):
    def __init__(self, left, operator, right):
        assert isinstance(left, Expr)
        assert isinstance(operator, Token)
        assert isinstance(right, Expr)

        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor):
        return visitor.visitBinary(self)


class Logical(Expr):
    def __init__(self, left, operator, right):
        assert isinstance(left, Expr)
        assert isinstance(operator, Token)
        assert isinstance(right, Expr)

        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor):
        return visitor.visitLogical(self)


class Grouping(Expr):
    def __init__(self, expression):
        assert isinstance(expression, Expr)

        self.expression = expression

    def accept(self, visitor):
        return visitor.visitGrouping(self)


class Literal(Expr):
    def __init__(self, value):
        assert isinstance(value, object)

        self.value = value

    def accept(self, visitor):
        return visitor.visitLiteral(self)


class Variable(Expr):
    def __init__(self, keyword):
        assert isinstance(keyword, Token)

        self.keyword = keyword

    def accept(self, visitor):
        return visitor.visitVariable(self)


class Call(Expr):
    def __init__(self, callee, parent, arguments):
        assert isinstance(callee, Expr)
        assert isinstance(parent, Token)
        assert isinstance(arguments, list)

        self.callee = callee
        self.parent = parent
        self.arguments = arguments

    def accept(self, visitor):
        return visitor.visitCall(self)

