class virtual_machine():
    def __init__(self):
        self.quadruples = {}
        self.const_table = {}
        self.proc_dir = {}
        self.mem = []
        self.curr_ip = 0

    def rel_dir(self, dir) -> int:
        return int(dir / 1000)

    def dir_translator(self, direction) -> tuple:
        return self.rel_dir(direction), direction - self.rel_dir(direction) * 1000

    # TODO: ADD SUPPORT FOR INDEXED TYPES
    def flatten_var_tables(self, proc_dir) -> dict:
        dir_list = []
        # Flattening global vars
        for _, var_data in proc_dir["global"]["var_table"].items():
            dir = var_data["virtual_direction"]
            if dir not in dir_list:
                dir_list.append(dir)
        # Flattening main local vars
        for _, var_data in proc_dir["local"]["var_table"].items():
            dir = var_data["virtual_direction"]
            if dir not in dir_list:
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
            self.mem[self.rel_dir(dir)].append(None)

    def mem_dump(self):
        mem_segs = ["GI", "GF", "LI", "LF", "TI", "TF", "TB", "CI", "CF", "TP"]
        print("\n---VIRT MEM---")
        for idx, seg in enumerate(self.mem):
            print("{:>4}".format(idx * 1000), mem_segs[idx], "==>", seg)
        print("--------------\n")

    def run(self, quadruples: list) -> None:
        self.quadruples = quadruples.copy()
        while self.quadruples[self.curr_ip][0] != "end":
            quad = self.quadruples[self.curr_ip]
            if quad[0] in ["+", "-", "*", "/", "<", ">", "<>", "==", "and", "or"]:
                if type(quad[3]) == int and self.rel_dir(quad[3]) in [4, 5, 6] \
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
                self.mem[temp_translated_dir[0]][temp_translated_dir[1]] = float(
                    self.mem[op1_translated_dir[0]][op1_translated_dir[1]]) + float(self.mem[op2_translated_dir[0]][op2_translated_dir[1]])
            elif quad[0] == "-":
                op1_translated_dir = self.dir_translator(quad[1])
                op2_translated_dir = self.dir_translator(quad[2])
                temp_translated_dir = self.dir_translator(quad[3])
                self.mem[temp_translated_dir[0]][temp_translated_dir[1]] = float(
                    self.mem[op1_translated_dir[0]][op1_translated_dir[1]]) - float(self.mem[op2_translated_dir[0]][op2_translated_dir[1]])
            elif quad[0] == "*":
                op1_translated_dir = self.dir_translator(quad[1])
                op2_translated_dir = self.dir_translator(quad[2])
                temp_translated_dir = self.dir_translator(quad[3])
                self.mem[temp_translated_dir[0]][temp_translated_dir[1]] = float(
                    self.mem[op1_translated_dir[0]][op1_translated_dir[1]]) * float(self.mem[op2_translated_dir[0]][op2_translated_dir[1]])
            elif quad[0] == "/":
                op1_translated_dir = self.dir_translator(quad[1])
                op2_translated_dir = self.dir_translator(quad[2])
                temp_translated_dir = self.dir_translator(quad[3])
                self.mem[temp_translated_dir[0]][temp_translated_dir[1]] = float(
                    self.mem[op1_translated_dir[0]][op1_translated_dir[1]]) / float(self.mem[op2_translated_dir[0]][op2_translated_dir[1]])

            elif quad[0] == "=":
                val_translated_dir = self.dir_translator(quad[1])
                var_translated_dir = self.dir_translator(quad[3])
                self.mem[var_translated_dir[0]][var_translated_dir[1]
                                                ] = self.mem[val_translated_dir[0]][val_translated_dir[1]]

            elif quad[0] == "write":
                output = str(self.mem[self.dir_translator(
                    quad[3])[0]][self.dir_translator(quad[3])[1]]) if type(quad[3]) == int else quad[3]
                while (self.quadruples[self.curr_ip + 1][0] == "write"):
                    write_quad = self.quadruples[self.curr_ip + 1]
                    next_output = self.mem[self.dir_translator(
                        write_quad[3])[0]][self.dir_translator(write_quad[3])[1]] if type(write_quad[3]) == int else write_quad[3]
                    output += str(next_output)
                    self.curr_ip += 1
                print(output.replace('"', ''))

            self.curr_ip += 1
