class Error(Exception):
    """Base class for other exceptions"""
    pass


def raise_error(p, cause="bad_syntax", **args) -> None:
    if cause == "bad_extension":
        raise Error("File extension not valid")
    elif cause == "bad_syntax":
        if p == None:
            token = "EOF"
        else:
            token = f"<{p.value}>"
        raise Error(f"Syntax error: Unexpected {token} on line {p.lineno}")
    elif cause == "variable_declaration":
        raise Error(
            f"Semantic error: Variable <{args['args'][0]}> already declared as type <{args['args'][1]}>")
    elif cause == "undeclared_variable":
        raise Error(
            f"Semantic error: Variable <{args['args'][0]}> not declared in current scope <{args['args'][1]}>")
    elif cause == "type_mismatch":
        if len(args["args"]) == 3:
            raise Error(
                f"Semantic error: Operator <{args['args'][0]}> cannot handle <{args['args'][1][0]}: {args['args'][1][1]}> and <{args['args'][2][0]}: {args['args'][2][1]}> (type mismatch)")
        elif len(args["args"]) == 2:
            raise Error(
                f"Semantic error: Statement <{args['args'][0]}> cannot be <{args['args'][1][0]}: {args['args'][1][1]}> (type mismatch)")
    elif cause == "function_declaration":
        raise Error(
            f"Semantic error: Function <{args['args']}> already declared")
    elif cause == "undefined_function":
        raise Error(f"Semantic error: Function <{args['args']}> is undefined")
    elif cause == "param_type_mismatch":
        raise Error(
            f"Semantic error: Parameter in <{args['args'][0]}> <{args['args'][1]}> expected <{args['args'][2]}> expression, found <{args['args'][3]}> instead")
    elif cause == "param_count":
        raise Error(
            f"Semantic error: Procedure <{args['args'][0]}> takes exactly <{args['args'][1]}> arguments, found <{args['args'][2]}> instead")
    elif cause == "non_indexed_var":
        raise Error(f"Semantic error: <{args['args'][0]}: {args['args'][1]}> is not an indexed variable")