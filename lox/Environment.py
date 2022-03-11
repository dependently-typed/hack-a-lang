import RuntimeError


class Environment:
    values = {}

    def __init__(self):
        self.enclosing = None

    def __init__(self, enclosing):
        self.enclosing = enclosing

    def get(self, name):
        if name.lexeme in self.values:
            return self.values[name.lexeme]

        if not self.enclosing is None:
            return self.enclosing.get(name)

        raise RuntimeError.RuntimeError(name, "Undefined variable '" + name.lexeme + "'.")

    def assign(self, name, value):
        if name.lexeme in self.values:
            self.values[name.lexeme] = value
            return

        if not self.enclosing is None:
            self.enclosing.assign(name, value)

        raise RuntimeError.RuntimeError(name, "Undefined variable '" + name.lexeme + "'.")

    def define(self, name, value):
        self.values[name] = value

    def ancestor(self, distance):
        environment = self
        for i in range(0, distance):
            environment = environment.enclosing
        return environment

    def getAt(self, distance, name):
        return self.ancestor(distance).values[name]

    def assignAt(self, distance, name, value):
        self.ancestor(distance).values[name] = value

    def __str__(self):
        result = str(self.values)
        if not self.enclosing is None:
            result += " -> " + str(self.enclosing)
        return result
