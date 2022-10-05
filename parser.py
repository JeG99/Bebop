import ply.yacc as yacc
from lexer import lexer, tokens
import sys

proc_dir = {}
curr_scope = "global"

def p_routine(p):
    '''
    routine : ROUTINE proc_dir_init ID SEMICOLON GLOBALS COLON var_declarations PROCEDURES COLON function_declarations BEGIN COLON LSQBRACKET LOCALS COLON var_declarations INSTRUCTIONS COLON statements RSQBRACKET
    ''' 
    p[0] = 1

def p_proc_dir_init(p):
    '''
    proc_dir_init :
    '''
    proc_dir['global'] = { 'var_table' : {} }
    curr_scope = 'global'

def p_var_declarations(p):
    '''
    var_declarations : VAR simple_declaration var_declarations
                     | VAR array_declaration var_declarations
                     | VAR matrix_declaration var_declarations
                     | empty
    '''

def p_simple_declaration(p): 
    '''
    simple_declaration : ID COLON var_type SEMICOLON 
    '''
    proc_dir[curr_scope]['var_table'].append({ 
        p[1] : {
            'type': p[3],
            'indexed': False
        } 
    })

def p_array_declaration(p):
    '''
    array_declaration : ID LSQBRACKET CONST_INT RSQBRACKET COLON type SEMICOLON 
    '''
    proc_dir[curr_scope]['var_table'].append({ 
        p[1] : {
            'type': p[6],
            'indexed': True,
            'dimensionality': 1,
            'size': p[3]
        } 
    })

def p_matrix_declaration(p):
    '''
    matrix_declaration : ID LSQBRACKET CONST_INT RSQBRACKET LSQBRACKET CONST_INT RSQBRACKET COLON type SEMICOLON
    '''
    proc_dir[curr_scope]['var_table'].append({ 
        p[1] : {
            'type': p[9],
            'indexed': True,
            'dimensionality': 2,
            'rows': p[3],
            'columns': p[6]
        } 
    })

def p_var_type(p):
    '''
    var_type : type
             | DF
    '''
    p[0] = p[1]

def p_function_declarations(p):
    '''
    function_declarations : PROC ID LPAREN params RPAREN COLON func_type LBRACKET LOCALS COLON var_declarations INSTRUCTIONS COLON statements RBRACKET function_declarations
                          | PROC ID LPAREN params RPAREN COLON func_type LBRACKET LOCALS COLON var_declarations INSTRUCTIONS COLON statements return SEMICOLON RBRACKET function_declarations
                          | empty
    '''

def p_return(p):
    '''
    return : RETURN expression
    '''

def p_func_type(p):
    '''
    func_type : type
              | VOID
    '''

def p_params(p):
    '''
    params : type ID params
           | COMMA type ID params
           | empty
    '''

def p_statements(p):
    '''
    statements : write SEMICOLON statements
               | read SEMICOLON statements
               | var_assignment SEMICOLON statements
               | condition SEMICOLON statements
               | loop SEMICOLON statements
               | function_call SEMICOLON statements
               | special_function_call SEMICOLON statements
               | empty
    '''

def p_write(p):
    '''
    write : WRITE write_params0
    '''

def p_write_params0(p):
    '''
    write_params0 : expression write_params1
                  | CONST_TEXT write_params1
    '''

def p_write_params1(p):
    '''
    write_params1 : COMMA expression write_params1
                  | COMMA CONST_TEXT write_params1
                  | empty
    '''

def p_read(p):
    '''
    read : READ ID
    '''

def p_var_assignment(p):
    '''
    var_assignment : ID ASSIGN expression
                   | ID LSQBRACKET expression RSQBRACKET ASSIGN expression
                   | ID LSQBRACKET expression RSQBRACKET LSQBRACKET expression RSQBRACKET ASSIGN expression
    '''

def p_condition(p):
    '''
    condition : IF LPAREN hyper_expression RPAREN LBRACKET statements RBRACKET
              | IF LPAREN hyper_expression RPAREN LBRACKET statements RBRACKET ELSE LBRACKET statements RBRACKET    
    '''

def p_loop(p):
    '''
    loop : REPEAT LPAREN hyper_expression RPAREN LBRACKET statements RBRACKET
    '''

def p_function_call(p):
    '''
    function_call : ID LPAREN call_params0 RPAREN 
    '''

def p_call_params0(p):
    '''
    call_params0 : expression call_params1
                 | empty
    '''

def p_call_params1(p):
    '''
    call_params1 : COMMA expression call_params1
                 | empty
    '''

def p_special_function_call(p):
    '''
    special_function_call : MEAN LPAREN call_params0 RPAREN
                     | MEDIAN LPAREN call_params0 RPAREN
                     | MODE LPAREN call_params0 RPAREN
                     | STD LPAREN call_params0 RPAREN
                     | KURTOSIS LPAREN call_params0 RPAREN
                     | PLOT LPAREN call_params0 RPAREN
                     | DPLOT LPAREN call_params0 RPAREN
                     | VARIANCE LPAREN call_params0 RPAREN
                     | SIMMETRY LPAREN call_params0 RPAREN
                     | CORRELATION LPAREN call_params0 RPAREN
                     | DFREAD LPAREN CONST_TEXT RPAREN
                     | HOMERO
                     | MARGE
    '''

def p_hyper_expression(p):
    '''
    hyper_expression : hyper_expression AND hyper_expression  
                     | hyper_expression OR hyper_expression
                     | super_expression
    '''

def p_super_expression(p):
    '''
    super_expression : super_expression LTHAN super_expression  
                     | super_expression GTHAN super_expression
                     | super_expression EQUAL super_expression
                     | super_expression DIFFERENT super_expression
                     | expression
    '''

def p_expression(p):
    '''
    expression : expression ADD expression  
               | expression SUB expression
               | term
    '''

def p_term(p):
    '''
    term : term MUL term
         | term DIV term
         | factor
    '''

def p_factor(p):
    '''
    factor : ID
           | array_access
           | matrix_access
           | LPAREN expression RPAREN
           | CONST_INT
           | CONST_FLOAT
           | function_call
           | special_function_call
    '''

def p_array_access(p):
    '''
    array_access : ID LSQBRACKET expression RSQBRACKET
    '''

def p_matrix_access(p):
    '''
    matrix_access : ID LSQBRACKET expression RSQBRACKET LSQBRACKET expression RSQBRACKET
    '''

def p_type(p):
    '''
    type : INT
         | FLOAT
    '''
    p[0] = p[1]

def p_empty(p):
    '''
    empty :
    '''
    pass

def p_error(p):
    if p == None:
        token = "end of file"
    else:
        token = f"{p.type}({p.value}) on line {p.lineno}"

    print(f"Syntax error: Unexpected {token}")

class Error(Exception):
    """Base class for other exceptions"""
    pass

if __name__ == '__main__':
    if len(sys.argv) > 1:

        parser = yacc.yacc()
        code = sys.argv[1]
        
        if ".spk" not in code:
            raise Error("File extension not valid")

        try:

            _file = open(code, 'r')
            source = _file.read()
            _file.close()
            lexer.input(source)

            #for lexem in lexer:
            #    print(lexem)

            lexer.lineno = 1
            if parser.parse(source) == 1:
                print("ROUTINE END")

        except EOFError:
            print(EOFError)

    else:
        print('A file must be provided as argument.')