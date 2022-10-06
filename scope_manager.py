import json
from error_handler import raise_error


class scope_manager():

    def __init__(self) -> None:
        self.proc_dir = {}
        self.curr_scope = ""

    def context_change(self, context: str) -> None:
        self.proc_dir[context] = {"var_table": {}}
        self.curr_scope = context

    def store_variable(self, yacc_production, var_type: str) -> None:
        if yacc_production[1] in list(self.proc_dir[self.curr_scope]["var_table"]):
            raise_error(yacc_production, "variable_declaration", args=(
                yacc_production[1], self.proc_dir[self.curr_scope]["var_table"][yacc_production[1]]["type"]))

        var_body = {
            "type": yacc_production[3],
            "indexed": False
        }
        if (var_type == "array"):
            var_body["type"] = yacc_production[6]
            var_body["indexed"] = True
            var_body["dimensionality"] = 1
            var_body["size"] = yacc_production[3]
        elif (var_type == "matrix"):
            var_body["type"] = yacc_production[9]
            var_body["indexed"] = True
            var_body["dimensionality"] = 2
            var_body["rows"] = yacc_production[3]
            var_body["columns"] = yacc_production[6]
        self.proc_dir[self.curr_scope]["var_table"][yacc_production[1]] = var_body

    def get_var_type(self, id: str) -> str:
        if id not in list(self.proc_dir[self.curr_scope]["var_table"]):
            raise_error(None, "undeclared_variable",
                        args=(id, self.curr_scope))
        else:
            return self.proc_dir[self.curr_scope]["var_table"][id]["type"]

    def dump_proc_dir(self) -> None:
        print(json.dumps(self.proc_dir, indent=4))
