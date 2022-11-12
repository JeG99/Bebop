class virtual_machine():
    def __init__(self):
        self.quadruples = {}
        self.const_table = {}
        self.proc_dir = {}
        self.mem = []
        self.curr_ip = 0

    def rel_dir(self, dir):
        return int(dir / 1000)
    
    def dir_translator(self, direction):
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
        for dir in self.flatten_var_tables(proc_dir):
            self.mem[self.rel_dir(dir)].append(None)

    def run(self, quadruples: list) -> None:
        self.quadruples = quadruples.copy()
        while self.quadruples[self.curr_ip][0] != "end":
            print(self.quadruples[self.curr_ip - 1])
            if self.quadruples[self.curr_ip][0] == "goto":
                self.curr_ip = self.quadruples[self.curr_ip][3] 
            elif self.quadruples[self.curr_ip][0] == "=":
                val = self.quadruples[self.curr_ip][1]
                var = self.quadruples[self.curr_ip][3]
                val_translated_dir = self.dir_translator(val)
                var_translated_dir = self.dir_translator(var)
                # mem assign
            self.curr_ip += 1