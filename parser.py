import ply.yacc as yacc
from lexer import lexer, tokens
import sys

from scope_manager import scope_manager
from stack_manager import stack_manager
from error_handler import raise_error

scope_manager = scope_manager(raise_error)
stack_manager = stack_manager()


def p_routine(p) -> None:
    '''
    routine : ROUTINE ID SEMICOLON GLOBALS COLON global_scope_init var_declarations PROCEDURES COLON function_declarations BEGIN COLON LSQBRACKET LOCALS COLON local_scope_init var_declarations INSTRUCTIONS COLON statements RSQBRACKET
    '''
    p[0] = 1
    scope_manager.dump_proc_dir()


def p_global_scope_init(p) -> None:
    '''
    global_scope_init :
    '''
    scope_manager.context_change("global")


def p_local_scope_init(p) -> None:
    '''
    local_scope_init : 
    '''
    scope_manager.context_change("local")


def p_var_declarations(p) -> None:
    '''
    var_declarations : VAR simple_declaration var_declarations
                     | VAR array_declaration var_declarations
                     | VAR matrix_declaration var_declarations
                     | empty
    '''


def p_simple_declaration(p) -> None:
    '''
    simple_declaration : ID COLON var_type SEMICOLON 
    '''
    scope_manager.store_variable(p, "simple")


def p_array_declaration(p) -> None:
    '''
    array_declaration : ID LSQBRACKET CONST_INT RSQBRACKET COLON type SEMICOLON 
    '''
    scope_manager.store_variable(p, "array")


def p_matrix_declaration(p) -> None:
    '''
    matrix_declaration : ID LSQBRACKET CONST_INT RSQBRACKET LSQBRACKET CONST_INT RSQBRACKET COLON type SEMICOLON
    '''
    scope_manager.store_variable(p, "matrix")


def p_var_type(p) -> None:
    '''
    var_type : type
             | DF
    '''
    p[0] = p[1]


def p_function_declarations(p) -> None:
    '''
    function_declarations : PROC ID proc_scope_init LPAREN params0 RPAREN COLON func_type LBRACKET LOCALS COLON var_declarations INSTRUCTIONS COLON statements RBRACKET function_declarations
                          | PROC ID proc_scope_init LPAREN params0 RPAREN COLON func_type LBRACKET LOCALS COLON var_declarations INSTRUCTIONS COLON statements return SEMICOLON RBRACKET function_declarations
                          | empty
    '''


def p_proc_scope_init(p) -> None:
    '''
    proc_scope_init : 
    '''
    scope_manager.context_change(p[-1])


def p_return(p) -> None:
    '''
    return : RETURN expression
    '''


def p_func_type(p) -> None:
    '''
    func_type : type
              | VOID
    '''


def p_params0(p) -> None:
    '''
    params0 : param params1
            | empty
    '''


def p_params1(p) -> None:
    '''
    params1 : COMMA param params1
            | empty
    '''


def p_param(p) -> None:
    '''
    param : ID COLON type
    '''
    scope_manager.store_variable(p, "simple")


def p_statements(p) -> None:
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


def p_write(p) -> None:
    '''
    write : WRITE write_params0
    '''


def p_write_params0(p) -> None:
    '''
    write_params0 : expression write_params1
                  | CONST_TEXT write_params1
    '''


def p_write_params1(p) -> None:
    '''
    write_params1 : COMMA expression write_params1
                  | COMMA CONST_TEXT write_params1
                  | empty
    '''


def p_read(p) -> None:
    '''
    read : READ ID
    '''


def p_var_assignment(p) -> None:
    '''
    var_assignment : simple_assignment
                   | array_assignment
                   | matrix_assignment
    '''


def p_simple_assignment(p) -> None:
    '''
    simple_assignment : ID ASSIGN expression
    '''


def p_array_assignment(p) -> None:
    '''
    array_assignment : ID LSQBRACKET expression RSQBRACKET ASSIGN expression
    '''


def p_matrix_assignment(p) -> None:
    '''
    matrix_assignment : ID LSQBRACKET expression RSQBRACKET LSQBRACKET expression RSQBRACKET ASSIGN expression
    '''


def p_condition(p) -> None:
    '''
    condition : IF LPAREN hyper_expression RPAREN LBRACKET statements RBRACKET
              | IF LPAREN hyper_expression RPAREN LBRACKET statements RBRACKET ELSE LBRACKET statements RBRACKET    
    '''


def p_loop(p) -> None:
    '''
    loop : REPEAT LPAREN hyper_expression RPAREN LBRACKET statements RBRACKET
    '''


def p_function_call(p) -> None:
    '''
    function_call : ID LPAREN call_params0 RPAREN 
    '''


def p_call_params0(p) -> None:
    '''
    call_params0 : expression call_params1
                 | empty
    '''


def p_call_params1(p) -> None:
    '''
    call_params1 : COMMA expression call_params1
                 | empty
    '''


def p_special_function_call(p) -> None:
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


def p_hyper_expression(p) -> None:
    '''
    hyper_expression : hyper_expression AND hyper_expression  
                     | hyper_expression OR hyper_expression
                     | super_expression
    '''


def p_super_expression(p) -> None:
    '''
    super_expression : super_expression LTHAN super_expression  
                     | super_expression GTHAN super_expression
                     | super_expression EQUAL super_expression
                     | super_expression DIFFERENT super_expression
                     | expression
    '''


def p_expression(p) -> None:
    '''
    expression : expression ADD expression  
               | expression SUB expression
               | term
    '''


def p_term(p) -> None:
    '''
    term : term MUL term
         | term DIV term
         | factor
    '''


def p_factor(p) -> None:
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


def p_array_access(p) -> None:
    '''
    array_access : ID LSQBRACKET expression RSQBRACKET
    '''


def p_matrix_access(p) -> None:
    '''
    matrix_access : ID LSQBRACKET expression RSQBRACKET LSQBRACKET expression RSQBRACKET
    '''


def p_type(p) -> None:
    '''
    type : INT
         | FLOAT
    '''
    p[0] = p[1]


def p_empty(p) -> None:
    '''
    empty : 
    '''
    pass


if __name__ == "__main__":
    if len(sys.argv) > 1:

        parser = yacc.yacc()
        code = sys.argv[1]

        if "spk" != code.split(".")[-1]:
            raise_error(p=None, cause="bad_extension")

        try:

            _file = open(code, "r")
            source = _file.read()
            _file.close()
            lexer.input(source)

            # for lexem in lexer:
            #    print(lexem)

            lexer.lineno = 1
            if parser.parse(source) == 1:
                print("ROUTINE END")

        except EOFError:
            print(EOFError)

    else:
        print("A file must be provided as argument.")
