import sys

tab = "    " # Tab is four spaces
base_desc = {
    "Expr": {
        "Assign" : [["Token.Token", "name"], ["Expr", "value"]],
        "Chain": [["Expr", "left"], ["Expr", "right"]],
        "Unary": [["Token.Token", "operator"], ["Expr", "right"]],
        "Binary": [["Expr", "left"], ["Token.Token", "operator"], ["Expr", "right"]],
        "Logical": [["Expr", "left"], ["Token.Token", "operator"], ["Expr", "right"]],
        "Grouping" : [["Expr", "expression"]],
        "Literal" : [["object", "value"]],
        "Variable" : [["Token.Token", "name"]],
        "Variable" : [["Token.Token", "keyword"]],
        "Call" : [["Expr","callee"], ["Token.Token", "parent"], ["list","arguments"]]
    },
    "Stmt": {
        "Expression" : [["Expr", "expression"]],
        "Function" : [["Token.Token", "name"], ["list", "params"],["list", "body"]],
        "Expression" : [["Expr", "expression"]],
        "If": [["Expr", "condition"], ["Stmt", "thenBranch"],["Stmt", "elseBranch"]],
        "Print" : [["Expr","expression"]],
        "Return" : [["Token.Token","keyword"], ["Expr","value"]],
        "Var" : [["Token.Token", "name"], ["Expr", "initializer"]],
        "While" : [["Expr","condition"], ["Stmt", "body"]]
    }
}

def defineAst(file, baseName, types):
    file.write("import Scanner\nimport Token\n\n")
    file.writelines(["class " + baseName + ":\n", tab + "pass\n\n"])
    for ExprType, expr in types.items():
        defineType(file, baseName, ExprType, expr)

def defineStmt(file, baseName, types):
    file.write("import Scanner\nimport Token\nimport Expr\n\n")
    file.writelines(["class " + baseName + ":\n", tab + "pass\n\n"])
    for ExprType, expr in types.items():
        defineType(file, baseName, ExprType, expr)

def defineType(file, baseName, className, fields):
    types, names = zip(*fields)
    field_str = ", ".join(names)
    asserts = [tab + tab + "assert isinstance(" + field[1] + ", " + field[0] + ")\n" for field in fields]
    instances = [tab + tab + "self." + name + " = " + name + "\n" for name in names]
    file.write("\n")
    file.writelines(["class " + className + "(" + baseName + "):\n""", tab + "def __init__(self, " +field_str + "):\n"])
    file.writelines(asserts)
    file.write("\n")
    file.writelines(instances)
    file.write("\n")
    file.writelines([tab + "def accept(self, visitor):\n", tab + tab + "return visitor.visit" + className + "(self)\n\n"])


path = "../lox/Expr.py"
with open(path, "w+") as file:
    defineAst(file, "Expr", base_desc["Expr"])

path = "../lox/Stmt.py"
with open(path, "w+") as file:
    defineStmt(file, "Stmt", base_desc["Stmt"])
