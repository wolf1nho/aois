class CanonicalFormsBuilder:
    def __init__(self):
        self.num_sdnf = []
        self.num_sknf = []

    def get_num_sknf(self):
        return self.num_sknf

    def get_num_sdnf(self):
        return self.num_sdnf

    def build_sdnf(self, table):
        if len(table) == 1:
            return str(table[0][0])
        clauses = []
        for row in table:
            values, result = row[:-1], row[-1]
            if result:
                lits = []
                for var, val in zip(table.variables, values):
                    lits.append(var if val else f"!{var}")
                clauses.append("(" + " & ".join(lits) + ")")
        return " | ".join(clauses) if clauses else "0"

    def build_sknf(self, table):
        if len(table) == 1:
            return str(table[0][0])
        clauses = []
        for row in table:
            values, result = row[:-1], row[-1]
            if not result:
                lits = []
                for var, val in zip(table.variables, values):
                    lits.append(f"!{var}" if val else var)
                clauses.append("(" + " | ".join(lits) + ")")
        return " & ".join(clauses) if clauses else "1"
    
    def to_numeric_form(self, table):
        self.num_sdnf = []
        self.num_sknf = []
        for row in table:
            values = row[:-1]
            result = row[-1]
            value = self._bin_to_int(values)
            if result:
                self.num_sdnf.append(value)
            else:
                self.num_sknf.append(value)
    
    def _bin_to_int(self, binary):
        val = 0
        for i in range(len(binary)):
            val = val * 2 + binary[i]
        return val
    
    def get_index_form(self, table):
        column = []
        for row in table:
            column.append(row[-1])
        return self._bin_to_int(column)