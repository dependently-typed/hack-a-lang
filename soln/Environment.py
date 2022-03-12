from RuntimeError import *
from Token import Token

class Environment:
    def __init__(self, enclosing=None):
        self.values = {}
        self.enclosing = enclosing

    def define(self, name: str, value: object):
        '''
            define a new variable
            if variable exists, redefine it
        '''
        self.values[name] = value

    def get(self, name: Token):
        '''
            get the value bound to a variable name
            we're checking for the variable's existence at runtime
        '''
        if name.lexeme in self.values:
            return self.values[name.lexeme]

        elif self.enclosing is not None:
            return self.enclosing.get(name)
        
        else:
            raise RuntimeError(name, f"Undefined variable {name.lexeme}")

    def assign(self, name: Token, value: object):
        if name.lexeme in self.values:
            self.values[name.lexeme] = value

        elif self.enclosing is not None:
            self.enclosing.assign(name, value)
            return
        
        else:
            raise RuntimeError(name, f"Undefined variable {name.lexeme}")

    def define(self, name, value):
        self.values[name] = value

    def ancestor(self, distance):
        environment = self
        for i in range(0, distance):
            environment = environment.enclosing
        return environment

    def getAt(self, distance, name):
        return self.ancestor(distance).values.get(name)

    def assignAt(self, distance, name, value):
        self.ancestor(distance).values[name] = value

    def __str__(self):
        result = str(self.values)
        if not self.enclosing is None:
            result += " -> " + str(self.enclosing)
        return result
