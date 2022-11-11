import math

from semantic_cube import semantic_cube
from error_handler import raise_error


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
        self.quadruples = []

    def fill_main_jump(self) -> None:
        self.quadruples[0][3] = self.instruction_counter

    def push_operand(self, operand: str, type: str) -> None:
        self.operand_stack.append(operand)
        self.type_stack.append(type)

    def push_operator(self, operator: str) -> None:
        self.operator_stack.append(operator)

    def check_top_operator(self) -> str:
        return self.operator_stack[-1]

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
        print("Operators stack:", self.operator_stack)
        print("Operands stack:", self.operand_stack)
        print("Types stack:", self.type_stack)
        print("Jumps stack:", self.jump_stack)
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
        self.quadruples.append(["end", None, None, None])

    def produce_quadruple(self, level: str) -> None:
        if level == "gosub":
            ops = ["gosub"]
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
            elif level == "param":
                operand1 = self.sm_instance.get_operand_virtual_direction(
                    self.pop_operand())
                self.sm_instance.validate_param_type(operand1[1])
                self.quadruples.append(
                    [operator, operand1[0], None, operator + "$" + str(self.sm_instance.get_call_param_count())])
            elif level == "era":
                size = self.pop_operand()
                self.quadruples.append([operator, None, None, size[0]])
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
            # ! THIS WILL BE EASIER TO DEBUG/TEST WHEN THE VM IS READY
            elif level == "return":
                op1 = self.pop_operand()
                # self.push_operand(self.sm_instance.temp_augment(op1[1]))
                op2 = self.pop_operand()
                operand1 = self.sm_instance.get_operand_virtual_direction(op1)
                operand2 = self.sm_instance.get_operand_virtual_direction(op2)
                # res_type = self.sc_instance.type_match(
                    # operator, operand1[1], operand2[1])
                # if res_type != "ERR":
                # temporal = self.sm_instance.temp_augment(operand1[1])
                self.quadruples.append(
                    [operator, operand2[0], None, operand1[0]])
                # self.push_operand(temporal, operand1[1])
                # else:
                #     raise_error(None, "type_mismatch", args=(
                #         operator, operand1, operand2))
            else:
                op1, op2 = self.pop_operand(), self.pop_operand()
                operand1 = self.sm_instance.get_operand_virtual_direction(op1)
                operand2 = self.sm_instance.get_operand_virtual_direction(op2)
                res_type = self.sc_instance.type_match(
                    operator, operand1[1], operand2[1])
                if res_type != "ERR":
                    temporal = self.sm_instance.temp_augment(res_type)
                    self.quadruples.append(
                        [operator, operand2[0], operand1[0], temporal])
                    self.push_operand(temporal, res_type)
                else:
                    raise_error(None, "type_mismatch", args=(
                        operator, operand1, operand2))
            self.instruction_counter += 1
