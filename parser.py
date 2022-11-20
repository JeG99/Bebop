import ply.yacc as yacc
import sys

from lexer import lexer, tokens
from scope_manager import scope_manager
from stack_manager import stack_manager
from virtual_machine import virtual_machine
from bebop_error_handler import raise_error

scope_manager = scope_manager()
initial_dirs = scope_manager.get_initial_dirs()
stack_manager = stack_manager(scope_manager)
virtual_machine = virtual_machine()


def p_routine(p) -> None:
    '''
    routine : routine_init ID SEMICOLON global_scope_init global_vars_block instructions_block function_block BEGIN COLON LSQBRACKET local_scope_init local_vars_block fill_main_jump instructions_block RSQBRACKET
    '''
    p[0] = 1
    stack_manager.finish_instructions()
    # scope_manager.dump_proc_dir()
    stack_manager.dump_stacks()
    virtual_machine.mem_init(
        scope_manager.get_const_table(), scope_manager.get_proc_dir())
    virtual_machine.run(stack_manager.quadruples)


def p_routine_init(p) -> None:
    '''
    routine_init : ROUTINE
    '''
    stack_manager.start_instructions()


def p_fill_main_jump(p) -> None:
    '''
    fill_main_jump : 
    '''
    stack_manager.fill_main_jump()


def p_global_vars_block(p) -> None:
    '''
    global_vars_block : GLOBALS COLON var_declarations
                      | empty
    '''


def p_local_vars_block(p) -> None:
    '''
    local_vars_block : LOCALS COLON var_declarations
                     | empty
    '''


def p_instructions_block(p) -> None:
    '''
    instructions_block : INSTRUCTIONS COLON statements
                       | empty
    '''


def p_proc_instructions_block(p) -> None:
    '''
    proc_instructions_block : INSTRUCTIONS COLON proc_statements
                            | empty
    '''


def p_proc_statements(p) -> None:
    '''
    proc_statements : write SEMICOLON proc_statements
                    | read SEMICOLON proc_statements
                    | var_assignment SEMICOLON proc_statements
                    | proc_condition proc_statements
                    | proc_loop proc_statements
                    | function_call SEMICOLON proc_statements
                    | special_function_call SEMICOLON proc_statements
                    | return expression return_semicolon proc_statements
                    | empty
    '''


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
    scope_manager.store_variable(p, "simple", False)


def p_array_declaration(p) -> None:
    '''
    array_declaration : ID LSQBRACKET CONST_INT RSQBRACKET COLON type SEMICOLON 
    '''
    scope_manager.store_variable(p, "array", False)


def p_matrix_declaration(p) -> None:
    '''
    matrix_declaration : ID LSQBRACKET CONST_INT RSQBRACKET LSQBRACKET CONST_INT RSQBRACKET COLON type SEMICOLON
    '''
    scope_manager.store_variable(p, "matrix", False)


def p_var_type(p) -> None:
    '''
    var_type : type
             | DF
    '''
    p[0] = p[1]


def p_function_block(p) -> None:
    '''
    function_block : PROCEDURES COLON function_declarations
                   | empty
    '''


def p_function_declarations(p) -> None:
    '''
    function_declarations : PROC ID proc_scope_init LPAREN params0 RPAREN COLON VOID set_return_type LBRACKET local_vars_block store_curr_ip instructions_block function_rbracket function_declarations
                          | PROC ID proc_scope_init LPAREN params0 RPAREN COLON func_type set_return_type LBRACKET local_vars_block store_curr_ip proc_instructions_block RBRACKET function_declarations
                          | empty
    '''


def p_function_rbracket(p) -> None:
    '''
    function_rbracket : RBRACKET
    '''
    stack_manager.push_operator("endfunc")
    stack_manager.produce_quadruple("endfunc")
    scope_manager.reset_curr_procedure_call()


def p_proc_scope_init(p) -> None:
    '''
    proc_scope_init : 
    '''
    scope_manager.check_function_definition(p[-1])
    scope_manager.context_change(p[-1])


def p_store_curr_ip(p) -> None:
    '''
    store_curr_ip : 
    '''
    scope_manager.store_proc_ip(stack_manager.get_current_istruction_pointer())


def p_set_return_type(p) -> None:
    '''
    set_return_type : 
    '''
    scope_manager.set_return_type(p[-1])
    scope_manager.define_return_global_var()


def p_return(p) -> None:
    '''
    return : RETURN
    '''
    stack_manager.push_operator("return")
    procedure = scope_manager.get_current_scope()
    stack_manager.push_operand(procedure[0], procedure[1])


def p_return_semicolon(p) -> None:
    '''
    return_semicolon : SEMICOLON
    '''
    stack_manager.produce_quadruple("return")
    stack_manager.push_operator("endfunc")
    stack_manager.produce_quadruple("endfunc")
    scope_manager.reset_curr_procedure_call()


def p_func_type(p) -> None:
    '''
    func_type : type
    '''
    p[0] = p[1]


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
    scope_manager.store_variable(p, "simple", True)


def p_statements(p) -> None:
    '''
    statements : write SEMICOLON statements
               | read SEMICOLON statements
               | var_assignment SEMICOLON statements
               | condition statements
               | loop statements
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
    write_params0 : write_operator expression produce_write_quad write_params1
                  | write_operator const_text produce_write_quad write_params1
    '''


def p_write_params1(p) -> None:
    '''
    write_params1 : COMMA write_operator expression produce_write_quad write_params1
                  | COMMA write_operator const_text produce_write_quad write_params1
                  | empty
    '''


def p_const_text(p) -> None:
    '''
    const_text : CONST_TEXT
    '''
    stack_manager.push_operand(p[1], "text")


def p_write_operator(p) -> None:
    '''
    write_operator : 
    '''
    stack_manager.push_operator("write")


def p_produce_write_quad(p) -> None:
    '''
    produce_write_quad : 
    '''
    stack_manager.produce_quadruple("write")


def p_read(p) -> None:
    '''
    read : READ push_operator identifier
    '''
    stack_manager.produce_quadruple("read")


def p_var_assignment(p) -> None:
    '''
    var_assignment : simple_assignment
                   | array_assignment
                   | matrix_assignment
    '''


def p_simple_assignment(p) -> None:
    '''
    simple_assignment : identifier ASSIGN push_operator expression
    '''
    stack_manager.produce_quadruple("simple_assignment")


def p_array_assignment(p) -> None:
    '''
    array_assignment : array_access ASSIGN push_operator expression
    '''
    stack_manager.produce_quadruple("simple_assignment")

def p_matrix_assignment(p) -> None:
    '''
    matrix_assignment : matrix_access ASSIGN push_operator expression
    '''
    stack_manager.produce_quadruple("simple_assignment")

def p_condition(p) -> None:
    '''
    condition : IF cond_lparen hyper_expression cond_rparen LBRACKET statements RBRACKET fill_pending_jump
              | IF cond_lparen hyper_expression cond_rparen LBRACKET statements RBRACKET else LBRACKET statements RBRACKET fill_pending_jump   
    '''

def p_proc_condition(p) -> None:
    '''
    proc_condition : IF cond_lparen hyper_expression cond_rparen LBRACKET proc_statements RBRACKET fill_pending_jump
                   | IF cond_lparen hyper_expression cond_rparen LBRACKET proc_statements RBRACKET else LBRACKET proc_statements RBRACKET fill_pending_jump   
    '''

def p_cond_lparen(p) -> None:
    '''
    cond_lparen : LPAREN
    '''
    stack_manager.push_operator("gotof")


def p_cond_rparen(p) -> None:
    '''
    cond_rparen : RPAREN
    '''
    stack_manager.produce_quadruple("gotof")
    stack_manager.push_jump(stack_manager.get_current_istruction_pointer() - 1)


def p_fill_pending_jump(p) -> None:
    '''
    fill_pending_jump : 
    '''
    stack_manager.assign_quadruple_jump(
        stack_manager.pop_jump(), stack_manager.get_current_istruction_pointer())


def p_else(p) -> None:
    '''
    else : ELSE
    '''
    stack_manager.push_operator("goto")
    stack_manager.produce_quadruple("goto")
    false = stack_manager.pop_jump()
    stack_manager.push_jump(stack_manager.get_current_istruction_pointer() - 1)
    stack_manager.assign_quadruple_jump(
        false, stack_manager.get_current_istruction_pointer())


def p_loop(p) -> None:
    '''
    loop : repeat cond_lparen hyper_expression cond_rparen LBRACKET statements RBRACKET fill_returning_jump
    '''

def p_proc_loop(p) -> None:
    '''
    proc_loop : repeat cond_lparen hyper_expression cond_rparen LBRACKET proc_statements RBRACKET fill_returning_jump
    '''

def p_repeat(p) -> None:
    '''
    repeat : REPEAT
    '''
    stack_manager.push_jump(stack_manager.get_current_istruction_pointer())


def p_fill_returning_jump(p) -> None:
    '''
    fill_returning_jump : 
    '''
    stack_manager.push_operator("while_goto")
    end_jump = stack_manager.pop_jump()
    stack_manager.produce_quadruple("while_goto")
    stack_manager.assign_quadruple_jump(
        end_jump, stack_manager.get_current_istruction_pointer())


def p_function_call(p) -> None:
    '''
    function_call : ID function_call_check function_call_lparen call_params0 function_call_rparen 
    '''


def p_function_call_check(p) -> None:
    '''
    function_call_check : 
    '''
    scope_manager.check_function_call(p[-1])
    scope_manager.set_curr_procedure_call(p[-1])
    stack_manager.push_era_jump(p[-1], stack_manager.get_current_istruction_pointer())
    stack_manager.push_operand(scope_manager.get_function_size(p[-1]), None)


def p_function_call_lparen(p):
    '''
    function_call_lparen : LPAREN
    '''
    stack_manager.push_operator("era")
    stack_manager.produce_quadruple("era")
    stack_manager.push_operator("(")


def p_function_call_rparen(p):
    '''
    function_call_rparen : RPAREN
    '''
    scope_manager.validate_call_param_count()
    stack_manager.push_operator("gosub")
    stack_manager.produce_quadruple("gosub")
    stack_manager.pop_operator()
    scope_manager.reset_call_param_count()


def p_call_params0(p) -> None:
    '''
    call_params0 : hyper_expression handle_call_param call_params1
                 | empty
    '''


def p_call_params1(p) -> None:
    '''
    call_params1 : COMMA hyper_expression handle_call_param call_params1
                 | empty
    '''


def p_handle_call_param(p) -> None:
    '''
    handle_call_param : 
    '''
    scope_manager.augment_call_param_count()
    stack_manager.push_operator("param")
    stack_manager.produce_quadruple("param")


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
    hyper_expression : hyper_expression AND push_operator hyper_expression
                     | hyper_expression OR push_operator hyper_expression
                     | super_expression produce_hyperexp_quad
    '''


def p_super_expression(p) -> None:
    '''
    super_expression : super_expression LTHAN push_operator super_expression
                     | super_expression GTHAN push_operator super_expression
                     | super_expression EQUAL push_operator super_expression
                     | super_expression DIFFERENT push_operator super_expression
                     | expression produce_superexp_quad
    '''


def p_expression(p) -> None:
    '''
    expression : expression ADD push_operator expression
               | expression SUB push_operator expression 
               | term produce_exp_quad
    '''


def p_term(p) -> None:
    '''
    term : term MUL push_operator term
         | term DIV push_operator term
         | factor produce_term_quad
    '''


def p_push_operator(p) -> None:
    '''
    push_operator : 
    '''
    stack_manager.push_operator(p[-1])


def p_produce_hyperexp_quad(p) -> None:
    '''
    produce_hyperexp_quad : 
    '''
    stack_manager.produce_quadruple("hyperexp")


def p_produce_superexp_quad(p) -> None:
    '''
    produce_superexp_quad : 
    '''
    stack_manager.produce_quadruple("superexp")


def p_produce_exp_quad(p) -> None:
    '''
    produce_exp_quad : 
    '''
    stack_manager.produce_quadruple("exp")


def p_produce_term_quad(p) -> None:
    '''
    produce_term_quad : 
    '''
    stack_manager.produce_quadruple("term")


def p_factor(p) -> None:
    '''
    factor : identifier
           | const_int
           | const_float
           | LPAREN push_cap expression RPAREN pop_cap
           | array_access
           | matrix_access
           | function_call
           | special_function_call
    '''


def p_identifier(p) -> None:
    '''
    identifier : ID
    '''
    stack_manager.push_operand(p[1], scope_manager.get_var_type(p[1]))


def p_const_int(p) -> None:
    '''
    const_int : CONST_INT
    '''
    scope_manager.push_constant(p[1], "int")
    stack_manager.push_operand(p[1], "int")


def p_const_float(p) -> None:
    '''
    const_float : CONST_FLOAT
    '''
    scope_manager.push_constant(p[1], "float")
    stack_manager.push_operand(p[1], "float")


def p_push_cap(p) -> None:
    '''
    push_cap : 
    '''
    stack_manager.push_operator('(')


def p_pop_cap(p) -> None:
    '''
    pop_cap : 
    '''
    stack_manager.pop_operator()


def p_array_access(p) -> None:
    '''
    array_access : identifier lsqbracket expression array_rsqbracket
    '''


def p_matrix_access(p) -> None:
     '''
     matrix_access : identifier lsqbracket expression matrix_rsqbracket_1 matrix_lsqbracket_2 expression matrix_rsqbracket_2
     '''


def p_lsqbracket(p) -> None:
    '''
    lsqbracket : LSQBRACKET
    '''
    stack_manager.verify_indexed_var(1)
    stack_manager.set_dim(1)
    stack_manager.push_dim()
    stack_manager.push_operator('(')


def p_array_rsqbracket(p) -> None:
    '''
    array_rsqbracket : RSQBRACKET
    '''
    stack_manager.push_operator("verify")
    stack_manager.produce_quadruple("verify")
    stack_manager.push_operator("+")
    stack_manager.produce_quadruple("array_access")

def p_matrix_rsqbracket_1(p) -> None:
    '''
    matrix_rsqbracket_1 : RSQBRACKET
    '''
    stack_manager.push_operator("verify")
    stack_manager.produce_quadruple("verify")
    stack_manager.push_operator("*")
    stack_manager.produce_quadruple("matrix_access_dim1")

def p_matrix_lsqbracket_2(p) -> None:
    '''
    matrix_lsqbracket_2 : LSQBRACKET
    '''
    stack_manager.set_dim(2)
    stack_manager.push_dim()
    stack_manager.push_operator('(')

def p_matrix_rsqbracket_2(p) -> None:
    '''
    matrix_rsqbracket_2 : RSQBRACKET
    '''
    stack_manager.push_operator("verify")
    stack_manager.produce_quadruple("verify")
    stack_manager.push_operator("+")
    stack_manager.produce_quadruple("matrix_access_dim2")

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


def p_error(p) -> None:
    raise_error(p)


if __name__ == "__main__":
    if len(sys.argv) > 1:

        parser = yacc.yacc()
        code = sys.argv[1]

        if "bbp" != code.split(".")[-1]:
            raise_error(p=None, cause="bad_extension")

        try:

            _file = open(code, "r")
            source = _file.read()
            _file.close()
            lexer.input(source)

            lexer.lineno = 1
            if parser.parse(source) == 1:
                print("ROUTINE END")

        except EOFError:
            print(EOFError)

    else:
        print("A file must be provided as argument.")
