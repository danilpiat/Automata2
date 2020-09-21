from __future__ import print_function
from AST import *
from colorama import Fore, Back, Style
import colorama
from termcolor import colored, cprint
from anytree import Node, RenderTree
import numpy as np


class XExceptions(Exception):
    def __init__(self, s):
        self.info = s

    def __str__(self):
        return self.info


class Stack:
    def __init__(self):
        self.call_stack = []
        self.last_frame = None

    def new_frame(self):
        self.call_stack.append(StackFrame())
        self.last_frame = self.call_stack[-1]

    def remove_frame(self):
        self.call_stack.pop()
        if len(self.call_stack) > 0:
            self.last_frame = self.call_stack[-1]
        else:
            self.last_frame = None

    def get(self):
        if len(self.call_stack) > 0:
            return self.last_frame.symbol_table, self.last_frame.functions_table
        else:
            return None, None

    def get_st(self, name, all=False):
        # print("-"*10)
        # for i in self.call_stack:
        #     print(i)
        # print("-"*10)
        t = None
        for i in self.call_stack[::-1]:
            t = i.symbol_table.get(name)
            if t is not None:
                if all:
                    return t
                return t[1]
        return t

    def get_func(self, name):
        t = None
        for i in self.call_stack[::-1]:
            t = i.functions_table.get(name)
            if t is not None:
                return t
        return t

    def set_st(self, name, value):
        for i in self.call_stack[::-1]:
            t = i.symbol_table.get(name)
            if t is not None:
                i.symbol_table[name] = (t[0], value)

    def add_st(self, type, name, value):
        if (isinstance(type, Type)):
            type = type.value
        if (isinstance(type, TypeArray)):
            type = 'array of %s' % type.value
            if value is None:
                value = {}
        # print (type)
        if (isinstance(name, Variable)):
            name = name.varname
        self.last_frame.symbol_table[name] = (type, value)


class Array:
    def __init__(self, a):
        self.arr = a

    def get_shape(self):
        return self.arr.shape

    def __str__(self):
        return ' '.join(self.arr)


class StackFrame:
    def __init__(self):
        self.symbol_table = {}
        self.functions_table = {}
    def __str__(self):
        return str(self.symbol_table)

class Function:
    def __init__(self, arglist, ret_type, code):
        self.args = arglist
        self.ret = ret_type
        self.code = code


