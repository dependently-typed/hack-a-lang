from LoxCallable import LoxCallable
import Environment
from Return import Return

class LoxFunction(LoxCallable):
    def __init__(self, declaration, closure, isInitializer):
        self.isInitializer = isInitializer
        self.closure = closure
        self.declaration = declaration

    def __str__(self):
        return "<fn " + self.declaration.name.lexeme + ">"

    def arity(self):
        return len(self.declaration.params)

    def call(self, interpreter, arguements):
        environment = Environment.Environment(self.closure)
        for i in range(len(self.declaration.params)):
            environment.define(self.declaration.params[i].lexeme, arguements[i])

        try:
            interpreter.executeBlock(self.declaration.body, environment)
        except Return as returnValue:
            return returnValue.value

        return None

