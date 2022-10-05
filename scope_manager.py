import json


class scope_manager():

    def __init__(self, error_handler):
        self.proc_dir = {}
        self.curr_scope = ""
        self.error_func = error_handler

    def context_change(self, context: str):
        self.proc_dir[context] = {"var_table": {}}
        self.curr_scope = context

    def store_variable(self, yacc_production, var_type: str):
        if yacc_production[1] in list(self.proc_dir[self.curr_scope]["var_table"]):
            self.error_func(yacc_production, "variable_declaration", args=(
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

    def dump_proc_dir(self):
        print(json.dumps(self.proc_dir, indent=4))
