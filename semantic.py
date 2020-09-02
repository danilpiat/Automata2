from __future__ import print_function
from collections import Iterable
from six import string_types
from AST import *
from visitor import *
from classes import *
from logger import Logger
import numpy as np
def flatten(obj):
     for i in obj:
         if isinstance(i, Iterable) and not isinstance(i, string_types):
             yield from flatten(i)
         else:
             yield i

# self.log_error(s="error at line: %s" % node.left.line)


class Semantic:
    def __init__(self, l):
        self.return_address = None
        self.stack = Stack()
        self.symbol_table = None
        self.functions_table = None
        self.error_list = []
        self.parent_function = None
        self.logger = l

    def log_error(self, s):
        self.error_list.append(s)

    def new_frame(self):
        self.stack.new_frame()
        self.symbol_table, self.functions_table = self.stack.get()

    def remove_frame(self):
        self.stack.remove_frame()
        self.symbol_table, self.functions_table = self.stack.get()

    def start(self, result):
        self.new_frame()
        self.visit(result)
        self.remove_frame()
        self.errors = len(self.error_list)

    def visit(self, result):
        self.logger.log_semantic("semantic: %s" % result.name)
        if isinstance(result, Variable):
            return self.xvisitVariable(result)
        elif isinstance(result, BinOp):
            return self.xvisitBinOp(result)
        elif isinstance(result, UnOp):
            return self.xvisitUnOp(result)
        elif isinstance(result, Number):
            return self.xvisitNumber(result)
        elif isinstance(result, Boolean):
            return self.xvisitBoolean(result)
        elif isinstance(result, String):
            return self.xvisitString(result)
        elif isinstance(result, Assigment):
            self.xvisitAssigment(result)
        elif isinstance(result, Compound):
            self.xvisitCompound(result)
        elif isinstance(result, ListNode):
            self.xvisitListNode(result)
        elif isinstance(result, List):
            self.xvisitList(result)
        elif isinstance(result, FunctionDeclare):
            self.xvisitFunctionDeclare(result)
        elif isinstance(result, Program):
            self.xvisitProgram(result)
        elif isinstance(result, VariableDeclaration):
            self.xvisitVariableDeclaration(result)
        elif isinstance(result, VariableDeclarationMultiply):
            self.xvisitVariableDeclarationMultiply(result)
        elif isinstance(result, ReturnStatement):
            self.xvisitReturn(result)
        elif isinstance(result, FunctionCall):
            self.xvisitFunctionCall(result)
        elif isinstance(result, EnterDoUntil):
            return self.xvisitEnterDoUntil(result)
        elif isinstance(result, LogicOp):
            return self.xvisitLogicOp(result)
        elif isinstance(result, Initializer):
            self.xvisitInitializer(result)
        elif isinstance(result, NoOp):
            return ['empty']
        elif isinstance(result, TypeConversion):
            return self.xvisitTypeConversion(result)
            """
            elif isinstance(result, NoOp):
            pass"""
        elif isinstance(result, GetArrElement):
            return self.xvisitGetArrElement(result)
        elif isinstance(result, PrintStatement):
            return self.visit(result.strx)
        else:
            # raise XExceptions("Gavno")
            self.logger.log_visit(result)

    def get_call_list_types(self, node):
        if node.arglist is not None:
            return [self.get_type(i) for i in node.arglist.nodes]
        else:
            return None

    def get_func_list_types(self, node):
        t = self.stack.get_func(node.functionname.varname)
        self.logger.log_semantic(t)
        self.logger.log_semantic(node.functionname.varname)
        self.logger.log_semantic(self.functions_table)
        if t is None:
            self.log_error(s="undeclared func=%s"%node.functionname.varname)
            return
        if t.args is not None:
               #print(t.args.nodes)
               #print(self.get_type(t.args.nodes[0]))
            return [self.get_type(i) for i in t.args.nodes]
        else:
            return None

    def check_ops(self, node):
        self.logger.log_semantic("semantic_check_inner")
        self.logger.log_semantic(node)
        ty = list(np.array([self.get_type(node.left), self.get_type(node.right)]).reshape(1, -1)[0])
        ty = flatten(ty)
        types = list(set(ty).difference(['any']))
        expected_types = [types[0]]
        self.logger.log_semantic(ty)
        self.logger.log_semantic(types)
        self.logger.log_semantic(expected_types)
        if (types == expected_types):
            self.logger.log_semantic("good types")
        else:
            self.logger.log_semantic("bad types")
            self.log_error(s="check_ops: bad types at line: %s; expected %s and found %s" %
                             (node.line, expected_types, types[1:]))
            # list(set(A) - set(B))
            self.logger.log_semantic(*expected_types)

    def get_type(self, node):
        if isinstance(node, Boolean):
            return self.visit(node)
        elif isinstance(node, Number):
            return self.visit(node)
        elif isinstance(node, String):
            return self.visit(node)
        elif isinstance(node, BinOp):
            return [self.get_type(node.left), self.get_type(node.right)]
        elif isinstance(node, LogicOp):
            return [self.get_type(node.left), self.get_type(node.right)]
        elif isinstance(node, Variable):
            return self.visit(node)
        elif isinstance(node, FunctionCall):
            t = self.stack.get_func(node.functionname.varname)
            if t is None:
                self.log_error(s="not declared function at line: %s" % node.line)
                return ['any']
            else:
                self.logger.log_semantic("ret=%s" % t.ret)
                return [t.ret]
        elif isinstance(node, Initializer):
            """
            if isinstance(node.left, NoOp):
                return ['empty array']
            """
            types = []
            self.arr_get_type(node.left.nodes, types)
            self.logger.log_semantic("types=%s" % types)
            types = list(set(types).difference(['any']))
            expected_types = [types[0]]
            if (types == expected_types):
                self.logger.log_semantic("good types")
                return ['array of %s' % types[0]]
            else:
                self.logger.log_semantic("bad types")
                self.log_error(s="get_type: bad types at line: %s; expected %s and found %s" %
                                 (node.line, expected_types, types[1:])) #[1:]
                # list(set(A) - set(B))
                self.logger.log_semantic(*expected_types)
                return ['not an array']
        elif isinstance(node, TypeConversion):
            return [self.visit(node)]
        elif isinstance(node, GetArrElement):
            return [self.visit(node)]
        elif isinstance(node, VariableDeclaration) or isinstance(node, VariableDeclarationMultiply):
            return [node.type.value]


    def arr_get_type(self, k, types):
        for i in k:
            if isinstance(i, Initializer):
                self.arr_get_type(i.left.nodes,types)
            else:
                self.logger.log_semantic (i)
                types.append(self.visit(i)[0])

    def xvisitVariable(self, result):
        print(result.varname)
        t = self.stack.get_st(result.varname, all=True)
        if t is None:
            self.log_error(s="not declared variable %s at line: %s" % (result.varname, result.line))
            return ['any']
        else:
            return [t[0]]

    def xvisitBinOp(self, result):
        self.logger.log_semantic("semantic_check (BinOp & LogicOp)")
        self.check_ops(result)

    def xvisitUnOp(self, result):
        return self.visit(result.left)

    def xvisitString(self, result):
        return ['str']

    def xvisitNumber(self, result):
        return ['int']

    def xvisitBoolean(self, result):
        return ['bool']

    def xvisitAssigment(self, result):
        self.logger.log_semantic("semantic_check (Assigment)")
        if isinstance(result.right, Assigment):
            found = self.xvisitAssigment(result.right)
        else:
            found = self.get_type(result.right)
        expected_types = self.get_type(result.left)
        expected_types = list(flatten(expected_types))[0]
        found = list(flatten(found))[0]
        self.logger.log_semantic("exp=%s" % expected_types)
        # self.semantic_check(i.right)
        self.logger.log_semantic(result.left)
        self.logger.log_semantic(result.right)
        #found = self.get_type(result.right)
        #expected_types = self.get_type(result.left)
        self.logger.log_semantic("expected=%s,found=%s" % (expected_types, found))
        if (found == expected_types) | ((found == 'array of empty') & (expected_types != 'array of empty')) :
            self.logger.log_semantic("good types")
        else:
            self.logger.log_semantic("bad types")
            self.log_error(s="assig: bad types at line: %s; variable %s expected %s and found %s" %
                             (result.line, result.left.varname, expected_types, found[1:])) #
        return found

    def xvisitCompound(self, result):
        self.visit(result.node)

    def xvisitListNode(self, result):
        pass

    def xvisitList(self, result):
        for i in result.nodes:
            self.visit(i)

    def xvisitFunctionDeclare(self, result):
        self.logger.log_semantic("semantic_check (FunctionDeclare)")
        t = self.functions_table.get(result.functionname.varname)
        if t is not None:
            self.log_error(s="redeclared function %s at line %s" %
                             (result.functionname.varname,result.line))
        else:
            self.functions_table[result.functionname.varname] = Function(arglist=result.arglist, ret_type=result.retType.value,
                                                                code=result.left)
        self.new_frame()
        self.parent_function = result.functionname.varname
        func = self.stack.get_func(result.functionname.varname)
        if func.args is not None:
            for j in range(len(func.args.nodes)):
                name = None
                type = func.args.nodes[j].type.value
                func_arg = func.args.nodes[j]
                if (isinstance(func_arg, Variable)):
                    name = func_arg.varname
                elif (isinstance(func_arg, VariableDeclaration)):
                    if (isinstance(func_arg.node, Assigment)):
                        name = func_arg.node.left.varname
                    else:
                        name = func_arg.node.varname
                self.stack.add_st(type=type, name=name, value=None)
        self.visit(result.left)
        self.remove_frame()


    def xvisitReturn(self, result):
        self.logger.log_semantic("semantic_check (ReturnStatement)")
        found = [self.stack.get_func(self.parent_function).ret]
        expected_type = self.get_type(result.left)
        if found == expected_type:
            self.logger.log_semantic("good types")
        else:
            self.logger.log_semantic("bad types")
            self.log_error(s="bad types at line: %s; expected %s and found %s" %
                             (result.line, expected_type, found))

    def xvisitProgram(self, result):
        self.visit(result.node)

    def xvisitVariableDeclaration(self, result):
        self.logger.log_semantic("semantic_check (VariableDeclaration)")
        type = result.type
        name = None
        line = 0
        if isinstance(result.node, Variable):
            name = result.node.varname
            line = result.node.line
        elif isinstance(result.node, Assigment):
            name = result.node.left.varname
            line = result.node.left.line
        t = self.symbol_table.get(name)
        if t is not None:
            self.log_error(s="redeclared variable %s at line %s" %
                             (name, line))
        else:
            self.stack.add_st(type, name, None)
        self.logger.log_semantic(self.symbol_table)
        return result.type

    def xvisitVariableDeclarationMultiply(self, result):
        self.logger.log_semantic("semantic_check (VariableDeclarationMultiply)")
        type = result.type
        names = [None] * len(result.nodes.nodes)
        line = 0
        self.logger.append_screen(self.symbol_table.copy())
        for j in range(len(result.nodes.nodes)):
            x = result.nodes.nodes[j]
            if isinstance(x, Variable):
                names[j] = x.varname
                line = x.line
            elif isinstance(x, Assigment):
                names[j] = x.left.varname
                line = x.left.line
            t = self.symbol_table.get(names[j])
            if t is not None:
                self.log_error(s="redeclared variable %s at line %s" %
                                 (names[j], line))
            else:
                self.stack.add_st(type, name=names[j], value=None)
        return result.type

    def xvisitFunctionCall(self, result):
        self.logger.log_semantic("semantic_check (FunctionCall)")
        found = self.get_call_list_types(result)
        expected_types = self.get_func_list_types(result)
        self.logger.log_semantic("found:%s" % found)
        self.logger.log_semantic("expected:%s" % expected_types)
        if found == expected_types:
            self.logger.log_semantic("good types")
            func = self.stack.get_func(result.functionname.varname)

        else:
            self.logger.log_semantic("bad types")
            self.log_error(s="bad types at line: %s; expected %s and found %s" %
                             (result.line, expected_types, found))

    def xvisitEnterDoUntil(self, result):
        self.logger.log_semantic("sem EnterDoUntil")
        return self.visit(result.statementList)

    def xvisitLogicOp(self, result):
        self.xvisitBinOp(result)

    def xvisitInitializer(self, result):
        pass

    def xvisitTypeConversion(self, result):
        t = self.get_type(result.value)
        if result.type.value == t[0]:
            self.logger.log_semantic (result.type.value)
            return result.type.value
        elif result.type.value != 'str':
            self.log_error(s="Unable to convert %s to %s at line %s" %
                             (result.value.value,result.type.value, result.line))
            return result.type.value
        else:
            return result.type.value

    def xvisitGetArrElement(self, result):
        types = []
        for i in result.left.nodes:
            types.append(self.visit(i))
        self.logger.log_semantic("GetArrElement=%s" % types)
        s = self.visit(result.varname)
        self.logger.log_semantic("s=%s" % s[0][9:])
        if 'array of' in s[0]:
            return s[0][9:]
        else:
            return s




"""
        if isinstance(node.left, BinOp):
            bin1 = node.left
            self.logger.log_semantic bin1
            t = self.check(bin1)
            if not t:
                self.log_error(s="error at line: %s" % node.left.line)
            return self.check_type_equality(node.right.value, bin1.right.value)
        elif isinstance(node.left, Variable):

        elif isinstance(node.right, Variable):

        else:
            return self.check_type_equality(node.right.value, node.left.value)
        """
"""
    def check_Assigment(self, node, te):
        t = self.check_Variable(node.left)
        if t[0] == te:
            return True
        return False

    def check_TypeConversion(self, node):
        pass
"""

"""
    def check_value_type(self, value, type):
        if isinstance(value, bool) & type == 'bool':
            return True
        elif isinstance(value, int) & type == 'int':
            return True
        elif isinstance(value, str) & type == 'str':
            return True
        else:
            return False

    def check_type_equality(self, value1, value2):
        self.logger.log_semantic value1, value2
        if isinstance(value1, bool) & isinstance(value2, bool):
            return 'bool'
        elif isinstance(value1, int) & isinstance(value2, int) & (not isinstance(value1, bool)) & (
        not isinstance(value2, bool)):
            return 'int'
        elif isinstance(value1, str) & isinstance(value2, str):
            return 'str'
        else:
            return False
"""
