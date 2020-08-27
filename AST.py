from anytree import NodeMixin


class AST: pass


class SyntaxError(AST, NodeMixin):
    def __init__(self, line, str=None, parent=None, children=None):
        self.name = "SyntaxError " + str
        self.str = str
        self.line = line

    def __str__(self):
        return "(Class %s: %s)" % (self.name, self.str)


class PrintStatement(AST, NodeMixin):
    def __init__(self, line, strx, parent=None, children=None):
        self.name = "PrintStatement"
        self.strx = strx
        self.line = line

    def __str__(self):
        return "Class %s: %s" %(self.name, self.strx)


class BindStatement(AST, NodeMixin):
    def __init__(self, line, variable, parent=None, children=None):
        self.name = "BindStatement"
        self.variable = variable
        self.line = line

    def __str__(self):
        return "(Class %s: %s)" % (self.name, self.variable)


class RobotStatement(AST, NodeMixin):
    def __init__(self, line, op, parent=None, children=None):
        self.name = "RobotStatement"
        self.op = op
        self.line = line

    def __str__(self):
        return "(Class %s: %s)" % (self.name, self.op)


class ReturnStatement(AST, NodeMixin):
    def __init__(self, line, expr, parent=None, children=None):
        self.name = "ReturnStatement"
        self.left = expr
        self.children = [expr]
        self.line = line

    def __str__(self):
        return "(Class %s: %s)" % (self.name, self.left)


class TypeConversion(AST, NodeMixin):
    def __init__(self, line, type, value=None, parent=None, children=None):
        self.name = "TypeConversion"
        self.children = [type]
        self.type = type
        self.value = value
        self.line = line

    def __str__(self):
        return "(Class %s: %s,%s)" % (self.name, self.type, self.value)


class GetArrElement(AST, NodeMixin):
    def __init__(self, line, index, varname, parent=None, children=None):
        self.name = "GetArrElement"
        self.children = [index]
        self.varname = varname
        self.left = index
        self.line = line

    def __str__(self):
        return "(Class %s: %s,%s)" % (self.name, self.varname, self.left)


class Indexing(AST, NodeMixin):
    def __init__(self, line, node, parent=None, children=None):
        self.name = "Indexing"
        self.left = node
        self.children = [node]
        self.line = line

    def __str__(self):
        return "(Class %s: %s)" % (self.name, self.left)


class Initializer(AST, NodeMixin):
    def __init__(self, line, node, parent=None, children=None):
        self.name = "Initializer"
        self.children = [node]
        self.left = node
        self.line = line

    def __str__(self):
        return "(Class %s: %s)" % (self.name, self.left)


class EnterDoUntil(AST, NodeMixin):
    def __init__(self, line, statementList, logic, until, parent=None, children=None):
        self.name = "EnterDoUntil"
        self.statementList = statementList
        self.logic = logic
        self.children = [statementList]
        self.until = until
        self.line = line

    def __str__(self):
        return "(Class %s: %s,%s)" % (self.name, self.logic, self.statementList)


class FunctionCall(AST, NodeMixin):
    def __init__(self, line, functionname, arglist=None, fromcall=False, parent=None, children=None):
        self.name = "FunctionCall"
        self.functionname = functionname
        self.arglist = arglist
        self.fromcall = fromcall
        self.line = line

    def __str__(self):
        return "(Class %s: %s,%s)" % (self.name, self.functionname, self.fromcall)

class FunctionDeclare(AST, NodeMixin):
    def __init__(self, line, functionname, arglist, retType, left, parent=None, children=None):
        if arglist is not None:
            print (arglist)
            self.name = "FunctionDeclare" + " " + str(retType) + " " + str(arglist.nodes)
        else:
            self.name = "FunctionDeclare" + " " + str(retType)
        self.functionname = functionname
        self.arglist = arglist
        self.retType = retType
        self.left = left
        self.children = [left]
        self.line = line
        self.returnx = None
    def __str__(self):
        return "(Class %s: %s,%s,%s)" % (self.name, self.retType, self.name, self.arglist)

class List(AST, NodeMixin):
    def __init__(self, line, node, type, parent=None, children=None):
        self.name = "List " + type
        self.nodes = [node]
        self.type = type
        self.line = line

    def __str__(self):
        return "(Class %s:%s)" % (self.name, self.nodes)


class Program(AST, NodeMixin):
    def __init__(self, line, main, node, parent=None, children=None):
        self.name = "Program"
        self.main = main
        self.node = node
        self.children = [node, main]  # [main,node]
        self.line = line

    def __str__(self):
        return "(Class %s: %s)" % (self.name, self.main)


class TypeArray(AST, NodeMixin):
    def __init__(self, line, value, parent=None, children=None):
        self.name = "TypeArray"
        self.value = value
        self.line = line

    def __str__(self):
        return "(Class %s: %s)" % (self.name, self.value)


class Type(AST, NodeMixin):
    def __init__(self, line, value, parent=None, children=None):
        self.name = "Type"
        self.value = value
        self.line = line

    def __str__(self):
        return "(Class %s: %s)" % (self.name, self.value)


class VariableDeclarationMultiply(AST, NodeMixin):
    def __init__(self, line, type, nodes, parent=None, children=None):
        self.name = "VariableDeclarationMultiply"
        self.type = type
        self.nodes = nodes
        self.children = [nodes]
        self.line = line

    def __str__(self):
        return "(Class %s: %s,%s)" % (self.name, self.type, self.nodes)


class VariableDeclaration(AST, NodeMixin):
    def __init__(self, line, type, node, parent=None, children=None):
        self.name = "VariableDeclaration"
        self.type = type
        self.node = node
        self.line = line
        self.children = [node]

    def __str__(self):
        return "(Class %s: %s,%s)" % (self.name, self.type, self.node)


class DeclarationList(AST, NodeMixin):
    def __init__(self, line, left, right, parent=None, children=None):
        self.name = "DeclarationList"
        self.left = left
        self.right = right
        self.line = line

    def __str__(self):
        return "(Class %s: %s,%s)" % (self.name, self.left, self.right)


class Number(AST, NodeMixin):
    def __init__(self, line, value, parent=None, children=None):
        self.name = "Number"
        self.value = value
        self.line = line

    def __str__(self):
        return "(Class %s: %s)" % (self.name, self.value)


class Boolean(AST, NodeMixin):
    def __init__(self, line, value, parent=None, children=None):
        if "true" in value:
            self.value = True
        elif "false" in value:
            self.value = False
        elif "undefined" in value:
            self.value = None
        self.name = "Boolean"
        self.line = line

    def __str__(self):
        return "(Class %s: %s)" % (self.name, self.value)


class String(AST, NodeMixin):
    def __init__(self, line, value, parent=None, children=None):
        self.name = "String"
        self.value = value
        self.line = line

    def __str__(self):
        return "(Class %s: %s)" % (self.name, self.value)


class BinOp(AST, NodeMixin):
    def __init__(self, line, op, left, right, parent=None, children=None):
        self.name = "BinOp"
        self.children = [left, right]
        self.op = op
        self.left = left
        self.right = right
        self.line = line

    def __str__(self):
        return "(Class %s: %s %s %s)" % (self.name, self.left, self.op, self.right)


class LogicOp(AST, NodeMixin):
    def __init__(self, line, op, left, right, parent=None, children=None):
        self.name = "LogicOp"
        self.children = [left, right]
        self.op = op
        self.left = left
        self.right = right
        self.line = line

    def __str__(self):
        return "(Class %s: %s %s %s)" % (self.name, self.left, self.op, self.right)


class UnOp(AST, NodeMixin):
    def __init__(self, line, op, left, parent=None, children=None):
        self.name = "UnOp"
        self.children = [left]
        self.op = op
        self.left = left
        self.line = line

    def __str__(self):
        return "(Class %s: %s %s)" % (self.name, self.op, self.left)


class Variable(AST, NodeMixin):
    def __init__(self, line, varname, parent=None, children=None):
        self.name = "Variable"
        self.varname = varname
        self.line = line

    def __str__(self):
        return "(Class %s: %s)" % (self.name, self.varname)


class Assigment(AST, NodeMixin):
    def __init__(self, line, left, right, parent=None, children=None):
        self.name = "Assigment"
        self.right = right
        self.left = left
        self.children = [left, right]
        self.line = line

    def __str__(self):
        return "(Class %s: %s = %s)" % (self.name, self.left, self.right)


class Compound(AST, NodeMixin):
    def __init__(self, line, node, parent=None, children=None):
        self.name = "Compound"
        self.node = node
        self.children = [node]
        self.line = line

    def __str__(self):
        return "(Class %s: %s)" % (self.name, self.node)


class Main(AST, NodeMixin):
    def __init__(self, line, node, programname, parent=None, children=None):
        self.name = "Main"
        self.programname = programname
        self.node = node
        self.children = [node]
        self.line = line

    def __str__(self):
        return "(Class %s: %s)" % (self.name, self.node)


class ListNode(AST, NodeMixin):
    def __init__(self, line, left, right=None, parent=None, children=None):
        self.name = "ListNode"
        self.left = left
        self.right = right
        if right is not None:
            self.children = [left, right]
        else:
            self.children = [left]
        self.line = line

    def __str__(self):
        if self.right is not None:
            return "(Class %s: %s,%s)" % (self.name, self.left, self.right)
        else:
            return "(Class %s: %s)" % (self.name, self.left)


class NoOp(AST, NodeMixin):
    def __init__(self, line, parent=None, children=None):
        self.name = "NoOp"
        self.line = line

    def __str__(self):
        return "(Class %s)" % self.name
