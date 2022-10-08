import json

from error_handler import raise_error


class scope_manager():

    def __init__(self) -> None:
        # Global addresses
        self.gi = 0
        self.gf = 1000
        # Local Addresses
        self.li = 2000
        self.lf = 3000
        # Temporal Addresses
        self.ti = 4000
        self.tf = 5000
        self.tb = 6000
        # Constant Addresses
        self.ci = 7000
        self.cf = 8000
        # Pointer Address
        self.tp = 9000

        self.constants_table = {}
        self.proc_dir = {}
        self.curr_scope = ""

    def push_constant(self, const: str, type: str) -> None:
        if const not in self.constants_table:
            self.constants_table[const] = self.ci * \
                (type == "int") + self.cf * (type == "float")
            self.ci += 1 * type == "int"
            self.cf += 1 * type == "float"

    def context_change(self, context: str) -> None:
        self.proc_dir[context] = {"var_table": {}}
        if context not in ["global", "local"]:
            self.proc_dir[context]["param_table"] = {}
            self.proc_dir[context]["param_count"] = 0
            self.proc_dir[context]["li"] = 0
            self.proc_dir[context]["lf"] = 0
            self.proc_dir[context]["ti"] = 0
            self.proc_dir[context]["tf"] = 0
            self.proc_dir[context]["tb"] = 0
        self.curr_scope = context
        self.li = 2000
        self.lf = 3000

    def set_return_type(self, return_type: str) -> None:
        self.proc_dir[self.curr_scope]["return_type"] = return_type

    def store_variable(self, yacc_production, var_kind: str, is_param: bool) -> None:
        if yacc_production[1] in list(self.proc_dir[self.curr_scope]["var_table"]):
            raise_error(yacc_production, "variable_declaration", args=(
                yacc_production[1], self.proc_dir[self.curr_scope]["var_table"][yacc_production[1]]["type"]))
        else:
            if var_kind == "simple":
                var_body = {
                    "type": yacc_production[3],
                    "indexed": False
                }
                if self.curr_scope not in ["global", "local"]:
                    self.proc_dir[self.curr_scope]["li"] += 1 * \
                        yacc_production[3] == "int"
                    self.proc_dir[self.curr_scope]["lf"] += 1 * \
                        yacc_production[3] == "float"
            if (var_kind == "array"):
                var_body = {
                    "type": yacc_production[6],
                    "indexed": True,
                    "dimensionality": 1,
                    "size": yacc_production[3]
                }
            elif (var_kind == "matrix"):
                var_body = {
                    "type": yacc_production[9],
                    "indexed": True,
                    "dimensionality": 2,
                    "rows": yacc_production[3],
                    "columns": yacc_production[6]
                }
            var_body["virtual_direction"] = (self.curr_scope == "global") * (self.gi * (var_body["type"] == "int") + self.gf * (var_body["type"] == "float")) + (
                self.curr_scope != "global") * (self.li * (var_body["type"] == "int") + self.lf * (var_body["type"] == "float"))
            self.gi += 1 * \
                var_body["type"] == "int" and self.curr_scope == "global"
            self.gf += 1 * \
                var_body["type"] == "float" and self.curr_scope == "global"
            self.li += 1 * \
                var_body["type"] == "int" and self.curr_scope != "global"
            self.lf += 1 * \
                var_body["type"] == "float" and self.curr_scope != "global"
            self.proc_dir[self.curr_scope]["var_table"][yacc_production[1]] = var_body
            if is_param:
                self.proc_dir[self.curr_scope]["param_count"] += 1
                self.proc_dir[self.curr_scope]["param_table"][yacc_production[1]] = var_body

    def store_proc_ip(self, ip: int) -> None:
        self.proc_dir[self.curr_scope]["initial_instruction_pointer"] = ip

    def check_function_definition(self, function_name: str) -> None:
        if function_name in self.proc_dir:
            raise_error(None, "function_declaration", args=(function_name))

    def check_function_call(self, function_name: str) -> None:
        if function_name not in self.proc_dir:
            raise_error(None, "undefined_function", args=(function_name))

    def temp_augment(self, temp_type: int) -> int:
        if self.curr_scope not in ["global", "local"]:
            self.proc_dir[self.curr_scope]["ti"] += 1 * temp_type == "int"
            self.proc_dir[self.curr_scope]["tf"] += 1 * temp_type == "float"
            self.proc_dir[self.curr_scope]["tb"] += 1 * temp_type == "bool"
        self.ti += 1 * temp_type == "int"
        self.tf += 1 * temp_type == "float"
        self.tb += 1 * temp_type == "bool"
        return self.ti * (temp_type == "int") + self.tf * (temp_type == "float") + self.tb * (temp_type == "bool")

    def get_operand_virtual_direction(self, operand: tuple) -> tuple:
        if operand[0] in self.constants_table:
            return self.constants_table[operand[0]], operand[1]
        elif operand[0] in self.proc_dir[self.curr_scope]["var_table"]:
            return self.proc_dir[self.curr_scope]["var_table"][operand[0]]["virtual_direction"], operand[1]
        elif type(operand[0]) == int:
            return operand

    def get_var_type(self, id: str) -> str:
        if id not in list(self.proc_dir[self.curr_scope]["var_table"]):
            raise_error(None, "undeclared_variable",
                        args=(id, self.curr_scope))
        else:
            return self.proc_dir[self.curr_scope]["var_table"][id]["type"]

    def dump_proc_dir(self) -> None:
        print("Constants table:", json.dumps(self.constants_table, indent=4))
        print("Procedures table:", json.dumps(self.proc_dir, indent=4))
