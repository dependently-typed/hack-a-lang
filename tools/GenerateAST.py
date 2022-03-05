import sys

tab = "    " # Tab is four spaces
base_desc = {
    "Expr": {
        "Chain": [["Expr", "left"], ["Expr", "right"]],
        "Unary": [["Scanner.Token", "operator"], ["Expr", "right"]],
        "Binary": [["Expr", "left"], ["Scanner.Token", "operator"], ["Expr", "right"]],
        "Grouping" : [["Expr", "expression"]],
        "Literal" : [["object", "value"]]
    }
}

def defineAst(file, baseName, types):
    file.write("import Scanner\n\n\n")
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
