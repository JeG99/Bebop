class Error(Exception):
    """Base class for other exceptions"""
    pass


def p_error(p, cause="bad_syntax", **args):
    if cause == "bad_extension":
        raise Error("File extension not valid")
    elif cause == "bad_syntax":
        if p == None:
            token = "EOF"
        else:
            token = f"<{p.value}>"
        raise Error(f"Syntax error: Unexpected {token} on line {p.lineno}")
    elif cause == "variable_declaration":
        print(args)
        raise Error(
            f"Semantic error: Variable <{args['args'][0]}> already declared as type <{args['args'][1]}>")
    elif cause == "type_missmatch":
        pass
