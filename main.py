# coding=utf-8
from __future__ import print_function
from lex import get_lex
from pars import get_parser, get_errors, get_log
from termcolor import colored, cprint
from visitor import Visitor

parser = get_parser()
lexer = get_lex()


def test(i):
    v = Visitor()
    v.start(i)
    logger = v.get_logger()
    logger.printx()


x123 = '''
begin(m);

int function go_up()
start
   measure;
   enter(b!='o') do 
      enter(b=='1') do demolish; measure; until true;
      enter(b=='e') do return 0; until true;
      forward;
      print_map; 
      measure;     
   until true;
   return 0;
stop;

int function m() 
start
   print_map;
   str b;bind b;
   print_map;
   
   rotate_right;
   go_up();
   enter(b=='e') do forward; print_map; return 0; until true;
   
   rotate_left;
   go_up();
   enter(b=='e') do forward; print_map; return 0; until true;  
      
   rotate_left;
   enter(b!='e') do 
      go_up();
      enter(b=='e') do forward; print_map; return 0; until true;
      rotate_left; measure;
      enter(b=='1') do demolish; measure; until true;
      enter(b=='e') do forward; print_map; return 0; until true;
      forward; rotate_left; measure;
      enter(b=='e') do forward; print_map; return 0; until true;
      go_up();
      enter(b=='e') do forward; print_map; return 0; until true;
      rotate_right; measure;
      enter(b=='1') do demolish;measure; until true;
      enter(b=='e') do forward; print_map; return 0; until true;
      forward; rotate_right; measure;
      enter(b=='e') do forward; print_map; return 0; until true;
   until true; 
   
   return 0;
stop;
'''

test(x123)