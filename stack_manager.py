class stack_manager():
    def __init__(self) -> None:
        self.operator_stack = []
        self.operand_stack = []
        self.type_stack = []

    def push_operand(self, operand, type) -> None:
        self.operand_stack.append(operand)
        self.type_stack.append(type)

    def push_operator(self, operator) -> None:
        self.operator_stack.append(operator)

    def check_top_operator(self) -> str:
        return self.operator_stack[-1]

    def pop_operand(self) -> tuple:
        return self.operand_stackp.pop(), self.type_stack.pop()

    def pop_operator(self) -> str:
        return self.operator_stack.pop()

    def dump_stacks(self) -> None:
        print(self.operator_stack)
        print(self.operand_stack)
        print(self.type_stack)
