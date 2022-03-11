import Expr
import Stmt
import Scanner
import Token
from TokenType import TokenType

class AstPrinter:
    def printast(self, exprOrStmt):
        return exprOrStmt.accept(self)

    def visitBlock(self, stmt):
        string = "(block "
        for statement in stmt.statements:
            string += str(statement.accept(self))
        string += ")"
        return string

    def visitExpression(self, stmt):
        self.parenthesize(";", stmt.expression)

    def visitFunction(self, stmt):
        string = "(fun " + stmt.name.lexeme + "("
        for param in stmt.params:
            if param != stmt.params[0]: string += " "
            string += param.lexeme
        string += ") "
        for body in stmt.body:
            string += body.accept(self)
        string += ")"
        return string

    def visitIf(self, stmt):
        if stmt.elseBranch is None:
            return self.parenthesize2("if", stmt.condition, stmt.thenBranch)
        return self.parenthesize2("if-else", stmt.condition, stmt.thenBranch, stmt.elseBranch)
    
    def visitPrint(self, stmt):
        return self.parenthesize("print", stmt.expression)

    def visitReturn(self, stmt):
        if stmt.value is None: return "(return)"
        return self.parenthesize("return", stmt.value)

    def visitVar(self, stmt):
        if stmt.initializer is None:
            return self.parenthesize2("var", stmt.name)
        return self.parenthesize2("var", stmt.name, "=", stmt.initializer)

    def visitWhile(self, stmt):
        return self.parenthesize2("while", stmt.condition, stmt.body)

    def visitChain(self, expr):
        return self.parenthesize("chain", expr.left, expr.right)

    def visitAssign(self, expr):
        return self.parenthesize2("=", expr.name.lexeme, expr.value)

    def visitBinary(self, expr):
        return self.parenthesize(expr.operator.lexeme, expr.left, expr.right)

    def visitCall(self, expr):
        return self.parenthesize2("call", expr.callee, expr.arguments)
    
    def visitGrouping(self, expr):
        return self.parenthesize("group", expr.expression)

    def visitLiteral(self, expr):
        return str(expr.value)

    def visitUnary(self, expr):
        return self.parenthesize(expr.operator.lexeme, expr.right)
    
    def visitVariable(self, expr):
        return expr.name.lexeme

    def parenthesize(self, name, *exprs):
        '''
        Parenthesize Expressions
        '''
        string = "(" + name
        for expr in exprs:
            string += " "
            string += expr.accept(self)
        string += ")"
        return string

    def parenthesize2(self, name, *parts):
        '''
        Parenthesize Expressions, Statements, Lists, or Tokens
        TODO: Not completely working, parts to transform is passing all arguments as one.
        '''
        string = ""
        string += self.transform("(" + name, *parts)
        string += ")"
        return string
    
    def transform(self, string, *parts):
        '''
        Get strings for different types
        TODO: Not completely working, parts to transform is passing all arguments as one.
        '''
        for part in parts:
            string += " "
            if isinstance(part, Expr.Expr) or isinstance(part, Stmt.Stmt):
                string += part.accept(self)
            elif isinstance(part, Token.Token):
                string += part.lexeme
            else:
                string += str(part) # don't think we need extra list to array as in Java because python list
        return string
