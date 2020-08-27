from termcolor import colored, cprint
from anytree import Node, RenderTree
class Logger:
    def __init__(self):
        self.code = None
        self.log_p = []
        self.log_s = []
        self.log_v = []
        self.log_e = []
        self.symbol_table_copy = []
        self.function_table_copy = []
        self.result_tree = None

    def append_screen(self, x):
        if len(x)>0:
           self.symbol_table_copy.append(str(x))
    def append_screen_function(self, x):
        self.function_table_copy.append(str(x))
    def set_code(self, c):
        self.code = c
    def set_log_p(self,*x):
        self.log_p = x
    def set_tree(self, tree):
        self.result_tree = tree
    def log_parse(self, *s):
        self.log_p.append(str(s))
    def log_semantic(self, *s):
        self.log_s.append(str(s))
    def log_visit(self, *s):
        self.log_v.append(str(s))
    def log_error(self, *s):
        self.log_e.append(str(s))

    def print_parse(self):
        cprint("parse_log", 'yellow')
        print(self.log_p)
    def print_semantic(self):
        cprint("semantic_log", 'yellow')
        for i in self.log_s:
            print(i)
    def print_visit(self):
        cprint("visit_log", 'yellow')
        for i in self.log_v:
            print(i)
    def print_screens(self):
        cprint("screens_log", 'yellow')
        tables = self.symbol_table_copy
        for i in tables:
            print(i)
    def print_error(self):
        cprint("errors_log", 'yellow')
        if len(self.log_e) == 0:
            cprint('Haven`t errors', 'blue')
        else:
            for i in self.log_e:
                cprint(i, 'red')
    def print_tree(self):
        cprint("tree", 'yellow')
        for pre, fill, node in RenderTree(self.result_tree):
            print("%s%s,%s" % (pre, node.name, node.line))

    def printx(self, color='yellow', filler="-------------------------"):
        cprint("%s" % (filler+'\n') * 5, 'blue')
        self.filler = filler
        self.color = color
        cprint("%s" % self.filler, self.color)
        self.print_tree()
        cprint("%s" % self.filler, self.color)
        self.print_parse()
        cprint("%s" % self.filler, self.color)
        self.print_semantic()
        cprint("%s" % self.filler, self.color)
        self.print_visit()
        cprint("%s" % self.filler, self.color)
        self.print_screens()
        cprint("%s" % self.filler, self.color)
        self.print_error()
        cprint("%s" % self.filler, self.color)
        cprint("%s" % (filler + '\n') * 5, 'blue')