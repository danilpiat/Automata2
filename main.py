# coding=utf-8
from __future__ import print_function
from lex import get_lex
from pars import get_parser, get_errors, get_log
from termcolor import colored, cprint
from visitor import Visitor
import os
parser = get_parser()
lexer = get_lex()


def test():
    path = os.getcwd() + "/results "
    if not os.path.isdir(path):
        os.mkdir(path)
    for j in os.listdir("tests"):
           text = open("tests/"+j, "r")
           i = text.read()
           print(i)
           v = Visitor()
           v.start(str(i))
           logger = v.get_logger()
           logger.printx()

test()