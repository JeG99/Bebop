import ply.yacc as yacc
from lexer import tokens

def p_routine(p):
    '''
    routine : ROUTINE ID SEMICOLON GLOBALS COLON var_declarations PROCEDURES COLON function_declarations BEGIN COLON LSQBRACKET LOCALS COLON var_declarations INSTRUCTIONS COLON statements RSQBRACKET
    ''' 

def p_var_declarations(p):
    '''
    
    '''

def p_var_declaration(p):
    '''
    var_declaration : VAR ID 
    '''