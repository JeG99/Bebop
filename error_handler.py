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
        raise Error(f"Semantic error: Operator <{args['args'][0]}> cannot handle <{args['args'][1][0]}: {args['args'][1][1]}> and <{args['args'][2][0]}: {args['args'][2][1]}> (type mismatch)")
