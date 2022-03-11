class LoxCallable:
    pass

class LoxFunction(LoxCallable):
    def __init__(self, declaration, closure, isInitializer):
        self.isInitializer = isInitializer
        self.closure = closure
        self.declaration = declaration

    def __str__(self):
        return "<fn " + declaration.name.lexeme + ">"

    def arity(self):
        return len(declaration.params)


