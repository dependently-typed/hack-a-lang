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
            Get the value bound to a variable name (we're checking for the variable's existence at runtime)
            If found then return its value,
            If this environment has an enclosing environment, search it there.
            If it is not found we have an error of the variable being not defined.
        '''
        ######################################################
        # TODO: Write your implementation here               #
        ######################################################
        


        
        ######################################################
        # End of your implementation                         #
        ######################################################

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
