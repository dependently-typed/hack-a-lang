import Environment
from TokenType import TokenType
from RuntimeError import RuntimeError
import LoxCallable
import LoxFunction
import Lox
import Return


class Interpreter:
    def __init__(self):
        self.globals = Environment.Environment()
        self.environment = self.globals
        self.locals = dict()

    def interpret(self, statements):
        try:
            for statement in statements:
                value = self.execute(statement)
            return value
        except RuntimeError as error:
            raise RuntimeError(error, str(error))

    def evaluate(self, expr):
        return expr.accept(self)

    def execute(self, stmt):
        return stmt.accept(self)

    def executeBlock(self, statements, environment):
        previous = self.environment
        try:
            self.environment = environment
            for statement in statements:
                self.execute(statement)
        finally:
            self.environment = previous

    def visitBlock(self, stmt):
        self.executeBlock(stmt.statements, Environment.Environment(self.environment));
        return None

    '''
    Not including visitClassStmt here due to decision to not implement Lox classes
    '''

    def visitExpression(self, stmt):
        self.evaluate(stmt.expression)

    def visitFunction(self, stmt):
        function = LoxFunction.LoxFunction(stmt, self.environment, False)
        self.environment.define(stmt.name.lexeme, function)

    def visitIf(self, stmt):
        if self.isTrue(self.evaluate(stmt.condition)):
            self.execute(stmt.thenBranch)
        elif stmt.elseBranch is not None:
            self.execute(stmt.elseBranch)
        return None

    def visitPrint(self, stmt):
        value = self.evaluate(stmt.expression)
        print(self.stringify(value))

    def visitReturn(self, stmt):
        value = None
        if stmt.value is not None:
            value = self.evaluate(stmt.value)
        raise Return.Return(value)

    def visitVar(self, stmt):
        value = None
        if stmt.initializer is not None:
            value = self.evaluate(stmt.initializer)
        self.environment.define(stmt.name.lexeme, value)

    def visitWhile(self, stmt):
        while self.isTrue(self.evaluate(stmt.condition)):
            self.execute(stmt.body)

    def visitAssign(self, expr):
        value = self.evaluate(expr.value)
        distance = self.locals.get(expr, None)
        if distance is not None:
            self.environment.assignAt(distance, expr.name, value)
        else:
            self.globals.assign(expr.name, value)
        return value

    def visitBinary(self, expr):
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)
        operatorType = expr.operator.type

        if operatorType is TokenType.GREATER:
            self.checkNumberOperands(expr.operator, left, right)
            return float(left) > float(right)

        elif operatorType is TokenType.GREATER_EQUAL:
            self.checkNumberOperands(expr.operator, left, right)
            return float(left) >= float(right)

        elif operatorType is TokenType.LESS:
            self.checkNumberOperands(expr.operator, left, right)
            return float(left) < float(right)

        elif operatorType is TokenType.LESS_EQUAL:
            self.checkNumberOperands(expr.operator, left, right)
            return float(left) <= float(right)

        elif operatorType is TokenType.EQUAL_EQUAL:
            return self.isEqual(left, right)

        elif operatorType is TokenType.BANG_EQUAL:
            return not self.isEqual(left, right)

        elif operatorType is TokenType.MINUS:
            self.checkNumberOperands(expr.operator, left, right)
            return float(left) - float(right)

        elif operatorType is TokenType.PLUS:
            if isinstance(left, float) and isinstance(right, float):
                return float(left) + float(right)
            elif isinstance(left, str) and isinstance(right, str):
                return str(left) + str(right)

            raise RuntimeError(expr.operator, "Operands must be two numbers or two strings.")

        elif operatorType is TokenType.SLASH:
            self.checkNumberOperands(expr.operator, left, right)
            return float(left) / float(right)

        elif operatorType is TokenType.STAR:
            self.checkNumberOperands(expr.operator, left, right)
            return float(left) * float(right)

        return None

    def visitCall(self, expr):
        callee = self.evaluate(expr.callee)
        arguments = []
        for argument in expr.arguments:
            arguments.append(self.evaluate(argument))
        if not isinstance(callee, LoxCallable.LoxCallable):
            raise RuntimeError(expr.paren, "Can only call functions and classes.")
        function = callee
        if len(arguments) != function.arity():
            raise RuntimeError(expr.paren, "Expected " +
                               function.arity() + " arguments but got " +
                               arguments.size() + ".")
        return function.call(self, arguments)

    def visitGrouping(self, expr):
        return self.evaluate(expr.expression)

    def visitLogical(self, expr):
        left = self.evaluate(expr.left)
        if (expr.operator.type is TokenType.OR):
            if self.isTrue(left):
                return left
        else:
            if not self.isTrue(left):
                return left

        return self.evaluate(expr.right)

    def visitThis(self, expr):
        return self.lookUpVariable(expr.keyword, expr)

    def resolve(self, expr, depth):
        self.locals[expr] = depth

    def visitLiteral(self, expr):
        return expr.value

    def visitExpression(self, stmt):
        return self.evaluate(stmt.expression)

    def visitUnary(self, expr):
        right = self.evaluate(expr.right)
        operatorType = expr.operator.type

        if operatorType is TokenType.BANG:
            return not self.isTrue(right)

        elif operatorType is TokenType.MINUS:
            self.checkNumberOperand(expr.operator, right)
            return -float(right)

    def visitVariable(self, expr):
        return self.lookUpVariable(expr.name, expr)

    def lookUpVariable(self, name, expr):
        distance = self.locals.get(expr, None)
        if distance is not None:
            return self.environment.getAt(distance, name.lexeme)
        else:
            return self.globals.get(name)

    def checkNumberOperand(self, operator, operand):
        if not isinstance(operand, float):
            raise RuntimeError(operator, "Operand must be a number.")

    def checkNumberOperands(self, operator, left, right):
        if not (isinstance(left, float) and isinstance(right, float)):
            raise RuntimeError(operator, "Operands must be numbers.")

    def stringify(self, object):
        if object is None:
            return "nil"
        if isinstance(object, float):
            text = str(object)
            if text[-2:0] == ".0":
                text = text[0:-2]
            return text
        return str(object)

    def isEqual(self, left, right):
        if left is None:
            if right is None:
                return True
            else:
                return False
        else:
            return left == right

    def isTrue(self, boolean):
        if boolean is None:
            return False
        elif isinstance(boolean, bool):
            return bool(boolean)
        else:
            return True
