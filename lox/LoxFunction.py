from LoxCallable import LoxCallable

class LoxFunction(LoxCallable):
    def __init__(self, declaration, closure, isInitializer):
        self.isInitializer = isInitializer
        self.closure = closure
        self.declaration = declaration

    def __str__(self):
        return "<fn " + declaration.name.lexeme + ">"

    def arity(self):
        return len(declaration.params)

    def call(self, interpreter, arguements):
        environment = Environment.Environment(self.closure)
        for i in range(len(declaration.params)):
            environment.define(declaration.params[i].lexeme, arguements[i])

        interpreter.executeBlock(declaration.body, environment);
