import Environment
from TokenType import TokenType

class Interpreter:
    def __init__(self):
        self.globals = Environment.Environment()
        self.environment = self.globals
        self.locals = dict()

    def interpret(self, statements):
        for statement in statements:
            value = self.execute(statement)
        return value


    def evaluate(self, expr):
        return expr.accept(self)

    def execute(self, stmt):
        return stmt.accept(self)

    def visitLiteral(self, expr):
        return expr.value

    def visitExpression(self, stmt):
        return self.evaluate(stmt.expression)


    def visitUnary(self, expr):
        right = self.evaluate(expr.right)
        operatorType = expr.operator.type

        if operatorType is TokenType.MINUS:
            return -float(right)

        elif operatorType is TokenType.BANG :
            return not self.isTrue(right)

        return None

    def isTrue(self,boolean):
        if boolean is None:
            return False
        elif isinstance(boolean, bool):
            return bool(boolean)
        else:
            return True


    def visitLogical(self, expr):
        left = self.evaluate(expr.left)
        if (expr.operator.type is TokenType.OR):
            if self.isTrue(left):
                return left
        else:
            if not self.isTrue(left):
                return left

        return self.evaluate(expr.right)

    def visitBinary(self, expr):
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)
        operatorType = expr.operator.type

        if operatorType is TokenType.GREATER:
            return float(left) > float(right)

        elif operatorType is TokenType.GREATER_EQUAL:
            return float(left) >= float(right)

        elif operatorType is TokenType.LESS:
            return float(left) < float(right)

        elif operatorType is TokenType.LESS_EQUAL:
            return float(left) <= float(right)

        elif operatorType is TokenType.EQUAL_EQUAL:
            return self.isEqual(left, right)

        elif operatorType is TokenType.BANG_EQUAL:
            return not self.isEqual(left, right)

        elif operatorType is TokenType.MINUS:
            return float(left) - float(right)

        elif operatorType is TokenType.PLUS:
            if (isinstance(left, float) and isinstance(right, float)):
                return float(left) + float(right)
            elif (isinstance(left, str) and isinstance(right, str)):
                return str(left) + str(right)

            #ERROR: must be of same time

        elif operatorType is TokenType.SLASH:
            return float(left) / float(right)

        elif operatorType is TokenType.STAR:
            return float(left) * float(right)

        return None

    def isEqual(self, left, right):
        if left is None:
            if right is None:
                return True
            else:
                return False
        else:
            return left == right

    def visitIf(self,stmt):
        if self.isTrue(self.evaluate(stmt.condition)):
            self.execute(stmt.thenBranch)
        elif stmt.elseBranch != None:
            self.execute(stmt.elseBranch)
        return None


    def visitBlock(self, stmt):
        self.executeBlock(stmt.statements, Environment.Environment(self.environment));
        return None

    def executeBlock(self, statements, environment):
        previous = self.environment
        try:
            self.environment = environment
            for i in statements:
                self.execute(i)
        finally:
            self.environment = previous

    def visitPrint(self, stmt):
        value = self.evaluate(stmt.expression)
        print(str(value))
