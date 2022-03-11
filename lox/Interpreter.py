import Environment
from TokenType import TokenType

class Interpreter:
    def __init__(self):
        # globals = Environment.Environment()
        # environment = globals
        locals = dict()

    def interpret(self, expression):
        value = self.evaluate(expression)
        return value


    def evaluate(self, expr):
        return expr.accept(self)

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

