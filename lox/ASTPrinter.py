import Expr
import Scanner

class AstPrinter:
    def printast(self, expr):
        return expr.accept(self)

    def visitChain(self, expr):
        return self.parenthesize("chain", expr.left, expr.right)

    def visitBinary(self, expr):
        return self.parenthesize(expr.operator.lexeme, expr.left, expr.right)

    def visitGrouping(self, expr):
        return self.parenthesize("group", expr.expression)

    def visitLiteral(self, expr):
        return str(expr.value)

    def visitUnary(self, expr):
        return self.parenthesize(expr.operator.lexeme, expr.right)

    def parenthesize(self, name, *exprs):
        string = "(" + name
        for expr in exprs:
            string += " "
            string += expr.accept(self)
        string += ")"
        return string

# expression = Expr.Binary(
#     Expr.Unary(
#         Scanner.Token(Scanner.TokenType.MINUS, "-", None, 1), Expr.Literal(123)),
#         Scanner.Token(Scanner.TokenType.STAR, "*", None, 1),
#         Expr.Grouping(Expr.Literal(45.67)
#     )
# )
# print(AstPrinter().printast(expression))
