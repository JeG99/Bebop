import json
from error_handler import raise_error


class scope_manager():

    def __init__(self) -> None:
                # Global addresses
        self.Gi = 0
        self.Gf = 1000
        # Local Addresses
        self.Li = 2000
        self.Lf = 3000
        # Temporal Addresses
        self.Ti = 4000
        self.Tf = 5000
        self.Tb = 6000
        # Constant Addresses
        self.Ci = 7000
        self.Cf = 8000
        # Pointer Address
        self.Tp = 9000

        self.constants_table = {}
        self.proc_dir = {}
        self.curr_scope = ""

    def push_constant(self, const: str, type: str) -> None:
        if const not in self.constants_table:
            self.constants_table[const] = self.Ci * (type == "int") + self.Cf * (type == "float")
            self.Ci += 1 * type == "int"
            self.Cf += 1 * type == "float"

    def context_change(self, context: str) -> None:
        self.proc_dir[context] = {"var_table": {}}
        self.curr_scope = context
        self.Li = 2000
        self.Lf = 3000

    def store_variable(self, yacc_production, var_type: str) -> None:
        if yacc_production[1] in list(self.proc_dir[self.curr_scope]["var_table"]):
            raise_error(yacc_production, "variable_declaration", args=(
                yacc_production[1], self.proc_dir[self.curr_scope]["var_table"][yacc_production[1]]["type"]))
        else:
            if var_type == "simple":
                var_body = {
                    "type": yacc_production[3],
                    "indexed": False
                }
            if (var_type == "array"):
                var_body = {
                    "type": yacc_production[6],
                    "indexed": True,
                    "dimensionality": 1,
                    "size": yacc_production[3]
                }
            elif (var_type == "matrix"):
                var_body = {
                    "type": yacc_production[9],
                    "indexed": True,
                    "dimensionality": 2,
                    "rows": yacc_production[3],
                    "columns": yacc_production[6]
                }
            var_body["virtual_direction"] = (self.curr_scope == "global") * (self.Gi * (var_body["type"] == "int") + self.Gf * (var_body["type"] == "float")) + (self.curr_scope != "global") * (self.Li * (var_body["type"] == "int") + self.Lf * (var_body["type"] == "float"))
            self.Gi += 1 * var_body["type"] == "int" and self.curr_scope == "global"
            self.Gf += 1 * var_body["type"] == "float" and self.curr_scope == "global"
            self.Li += 1 * var_body["type"] == "int" and self.curr_scope != "global"
            self.Lf += 1 * var_body["type"] == "float" and self.curr_scope != "global"
            self.proc_dir[self.curr_scope]["var_table"][yacc_production[1]] = var_body

    def get_var_type(self, id: str) -> str:
        if id not in list(self.proc_dir[self.curr_scope]["var_table"]):
            raise_error(None, "undeclared_variable",
                        args=(id, self.curr_scope))
        else:
            return self.proc_dir[self.curr_scope]["var_table"][id]["type"]

    def dump_proc_dir(self) -> None:
        print("Constants table:", json.dumps(self.constants_table, indent=4))
        print("Procedures table:", json.dumps(self.proc_dir, indent=4))
