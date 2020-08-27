# coding=utf-8
from __future__ import print_function
from pars import get_parser, get_errors, get_log
from AST import *
from semantic import *
from classes import *
from semantic import Semantic
from logger import Logger
from robot import Robot

# cprint('Вывод с помощью cprint', 'green', 'on_blue')
class Visitor:
    def __init__(self):
        self.stack = None
        self.semantic = None
        self.errors = None
        self.robot = None
        self.bind = None
        self.reflect = None
        self.main = None
        self.return_address = None
        self.symbol_table = None
        self.functions_table = None
        self.returnx = False
        self.logger = Logger()
        l = get_log()
        self.logger.set_log_p(l)
        colorama.init()

    def get_logger(self):
        return self.logger

    def start(self, code):
        parser = get_parser()
        result = parser.parse(code)
        self.errors = get_errors()
        if self.errors > 0:
            return
        self.logger.set_tree(result)
        self.semantic = Semantic(self.logger)
        self.semantic.start(result)
        if self.semantic.errors > 0:
            self.logger.log_error(self.semantic.error_list)
            return
        self.stack = Stack()
        self.robot = Robot()
        self.visit(result)
        # self.logger.log_visit(self.symbol_table)
        # self.logger.append_screen(self.symbol_table.copy())
        self.logger.log_visit(self.functions_table)
        self.logger.log_visit(self.main)

    def new_frame(self):
        self.stack.new_frame()
        self.symbol_table, self.functions_table = self.stack.get()

    def remove_frame(self):
        self.stack.remove_frame()
        self.symbol_table, self.functions_table = self.stack.get()

    def visit(self, result):
        self.logger.log_visit("visit: %s" % result.name)
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
            return self.xvisitAssigment(result)
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
            return self.xvisitFunctionCall(result)
        elif isinstance(result, EnterDoUntil):
            self.xvisitEnterDoUntil(result)
        elif isinstance(result, LogicOp):
            return self.xvisitLogicOp(result)
        elif isinstance(result, Initializer):
            return self.xvisitInitializer(result)
        elif isinstance(result, GetArrElement):
            return self.xvisitGetArrEl(result)
        elif isinstance(result, TypeConversion):
            return self.xvisitTypeConversion(result)
        elif isinstance(result, PrintStatement):
            self.xvisitPrintStatement(result)
        elif isinstance(result, RobotStatement):
            return self.xvisitRobot(result)
        elif isinstance(result, BindStatement):
            self.xvisitBind(result)
        elif isinstance(result, NoOp):
            pass
        else:
            # raise XExceptions("Gavno")
            self.logger.log_visit(result)

    def xvisitList(self, node):
        for i in node.nodes:
            if isinstance(i,ReturnStatement):
                raise XExceptions("out")
            self.visit(i)

    def xvisitBind(self, node):
        self.bind = node.variable.varname
        self.stack.set_st(name=self.bind, value='0')

    def xvisitRobot(self, node):
        if node.op != "measure":
           return self.robot.action(node)
        elif node.op == "measure":
            self.stack.set_st(name=self.bind, value=self.robot.action(node))

    def xvisitTypeConversion(self, node):
        if node.type.value == "int":
            return str(self.visit(node.value))
        elif node.type.value == "bool":
            return str(self.visit(node.value))
        elif node.type.value == "str":
            return str(self.visit(node.value))

    def xvisitGetArrEl(self, node):
        arr = self.stack.get_st(node.varname.varname)
        indexes = self.xvisitIndexing(node.left)
        x = arr
        for i in indexes:
            x = x[i]
        return x

    def set_arr_element(self, node, x):
        self.logger.append_screen(self.symbol_table)
        if not isinstance(node, GetArrElement):
            raise XExceptions("not a GetArrElement")
        ind = self.xvisitIndexing(node.left)
        arr = self.stack.get_st(node.varname.varname)
        self.logger.log_visit(arr)
        for i in ind[0:-1]:
            arr = arr[i]
            self.logger.log_visit(arr)
        arr[ind[-1]] = x
        self.logger.log_visit(arr)
        self.logger.append_screen(self.symbol_table)

    def xvisitIndexing(self, node):
        return [self.visit(i) for i in node.nodes]

    def xvisitNumber(self, node):
        return node.value

    def xvisitBinOp(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        if (left is None) | (right is None):
            # self.logger.log_visit(self.symbol_table)
            self.logger.append_screen(self.symbol_table.copy())
            raise XExceptions("Gavno2")
        if node.op == '+':
            return left + right
        elif node.op == '-':
            return left - right
        elif node.op == '/':
            return left / right
        elif node.op == '*':
            return left * right
        elif node.op == '**':
            return left ** right

    def xvisitLogicOp(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        if (left is None) or (right is None):
            # self.logger.log_visit  (self.symbol_table)
            self.logger.append_screen(self.symbol_table.copy())
            print(node.right,node.left)
            raise XExceptions("Gavno2")
        """
        if (isinstance(node.left,Variable)):
            left = left[1]
        if (isinstance(node.right,Variable)):
            right = right[1]
        """
        if node.op == '!=':
            self.logger.log_visit(node.op)
            return left != right
        elif node.op == '==':
            self.logger.log_visit(node.op)
            return left == right
        elif node.op == '>':
            self.logger.log_visit(node.op)
            return left > right
        elif node.op == '<':
            self.logger.log_visit(node.op)
            return left < right
        elif node.op == '>=':
            self.logger.log_visit(node.op)
            return left >= right
        elif node.op == '<=':
            self.logger.log_visit(node.op)
            return left <= right

    def xvisitUnOp(self, node):
        if node.op == '-':
            return -(self.visit(node.left))

    def xvisitVariable(self, node):
        return self.stack.get_st(node.varname)

    def xvisitAssigment(self, node):
        value = self.visit(node.right)
        if isinstance(node.right,FunctionCall):
            value = self.return_address
            self.return_address = None
        if isinstance(node.left, GetArrElement):
            self.set_arr_element(node.left, value)
        else:
            self.stack.set_st(name=node.left.varname, value=value)
        self.logger.append_screen(self.symbol_table)
        return value

    def xvisitCompound(self, node):
        self.visit(node.node)

    def xvisitListNode(self, node):
        self.visit(node.left)
        self.visit(node.right)

    def xvisitFunctionDeclare(self, node):
        self.functions_table[node.functionname.varname] = Function(arglist=node.arglist, ret_type=node.retType.value,
                                                                   code=node.left)
        self.logger.log_visit(self.functions_table)

    def xvisitProgram(self, node):
        self.main = node.main.functionname
        self.logger.log_visit("call main %s" % str(self.main))
        self.new_frame()
        self.visit(node.node)
        self.visit(node.main)
        self.remove_frame()
        # self.main = node.value.varname

    def xvisitVariableDeclaration(self, node):
        type = node.type
        name = None
        value = None
        if isinstance(node.node, Variable):
            name = node.node.varname
        elif isinstance(node.node, Assigment):
            name = node.node.left.varname
            value = self.visit(node.node.right)
        if value is None and self.return_address is not None:
            value = self.return_address
            self.return_address = None
        self.stack.add_st(type, name, value)
        # self.logger.log_visit(self.symbol_table)
        self.logger.append_screen(self.symbol_table.copy())

    def xvisitVariableDeclarationMultiply(self, node):
        type = node.type
        names = [None] * len(node.nodes.nodes)
        values = [None] * len(node.nodes.nodes)
        for j in range(len(node.nodes.nodes)):  # reversed(range)
            i = node.nodes.nodes[j]
            if isinstance(i, Variable):
                names[j] = i.varname
                values[j] = None
            elif (isinstance(i, Assigment)):
                names[j] = i.left.varname
                # self.logger.log_visit(self.symbol_table)
                values[j] = (self.visit(i.right))
            self.logger.append_screen(self.symbol_table)
            self.stack.add_st(type, name=names[j], value=values[j])

    def xvisitFunctionCall(self, node):
        self.new_frame()
        parent_frame = self.stack.call_stack[-2]
        func = self.stack.get_func(node.functionname.varname)
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
                if len(node.arglist.nodes) > j:
                    call_arg = node.arglist.nodes[j]
                    if (isinstance(call_arg, Variable)):
                        value = parent_frame.symbol_table.get(call_arg.varname)[1]
                    else:
                        value = self.visit(call_arg.right)
                else:
                    if isinstance(func_arg.node, Variable):
                        value = self.visit(func_arg.node.varname)
                self.stack.add_st(type=type, name=name, value=value)
        else:
            self.logger.log_visit("without args")
        try:
            self.visit(func.code)
        except XExceptions:
            k = 0
        # self.logger.log_visit(self.symbol_table)
        self.logger.append_screen(self.symbol_table)
        self.remove_frame()
        return self.return_address

    def xvisitReturn(self, node):
        self.return_address = self.visit(node.left)

    def xvisitEnterDoUntil(self, node):
        res = self.visit(node.logic)
        until = self.visit(node.until)
        while res == until:
            self.new_frame()
            self.visit(node.statementList)
            self.remove_frame()
            res = self.visit(node.logic)
            self.logger.log_visit("res = %s,until = %s" % (res, until))

    def xvisitBoolean(self, node):
        return node.value

    def xvisitInitializer(self, node):
        t = {}
        for i in range(len(node.left.nodes)):
            t[i] = self.visit(node.left.nodes[i])
        return t

    def xvisitPrintStatement(self, node):
        if isinstance(node.strx,List):
            s = [self.visit(i) for i in node.strx.nodes]
            print(*s, sep=',')
            for i in s:
                print(type(i))
        else:
            s = self.visit(node.strx)
            print(s)

    def xvisitString(self, node):
        return node.value.strip("\'")


"""
    def get_st(self, name):
        self.logger.log_visit  name
        return self.symbol_table.get(name)[1]
"""
"""
    def xvisitVariableDeclarationMultiply(self, node):
        type = node.type
        names = [None] * len(node.nodes.nodes)
        values = [None] * len(node.nodes.nodes)
        for j in range(len(node.nodes.nodes)):  # reversed(range)
            i = node.nodes.nodes[j]
            if isinstance(i, Variable):
                names[j] = i.varname
                values[j] = None
            elif (isinstance(i, Assigment)):
                names[j] = i.left.varname
                self.logger.log_visit  self.stack.symbol_table
                values[j] = self.visit(i.right)
        for i in range(len(names)):
            self.add_st(type, name=names[i], value=values[i])
"""
"""
        self.statementList = statementList
        self.logic = logic
        self.children = [statementList]
        self.until = until
"""
"""
f.args 
f.ret 
f.code 
"""
