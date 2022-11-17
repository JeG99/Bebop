from bebop_error_handler import raise_error


class virtual_machine():
    def __init__(self):
        self.quadruples = {}
        self.const_table = {}
        self.proc_dir = {}
        self.mem = []
        self.curr_ip = 0
        self.call_stack = []

    def rel_dir(self, dir) -> int:
        return int(dir / 1000)

    def dir_translator(self, direction) -> tuple:
        return self.rel_dir(direction), direction - self.rel_dir(direction) * 1000

    def flatten_var_tables(self, proc_dir) -> list:
        dir_list = []
        # Flattening global vars
        for _, var_data in proc_dir["global"]["var_table"].items():
            dir = var_data["virtual_direction"]
            indexed = var_data["indexed"]
            if dir not in dir_list:
                if indexed:
                    if var_data["dimensionality"] == 1:
                        dir_list.append((dir, var_data["lim_sup1"]))
                    elif var_data["dimensionality"] == 2:
                        dir_list.append((dir, var_data["lim_sup1"] * var_data["lim_sup2"]))
                else:
                    dir_list.append(dir)
        # Flattening main local vars
        for _, var_data in proc_dir["local"]["var_table"].items():
            dir = var_data["virtual_direction"]
            indexed = var_data["indexed"]
            if dir not in dir_list:
                if indexed:
                    if var_data["dimensionality"] == 1:
                        dir_list.append((dir, var_data["lim_sup1"]))
                    elif var_data["dimensionality"] == 2:
                        dir_list.append((dir, var_data["lim_sup1"] * var_data["lim_sup2"]))
                else:
                    dir_list.append(dir)
        return dir_list

    def mem_init(self, const_table, proc_dir) -> None:
        self.mem = [[] for dir in range(10)]

        self.const_table = const_table.copy()
        self.proc_dir = proc_dir.copy()

        # Mapping contants to virtual memory
        for const, dir in self.const_table.items():
            self.mem[self.rel_dir(dir)].append(const)

        # Mapping global & local vars to virtual memory
        for dir in self.flatten_var_tables(proc_dir):
            if type(dir) == tuple:
                required_alloc_space = dir[1]
                while(required_alloc_space > 0):
                    self.mem[self.rel_dir(dir[0])].append(None)
                    required_alloc_space -= 1
            else:
                self.mem[self.rel_dir(dir)].append(None)

    def mem_dump(self):
        mem_segs = ["GI", "GF", "LI", "LF", "TI", "TF", "TB", "CI", "CF", "TP"]
        print("\n---VIRT MEM---")
        for idx, seg in enumerate(self.mem):
            print("{:>4}".format(idx * 1000), mem_segs[idx], "==>", seg)
        print("--------------\n")

    def get_operand(self, dir: int):
        if dir >= 9000:
            pointed_dir = int(self.mem[9][dir - 9000])
            operand = self.mem[int(pointed_dir / 1000)][pointed_dir - int(pointed_dir / 1000) * 1000]
            if int(pointed_dir / 1000) in [0, 2, 4, 7]:
                return int(operand)
            elif int(pointed_dir / 1000) in [1, 3, 5, 8]:
                return float(operand)
        else:
            operand = self.mem[int(dir / 1000)][dir - int(dir / 1000) * 1000]
            if int(dir / 1000) in [0, 2, 4, 7]:
                return int(operand)
            elif int(dir / 1000) in [1, 3, 5, 8]:
                return float(operand)

                
    def run(self, quadruples: list) -> None:
        self.quadruples = quadruples.copy()
        while self.quadruples[self.curr_ip][0] != "end":
            # self.mem_dump()
            quad = self.quadruples[self.curr_ip]
            if quad[0] in ["+", "-", "*", "/", "<", ">", "<>", "==", "and", "or"]:
                if type(quad[3]) == int and self.rel_dir(quad[3]) in [4, 5, 6, 9] \
                        and self.dir_translator(quad[3])[1] >= len(self.mem[self.rel_dir(quad[3])]):
                    self.mem[self.rel_dir(quad[3])].append(None)

            if quad[0] == "goto":
                self.curr_ip = quad[3]
                continue
            elif quad[0] == "while_goto":
                self.curr_ip = quad[1]
                continue
            elif quad[0] == "gotof":
                if not self.mem[self.dir_translator(quad[1])[0]][self.dir_translator(quad[1])[1]]:
                    self.curr_ip = quad[3]
                    continue

            elif quad[0] == "and":
                op1_translated_dir = self.dir_translator(quad[1])
                op2_translated_dir = self.dir_translator(quad[2])
                temp_translated_dir = self.dir_translator(quad[3])
                self.mem[temp_translated_dir[0]][temp_translated_dir[1]] = self.mem[op1_translated_dir[0]][op1_translated_dir[1]] \
                                                                           and self.mem[op2_translated_dir[0]][op2_translated_dir[1]]
            elif quad[0] == "or":
                op1_translated_dir = self.dir_translator(quad[1])
                op2_translated_dir = self.dir_translator(quad[2])
                temp_translated_dir = self.dir_translator(quad[3])
                self.mem[temp_translated_dir[0]][temp_translated_dir[1]] = self.mem[op1_translated_dir[0]][op1_translated_dir[1]] \
                                                                           or self.mem[op2_translated_dir[0]][op2_translated_dir[1]]

            elif quad[0] == ">":
                op1_translated_dir = self.dir_translator(quad[1])
                op2_translated_dir = self.dir_translator(quad[2])
                temp_translated_dir = self.dir_translator(quad[3])
                self.mem[temp_translated_dir[0]][temp_translated_dir[1]] = float(
                    self.mem[op1_translated_dir[0]][op1_translated_dir[1]]) > float(self.mem[op2_translated_dir[0]][op2_translated_dir[1]])
            elif quad[0] == "<":
                op1_translated_dir = self.dir_translator(quad[1])
                op2_translated_dir = self.dir_translator(quad[2])
                temp_translated_dir = self.dir_translator(quad[3])
                self.mem[temp_translated_dir[0]][temp_translated_dir[1]] = float(
                    self.mem[op1_translated_dir[0]][op1_translated_dir[1]]) < float(self.mem[op2_translated_dir[0]][op2_translated_dir[1]])
            elif quad[0] == "==":
                op1_translated_dir = self.dir_translator(quad[1])
                op2_translated_dir = self.dir_translator(quad[2])
                temp_translated_dir = self.dir_translator(quad[3])
                self.mem[temp_translated_dir[0]][temp_translated_dir[1]] = float(
                    self.mem[op1_translated_dir[0]][op1_translated_dir[1]]) == float(self.mem[op2_translated_dir[0]][op2_translated_dir[1]])
            elif quad[0] == "<>":
                op1_translated_dir = self.dir_translator(quad[1])
                op2_translated_dir = self.dir_translator(quad[2])
                temp_translated_dir = self.dir_translator(quad[3])
                self.mem[temp_translated_dir[0]][temp_translated_dir[1]] = float(
                    self.mem[op1_translated_dir[0]][op1_translated_dir[1]]) != float(self.mem[op2_translated_dir[0]][op2_translated_dir[1]])

            elif quad[0] == "+":
                op1_translated_dir = self.dir_translator(quad[1])
                op2_translated_dir = self.dir_translator(quad[2])
                temp_translated_dir = self.dir_translator(quad[3])
                self.mem[temp_translated_dir[0]][temp_translated_dir[1]] = self.get_operand(quad[1]) + self.get_operand(quad[2])
            elif quad[0] == "-":
                op1_translated_dir = self.dir_translator(quad[1])
                op2_translated_dir = self.dir_translator(quad[2])
                temp_translated_dir = self.dir_translator(quad[3])
                self.mem[temp_translated_dir[0]][temp_translated_dir[1]] = self.get_operand(quad[1]) - self.get_operand(quad[2])
            elif quad[0] == "*":
                op1_translated_dir = self.dir_translator(quad[1])
                op2_translated_dir = self.dir_translator(quad[2])
                temp_translated_dir = self.dir_translator(quad[3])
                self.mem[temp_translated_dir[0]][temp_translated_dir[1]] = self.get_operand(quad[1]) * self.get_operand(quad[2])
            elif quad[0] == "/":
                op1_translated_dir = self.dir_translator(quad[1])
                op2_translated_dir = self.dir_translator(quad[2])
                temp_translated_dir = self.dir_translator(quad[3])
                self.mem[temp_translated_dir[0]][temp_translated_dir[1]] = self.get_operand(quad[1]) / self.get_operand(quad[2])

            # elif quad[0] == "=":
            #     val_translated_dir = self.dir_translator(quad[1])
            #     var_translated_dir = self.dir_translator(quad[3])
            #     self.mem[var_translated_dir[0]][var_translated_dir[1]
            #                                     ] = self.mem[val_translated_dir[0]][val_translated_dir[1]]
            elif quad[0] == "=":
                if quad[3] >= 9000:
                    var_translated_dir = self.dir_translator(quad[3])
                    pointed_dir = self.mem[var_translated_dir[0]][var_translated_dir[1]]
                    var_translated_pointed_dir = self.dir_translator(pointed_dir)
                    self.mem[var_translated_pointed_dir[0]][var_translated_pointed_dir[1]] = self.get_operand(quad[1])
                else:    
                    var_translated_dir = self.dir_translator(quad[3])
                    self.mem[var_translated_dir[0]][var_translated_dir[1]] = self.get_operand(quad[1])

            elif quad[0] == "write":
                output = str(self.get_operand(quad[3])) if type(quad[3]) == int else quad[3]
                while (self.quadruples[self.curr_ip + 1][0] == "write"):
                    write_quad = self.quadruples[self.curr_ip + 1]
                    next_output = str(self.get_operand(write_quad[3])) if type(write_quad[3]) == int else write_quad[3]
                    output += next_output
                    self.curr_ip += 1
                print(output.replace('"', ''))
            
            elif quad[0] == "verify":
                index = self.get_operand(quad[1])
                inf_lim = int(self.mem[7][quad[2] - 7000])
                sup_lim = int(self.mem[7][quad[3] - 7000])
                if index < inf_lim or index >= sup_lim:
                    raise_error(None, "out_of_bounds")

            self.curr_ip += 1
