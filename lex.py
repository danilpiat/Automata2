# ------------------------------------------------------------
# calclex.py
#
# tokenizer for a simple expression evaluator for
# numbers and +,-,*,/
# ------------------------------------------------------------
import ply.lex as lex
import sys

# List of token names.   This is always required
tokens = ['NUMBER', 'ID','BOOLEAN','STRING',
          'ASSIGNMENT', 'PLUS', 'MINUS', 'DIVIDE', 'TIMES', 'POWER',
          'LPAREN', 'RPAREN', 'PARENS', 'CLPAREN', 'CRPAREN', 'QRPAREN', 'QLPAREN',
          'DOUBLE_QUOTE', 'QUOTE',
          'BT', 'LT', 'EQ', 'NE', 'BE', 'LE',
          'COLON', 'SEMI', 'CONTINUE', 'COMMA', 'COMMENT', 'NEWLINE', 'DOT']

reserved = {
    # 'program': 'PROGRAM',
    # 'var': 'VAR',
    # 'then': 'THEN',
    # 'else': 'ELSE',
    # 'push': 'PUSH',
    # 'back': 'BACK',
    # 'pop': 'POP',


    'true': 'TRUE',
    'false': 'FALSE',
    'undefined': 'UNDEFINED',
    'bool': 'BOOL',
    'str': 'STR',
    'int': 'INT',
    'array': 'ARRAY',
    'function': 'FUNCTION',
    'of': 'OF',
    'to': 'TO',
    'begin': 'BEGIN',
    'end': 'END',
    'do': 'DO',
    'until': 'UNTIL',
    'enter': 'ENTER',

    'return': 'RETURN',
    'call': 'CALL',
    'start': 'START',
    'stop': 'STOP',
    'print' : 'PRINT',


    # robot
    'back': 'BACK',
    'right': 'RIGHT',
    'left': 'LEFT',
    'forward': 'FORWARD',
    'rotate_right': 'ROTATE_RIGHT',
    'rotate_left': 'ROTATE_LEFT',
    #'lms': 'LMS',
    'measure': 'MEASURE',
    'demolish': 'DEMOLISH',
    'bind' : 'BIND',
    'print_map' : 'PRINTMAP',

    # material
    '"GLASS"': 'GLASS',
    '"STEEL"': 'STEEL',
    '"WOOD': 'WOOD',
    '"PLASTIC"': 'PLASTIC',
    '"CONCRETE"': 'CONCRETE',
    '"EXIT"': 'EXIT',

}

tokens = list(tokens) + list(reserved.values())
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_PARENS = r'\(\s*\)'
t_COLON = r'\:'
t_ASSIGNMENT = r'\='
t_COMMA = r'\,'

t_POWER = r'\*\*'
t_EQ = r'\=\='
t_NE = r'\!\='
t_LT = r'\<'
t_BT = r'\>'
t_LE = r'\<\='
t_BE = r'\>\='
t_SEMI = r'\;'
t_CRPAREN = r'\]'
t_CLPAREN = r'\['
t_QRPAREN = r'\}'
t_QLPAREN = r'\{'
# Regular expression rules for simple tokens
t_PLUS = r'\+'
t_MINUS = r'-'
t_DOT = r'\.'


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')  # Check for reserved words
    return t


def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_STRING(t):
    r'(\".*\")|(\'.*\')'
    t.value = str(t.value)
    return t

t_ignore = ' \t'
t_ignore_COMMENT = r'\#.*'

def t_NEWLINE(t):
    r'\n+'
    #t.lexer.lineno += len(t.value)
    t.lexer.lineno += t.value.count('\n')
    #t.lexer.linestart = t.lexer.lexpos
    #return t

def t_error(t):
    sys.stderr.write('Error: Illegal character: %s at line %s\n' % (t.value[0], t.lexer.lineno))
    t.lexer.skip(1)

lexer = lex.lex()


def get_lex():
    return lex
