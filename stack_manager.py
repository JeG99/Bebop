import math

from semantic_cube import semantic_cube
from bebop_error_handler import raise_error


class stack_manager():
    def __init__(self, scope_manager) -> None:
        self.temp_counter = 0
        self.instruction_counter = 0
        self.sc_instance = semantic_cube()
        self.sm_instance = scope_manager
        self.operator_stack = []
        self.operand_stack = []
        self.type_stack = []
        self.jump_stack = []
        self.era_jump_stacks = {}
        self.dim_stack = []
        self.quadruples = []
        self.dim = 1

    def push_era_jump(self, call: str, jump: int) -> None:
        if call not in self.era_jump_stacks.keys():
            self.era_jump_stacks[call] = []
        self.era_jump_stacks[call].append(jump)

    def fill_main_jump(self) -> None:
        self.quadruples[0][3] = self.instruction_counter

    def push_operand(self, operand: str, type: str) -> None:
        self.operand_stack.append(operand)
        self.type_stack.append(type)

    def push_operator(self, operator: str) -> None:
        self.operator_stack.append(operator)

    def check_top_operator(self) -> str:
        return self.operator_stack[-1]

    def check_top_operand(self) -> tuple:
        return self.operand_stack[-1], self.type_stack[-1]

    def pop_operand(self) -> tuple:
        return self.operand_stack.pop(), self.type_stack.pop()

    def pop_operator(self) -> str:
        return self.operator_stack.pop()

    def push_jump(self, instruction_pointer: int) -> None:
        self.jump_stack.append(instruction_pointer)

    def pop_jump(self) -> int:
        return self.jump_stack.pop()

    def get_current_istruction_pointer(self) -> int:
        return self.instruction_counter

    def assign_quadruple_jump(self, quad: int, jump: int) -> None:
        self.quadruples[quad][3] = jump

    def dump_stacks(self) -> None:
        # print("Operators stack:", self.operator_stack)
        # print("Operands stack:", self.operand_stack)
        # print("Types stack:", self.type_stack)
        # print("Jumps stack:", self.jump_stack)
        # print("Dimension stack:", self.dim_stack)
        # print("ERA jumps stacks:", self.era_jump_stacks)
        print("Quadruples:")
        s = [["----" if e == None else str(e) for e in row]
             for row in self.quadruples]
        lens = [max(map(len, col)) for col in zip(*s)]
        fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
        quads = dict(zip(['{:{width}d}'.format(i, width=int(
            math.log10(len(s)))+1) + " ==> " for i in range(len(s))], s))
        table = [ip + fmt.format(*row) for ip, row in quads.items()]
        print('\n'.join(table))

    def start_instructions(self) -> None:
        self.quadruples.append(["goto", None, None, None])
        self.instruction_counter += 1

    def finish_instructions(self) -> None:
        # update era quads
        for id, era_jump_stack in self.era_jump_stacks.items():
            era_jump = 0
            while len(era_jump_stack) > 0:
                quad = era_jump_stack.pop()
                self.assign_quadruple_jump(quad, self.sm_instance.get_function_size(id))
                era_jump += 1
        # append last quad
        self.quadruples.append(["end", None, None, None])

    def verify_indexed_var(self, dims: int) -> None:
        var = self.check_top_operand()
        indexed = False
        if var[0] in self.sm_instance.proc_dir["global"]["var_table"]:
            indexed = self.sm_instance.proc_dir["global"]["var_table"][var[0]]["indexed"]
        elif var[0] in self.sm_instance.proc_dir[self.sm_instance.curr_scope]["var_table"]:
            indexed = self.sm_instance.proc_dir[self.sm_instance.curr_scope]["var_table"][var[0]]["indexed"]
        if not indexed:
            raise_error(None, "non_indexed_var", args=(var))

    def set_dim(self, dim: int) -> None:
        self.dim = dim

    def push_dim(self) -> None:
        id = self.check_top_operand()[0]

        if self.dim == 2:
            temp = self.pop_operand()
            id = self.pop_operand()[0]
            self.push_operand(temp[0], temp[1])

        curr_dim = ()
        curr_scope = "global" if id in self.sm_instance.proc_dir["global"]["var_table"] else self.sm_instance.curr_scope

        if self.sm_instance.proc_dir[curr_scope]["var_table"][id]["dimensionality"] == 1:
            curr_dim = (
                id,
                self.dim,
                self.sm_instance.proc_dir[curr_scope]["var_table"][id]["lim_sup1"],
                self.sm_instance.proc_dir[curr_scope]["var_table"][id]["virtual_direction"],
                self.sm_instance.proc_dir[curr_scope]["var_table"][id]["dimensionality"]
            )
        elif self.sm_instance.proc_dir[curr_scope]["var_table"][id]["dimensionality"] == 2:
            curr_dim = (
                id,
                self.dim,
                self.sm_instance.proc_dir[curr_scope]["var_table"][id]["lim_sup1"],
                self.sm_instance.proc_dir[curr_scope]["var_table"][id]["lim_sup2"],
                self.sm_instance.proc_dir[curr_scope]["var_table"][id]["virtual_direction"],
                self.sm_instance.proc_dir[curr_scope]["var_table"][id]["dimensionality"]
            )
        
        self.dim_stack.append(curr_dim)

    def pop_dim(self) -> tuple:
        return self.dim_stack.pop()

    def check_dim(self) -> tuple:
        return self.dim_stack[-1]

    def produce_quadruple(self, level: str) -> None:
        if level == "gosub":
            ops = ["gosub"]
        elif level == "verify":
            ops = ["verify"]
        elif level == "array_access":
            ops = ["+"]
        elif level == "matrix_access_dim1":
            ops = ["*"]
        elif level == "matrix_access_dim2":
            ops = ["+"]
        elif level == "param":
            ops = ["param"]
        elif level == "era":
            ops = ["era"]
        elif level == "while_goto":
            ops = ["while_goto"]
        elif level == "gotof":
            ops = ["gotof"]
        elif level == "endfunc":
            ops = ["endfunc"]
        elif level == "goto":
            ops = ["goto"]
        elif level == "read":
            ops = ["read"]
        elif level == "write":
            ops = ["write"]
        elif level == "return":
            ops = ["return"]
        elif level == "simple_assignment":
            ops = ["="]
        elif level == "hyperexp":
            ops = ["and", "or"]
        elif level == "superexp":
            ops = [">", "<", "==", "<>"]
        elif level == "exp":
            ops = ["+", "-"]
        elif level == "term":
            ops = ["*", "/"]
        if self.check_top_operator() in ops:
            operator = self.pop_operator()
            if level == "gosub":
                procedure = self.sm_instance.get_curr_procedure_call()
                self.quadruples.append(
                    [operator, procedure[0], None, procedure[2]])

            elif level == "verify":
                s1 = self.check_top_operand()
                dim = self.check_dim()
                self.sm_instance.push_constant(str(0), "int")
                self.push_operand(str(0), "int")
                self.sm_instance.push_constant(str(dim[2]), "int")
                self.push_operand(str(dim[2]), "int")
                op2 = self.pop_operand()
                op1 = self.pop_operand()
                
                if type(s1) == int and (s1 >= 9000 or (s1 >= 4000 and s1 < 6000)):
                    s1_dir = (s1, "pointer")
                else:
                    s1_dir = self.sm_instance.get_operand_virtual_direction(s1)
                
                operand1 = self.sm_instance.get_operand_virtual_direction(op1)
                operand2 = self.sm_instance.get_operand_virtual_direction(op2)
                self.quadruples.append([operator, s1_dir[0], operand1[0], operand2[0]])

            elif level == "array_access":
                s1 = self.pop_operand()[0]
                
                if type(s1) == int and (s1 >= 9000 or (s1 >= 4000 and s1 < 6000)):
                    s1_dir = (s1, "pointer")
                else:
                    s1_dir = self.sm_instance.get_operand_virtual_direction((str(s1), "int"))
                
                dim = self.pop_dim()
                self.sm_instance.push_constant(str(dim[3]), "int")
                base_dir_dir = self.sm_instance.get_operand_virtual_direction((str(dim[3]), "int"))
                temporal = self.sm_instance.temp_augment("pointer")
                self.quadruples.append([
                    operator, 
                    s1_dir[0], 
                    base_dir_dir[0], 
                    temporal])
                self.pop_operand()
                self.push_operand(temporal, "int")    
                self.pop_operator()    

            elif level == "matrix_access_dim1":
                s1 = self.pop_operand()[0]

                if type(s1) == int and (s1 >= 9000 or (s1 >= 4000 and s1 < 6000)):
                    s1_dir = (s1, "pointer")
                else:
                    s1_dir = self.sm_instance.get_operand_virtual_direction((str(s1), "int"))
                
                dim = self.pop_dim()
                self.sm_instance.push_constant(str(dim[3]), "int")
                m1_dir = self.sm_instance.get_operand_virtual_direction((str(dim[3]), "int"))

                temporal = self.sm_instance.temp_augment("int")
                self.quadruples.append([
                    operator,
                    s1_dir[0],
                    m1_dir[0],
                    temporal
                ])
                self.push_operand(temporal, "int")
                self.pop_operator()

            elif level == "matrix_access_dim2":
                s2 = self.pop_operand()[0]

                if type(s2) == int and (s2 >= 9000 or (s2 >= 4000 and s2 < 6000)):
                    s2_dir = (s2, "pointer")
                else:   
                    s2_dir = self.sm_instance.get_operand_virtual_direction((str(s2), "int"))
                
                dim = self.pop_dim()
                self.sm_instance.push_constant(str(dim[2]), "int")
                
                temp = self.pop_operand()

                temporal = self.sm_instance.temp_augment("int")
                self.quadruples.append([
                    operator,
                    temp[0],
                    s2_dir[0],
                    temporal
                ])
                self.push_operand(temporal, "int")
                
                # ADD DIRBASE
                self.sm_instance.push_constant(str(dim[4]), "int")
                base_dir_dir = self.sm_instance.get_operand_virtual_direction((str(dim[4]), "int"))
                temp = self.pop_operand()
                temporal = self.sm_instance.temp_augment("pointer")
                self.quadruples.append([
                    "+",
                    temp[0],
                    base_dir_dir[0],
                    temporal
                ])
                self.push_operand(temporal, "int")
                self.pop_operator()
                self.instruction_counter += 1

            elif level == "param":
                operand1 = self.sm_instance.get_operand_virtual_direction(
                    self.pop_operand())
                self.sm_instance.validate_param_type(operand1[1])
                self.quadruples.append(
                    [operator, operand1[0], None, operator + "$" + str(self.sm_instance.get_call_param_count())])
            
            elif level == "era":
                procedure = self.sm_instance.get_curr_procedure_call()
                size = self.pop_operand()
                self.quadruples.append([operator, procedure[0], None, size[0]])
            
            elif level == "while_goto":
                return_jump = self.pop_jump()
                self.quadruples.append([operator, return_jump, None, None])
            
            elif level == "endfunc":
                self.quadruples.append([operator, None, None, None])
            
            elif level == "goto":
                self.quadruples.append([operator, None, None, None])
            
            elif level == "gotof":
                operand1 = self.pop_operand()
                if operand1[1] == "bool":
                    self.quadruples.append([operator, operand1[0], None, None])
                else:
                    raise_error(None, "type_mismatch", args=("cond", operand1))
            
            elif level == "simple_assignment":
                op1 = self.pop_operand(), self.pop_operand()
                operand1 = self.sm_instance.get_operand_virtual_direction(
                    op1[0])
                operand2 = self.sm_instance.get_operand_virtual_direction(
                    op1[1])
                self.quadruples.append(
                    [operator, operand1[0], None, operand2[0]])
            
            elif level == "read":
                operand1 = self.sm_instance.get_operand_virtual_direction(
                    self.pop_operand())
                self.quadruples.append([operator, None, None, operand1[0]])
            
            elif level == "write":
                operand1 = self.pop_operand()
                if operand1[1] != "text":
                    operand1 = self.sm_instance.get_operand_virtual_direction(
                        operand1)
                self.quadruples.append([operator, None, None, operand1[0]])
            
            elif level == "return":
                op1 = self.pop_operand()
                op2 = self.pop_operand()
                operand1 = self.sm_instance.get_operand_virtual_direction(op1)
                operand2 = self.sm_instance.get_operand_virtual_direction(op2)
                # TODO: Return type typematching
                self.quadruples.append([operator, operand2[0], None, operand1[0]])
            
            else:
                op1, op2 = self.pop_operand(), self.pop_operand()
                operand1 = self.sm_instance.get_operand_virtual_direction(op1)
                operand2 = self.sm_instance.get_operand_virtual_direction(op2)
                if operand1[1] != "pointer" and operand2[1] != "pointer":
                    res_type = self.sc_instance.type_match(operator, operand1[1], operand2[1])
                else:
                    res_type = "pointer"
                if res_type != "ERR":
                    temporal = self.sm_instance.temp_augment(res_type)
                    self.quadruples.append(
                        [operator, operand2[0], operand1[0], temporal])
                    self.push_operand(temporal, res_type)
                else:
                    raise_error(None, "type_mismatch", args=(
                        operator, operand1, operand2))
            
            self.instruction_counter += 1
