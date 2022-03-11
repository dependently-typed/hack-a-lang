from LoxCallable import LoxCallable

# TODO finish class
class LoxFunction(LoxCallable):
    def __init__(self, declaration, closure, isInitializer):
        self.isInitializer = isInitializer
        self.closure = closure
        self.declaration = declaration

    def __str__(self):
        return "<fn " + self.declaration.name.lexeme + ">"

    def arity(self):
        return len(self.declaration.params)
