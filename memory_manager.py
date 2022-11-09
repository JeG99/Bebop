class memory_manager():
    def __init__(self):
        self.const_table = {}
        self.proc_dir = {}
        self.mem = []

    def rel_dir(self, dir):
        return int(dir / 1000)

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

        print(self.mem)