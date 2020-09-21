# Yacc example

import ply.yacc as yacc

# Get the token map from the lexer.  This is required.
from lex import tokens
from AST import *


errors = 0
log_p = []
def get_errors():
    return errors
def get_log():
    return log_p
def log(x):
    global log_p
    log_p.append(x)


def p_program(p):
    '''program : main statement_list'''#statement_list function_declare_list
    p[0] = Program(line=p.lineno(1), main=p[1], node=p[2])  # p[2]
    log("program")

def p_err1(p):
    '''statement_list : statement_list error'''
    p[0] = SyntaxError(line=p.lineno(2), str="statement_list")
    log("statement_list_err")

def p_err2(p):
    '''program : main error'''
    p[0] = SyntaxError(line=p.lineno(2), str="function_declare")
    log("function_declare_err")


def p_function_declare(p):
    '''function_declare : type_spec FUNCTION variable PARENS statement
                         | type_spec FUNCTION variable LPAREN arg_list RPAREN statement'''
    if len(p) == 6:
        p[0] = FunctionDeclare(line=p.lineno(1), retType=p[1], functionname=p[3], arglist=None, left=p[5])
    else:
        p[0] = FunctionDeclare(line=p.lineno(1), retType=p[1], functionname=p[3], arglist=p[5], left=p[7])
    log("function_declare")

"""
def p_function_declare_list(p):
    '''function_declare_list : function_declare
                              | function_declare_list function_declare'''
    if (isinstance(p[1],SyntaxError)):
        p[0] = p[1]
    elif len(p) == 2:
        p[0] = List(node=p[1],type="func")
        p[0].children = p[0].nodes
    else:
        p[1].nodes.append(p[2])
        p[1].children = p[1].nodes
        p[0] = p[1] #ListNode(left=p[1], right=p[2])
    log("function_declare_list")
"""

def p_compound_statement(p):
    '''compound_statement : START statement_list STOP'''
    p[0] = Compound(line=p.lineno(2), node=p[2])
    log("compound_statement")


def p_statementlist(p):
    '''statement_list : statement
                       | statement_list statement '''
    if (isinstance(p[1],SyntaxError)):
        p[0] = p[1]
    elif len(p) == 2:
        p[0] = List(line=p.lineno(1), node=p[1],type="statement")
        p[0].children = p[0].nodes
    else:
        p[1].nodes.append(p[2])
        p[1].children = p[1].nodes
        p[0] = p[1] #ListNode(left=p[1], right=p[2])
    log("statement_list")

#function_declare_list
def p_statement(p):
    '''statement : function_declare
                  | assigment_statement SEMI
                  | logic_expression SEMI
                  | variable_declaration_multiply SEMI
                  | variable_declaration SEMI
                  | compound_statement SEMI
                  | enter_do_until SEMI
                  | p_print_statement SEMI
                  | factor SEMI
                  | expression SEMI
                  | return SEMI
                  | robot_st SEMI
                  | bind SEMI
                  | empty'''
    p[0] = p[1]
    log("statement")

def p_err3(p):
    '''statement : assigment_statement error
                  | logic_expression error
                  | variable_declaration_multiply error
                  | compound_statement error
                  | enter_do_until error
                  | function_call error
                  | factor error
                  | expression error
                  | return error
                  | robot error
                  | robot_st error
                  | bind error
                  | p_print_statement error
                  | error PARENS
                  | error SEMI
                  | error'''
    if len(p) == 2:
        p[0] = SyntaxError(line=p.lineno(1), str="statement_list")
    else:
        p[0] = SyntaxError(line=p.lineno(2), str="statement_list")
    log("statement_list_err")


def p_print_statement(p):
    '''p_print_statement : PRINT LPAREN factor RPAREN
                         | PRINT LPAREN expression RPAREN
                         | PRINT LPAREN logic_expression RPAREN
                         | PRINT LPAREN varlist RPAREN
                         | PRINT PARENS'''
    if len(p) == 5:
        p[0] = PrintStatement(line=p.lineno(3), strx=p[3])
    else:
        p[0] = PrintStatement(line=p.lineno(1), strx='')


def p_return_statement(p):
    '''return : RETURN expression
              | RETURN factor'''
    p[0] = ReturnStatement(line=p.lineno(2), expr=p[2])
    log("return")


def p_robot_statement(p):
    '''robot : RIGHT
             | LEFT
             | BACK
             | FORWARD
             | ROTATE_RIGHT
             | ROTATE_LEFT
             | DEMOLISH'''
    p[0] = RobotStatement(line=p.lineno(1), op=p[1])
    log("robot")

def p_robot_statement2(p):
    '''robot_st : MEASURE
                 | PRINTMAP'''
    p[0] = RobotStatement(line=p.lineno(1), op=p[1])
    log("robot_st")

def p_bind(p):
    '''bind : BIND variable'''
    p[0] = BindStatement(line=p.lineno(1), variable=p[2])


def p_function_call(p):
    '''function_call : variable LPAREN varlist RPAREN
                     | variable PARENS'''
    if len(p) == 5:
       p[0] = FunctionCall(line=p.lineno(1), functionname=p[1],arglist=p[3])
    else:
        p[0] = FunctionCall(line=p.lineno(1), functionname=p[1], arglist=None)
    log('function_call1')


def p_function_call_call(p):
    '''function_call : CALL LPAREN variable COMMA variable RPAREN
                     | CALL LPAREN variable RPAREN'''
    if len(p)==6:
        p[0] = FunctionCall(line=p.lineno(1), functionname=p[3], arglist=p[5], fromcall=True)
    else :
        p[0] = FunctionCall(line=p.lineno(1), functionname=p[3], arglist=None, fromcall=True)
    log('function_call2')


def p_enter_do_until(p):
    '''enter_do_until : ENTER LPAREN logic_expression RPAREN DO statement_list UNTIL boolean
                      | ENTER LPAREN factor RPAREN DO statement_list UNTIL boolean'''
    p[0] = EnterDoUntil(line=p.lineno(1), logic=p[3], statementList=p[6], until=p[8])
    log('enter_do_until')


def p_assign(p):
    '''assigment_statement : asig_left ASSIGNMENT expression
                           | asig_left ASSIGNMENT initializer
                           | asig_left ASSIGNMENT assigment_statement'''
    p[0] = Assigment(line=p.lineno(1), left=p[1], right=p[3])
    log("assigment_statement")


def p_assign_left(p):
    '''asig_left : variable
                | getarrel'''
    p[0]= p[1]


def p_initializer(p):
    '''initializer : QLPAREN varlist QRPAREN
                   |  QLPAREN initializer_list QRPAREN'''
    p[0] = Initializer(line=p.lineno(1), node=p[2])
    log("initializer")


def p_initializer_list(p):
    '''initializer_list : initializer
                        | initializer_list COMMA initializer
                        | empty '''
    if len(p) == 2:
        p[0] = List(line=p.lineno(1), node=p[1],type="init")
        p[0].children = p[0].nodes
    else:
        p[1].nodes.append(p[3])
        p[1].children = p[1].nodes
        p[0] = p[1] #ListNode(left=p[1], right=p[2])
    log("initializer_list")


#                | CLPAREN variable CRPAREN
#                | CLPAREN expression CRPAREN
def p_indexing(p):
    '''indexing : CLPAREN factor CRPAREN
                | indexing CLPAREN factor CRPAREN'''
    if len(p) == 4:
        p[0] = List(line=p.lineno(1), node=p[2],type="index")
        p[0].children = p[0].nodes
    else:
        p[1].nodes.append(p[3])
        p[1].children = p[1].nodes
        p[0] = p[1] #ListNode(left=p[1], right=p[2])
    log("indexing")

def p_getarrel(p):
    '''getarrel : factor indexing'''
    p[0] = GetArrElement(line=p.lineno(1), varname=p[1],index=p[2])
    log("getarrel")


def p_conversion(p):
    '''type_conversion : LPAREN type_spec RPAREN'''
    p[0] = TypeConversion(line=p.lineno(2), type=p[2])
    log("type_conversion")

def p_arg_list(p):
    '''arg_list : variable_declaration
                 | arg_list COMMA variable_declaration'''
    if len(p) == 2:
        p[0] = List(line=p.lineno(1), node=p[1],type="args")
        p[0].children = p[0].nodes
    else:
        p[1].nodes.append(p[3])
        p[1].children = p[1].nodes
        p[0] = p[1]
    log("arg_list")


def p_variable_declaration_multiply(p):
    '''variable_declaration_multiply : type_spec varlist
                                     | type_spec varlist_with_assigment'''
    p[0] = VariableDeclarationMultiply(line=p.lineno(2), type=p[1], nodes=p[2])
    log("variable_declaration_multiply")


def p_variable_declaration(p):
    '''variable_declaration : type_spec variable
                             | type_spec assigment_statement'''
    p[0] = VariableDeclaration(line=p.lineno(2), type=p[1], node=p[2])
    log("variable_declaration")


def p_varlist_with_assigment(p):
    '''varlist_with_assigment : assigment_statement
                              | variable
                              | varlist_with_assigment COMMA assigment_statement
                              | varlist_with_assigment COMMA variable'''
    if len(p) == 2:
        p[0] = List(line=p.lineno(1), node=p[1],type="var_decl")
        p[0].children = p[0].nodes
    else:
        p[1].nodes.append(p[3])
        p[1].children = p[1].nodes
        p[0] = p[1]
    log("varlist_with_assigment")

def p_varlist(p):
    '''varlist : variable
                | varlist COMMA variable
                | factor
                | varlist COMMA expression
                | expression
                | varlist COMMA factor
                | logic_expression
                | varlist COMMA logic_expression'''
    if len(p) == 2:
        p[0] = List(line=p.lineno(1), node=p[1],type="var")
        p[0].children = p[0].nodes
    else:
        p[1].nodes.append(p[3])
        p[1].children = p[1].nodes
        p[0] = p[1]
    log("varlist")


def p_type_spec(p):
    '''type_spec : INT
                 | BOOL
                 | STR
                 | array_type'''
    p[0] = Type(line=p.lineno(1), value=p[1])
    log("type_spec")



def p_array_type_spec(p):
    '''array_type : ARRAY OF INT
                  | ARRAY OF BOOL
                  | ARRAY OF STR'''
    p[0] = TypeArray(line=p.lineno(1), value=p[3])
    log("array_type")

def p_main(p):
    'main : BEGIN LPAREN variable RPAREN SEMI'
    p[0] = FunctionCall(line=p.lineno(1), functionname=p[3])
    log("main")


def p_empty(p):
    '''empty : NEWLINE
             | '''
    p[0] = NoOp(line=None)
    log("empty")


def p_logic_operators(p):
    '''logic_expression : boolean
                        | factor logic factor
                        | logic_expression logic factor
                        | robot'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = LogicOp(line=p.lineno(1), left=p[1], right=p[3], op=p[2])
    log("logic_expr")


def p_logic(p):
    '''logic : LE
            | BE
            | LT
            | BT
            | EQ
            | NE'''
    p[0] = p[1]
    log("logic")

def p_binary_operators(p):
    '''expression : term
                   | expression PLUS term
                   | expression MINUS term
        term       : factor
                   | term TIMES factor
                   | term DIVIDE factor'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = BinOp(line=p.lineno(1), left=p[1], right=p[3], op=p[2])
    log("expr")

def p_var_id(p):
    'variable : ID'
    p[0] = Variable(line=p.lineno(1), varname=p[1])
    log("variable")


def p_factor_v(p):
    '''number : NUMBER'''
    p[0] = Number(line=p.lineno(1), value=p[1])
    log("number")

def p_boolean(p):
    '''boolean : TRUE
               | FALSE
               | UNDEFINED'''
    p[0] = Boolean(line=p.lineno(1), value=p[1])
    log("boolean")


def p_factor_v3(p):
    '''string : STRING'''
    p[0] = String(line=p.lineno(1), value=p[1])
    log("string")


def p_factor(p):
    '''factor : MINUS factor
               | PLUS factor
               | type_conversion factor
               | LPAREN expression RPAREN
               | variable
               | getarrel
               | number
               | string
               | boolean
               | function_call'''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 3:
        if isinstance(p[1],TypeConversion):
            p[1].value = p[2]
            p[0] = p[1]
        else:
            p[0] = UnOp(line=p.lineno(2), op=p[1], left=p[2])
    else:
        p[0] = p[2]
    log("factor")



# Error rule for syntax errors
def p_error(p):
    log("Syntax error in input!")
    global errors
    errors += 1


parser = yacc.yacc()
parser.defaulted_states = {}

def get_parser():
    return parser
