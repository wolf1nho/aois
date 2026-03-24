class CanonicalFormsBuilder:
    def __init__(self):
        self.sdnf = ""
        self.sknf = ""
        self.num_sdnf = []
        self.num_sknf = []

    def get_canonical_forms(self, table, variables):
        self.sdnf = self._build_sdnf(table, variables)
        self.sknf = self._build_sknf(table, variables)
        return self.sdnf, self.sknf

    def _build_sdnf(self, table, variables):
        clauses = []
        for row in table:
            values, result = row[:-1], row[-1]
            if result:
                lits = []
                for var, val in zip(variables, values):
                    lits.append(var if val else f"!{var}")
                clauses.append("(" + " & ".join(lits) + ")")
        return " | ".join(clauses) if clauses else "0"

    def _build_sknf(self, table, variables):
        clauses = []
        for row in table:
            values, result = row[:-1], row[-1]
            if not result:
                lits = []
                for var, val in zip(variables, values):
                    lits.append(f"!{var}" if val else var)
                clauses.append("(" + " | ".join(lits) + ")")
        return " & ".join(clauses) if clauses else "1"
    
    def to_numeric_form(self, table):
        self.num_sdnf = []
        self.num_sknf = []
        for row in table:
            values = row[:-1]
            result = row[-1]
            value = self.bin_to_int(values)
            if result:
                self.num_sdnf.append(value)
            else:
                self.num_sknf.append(value)
    
    def bin_to_int(self, binary):
        val = 0
        for i in range(len(binary)):
            val = val * 2 + binary[i]
        return val
    
    def get_index_form(self, table):
        column = []
        for row in table:
            column.append(row[-1])
        return self.bin_to_int(column)