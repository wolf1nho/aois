from src.TruthTable import TruthTable

class DerivativeAnalyzer:
    def __init__(self):
        self.derivatives = {}

    def analyze(self, table, d_of_variables = ""):
        if not table.table or not table.variables:
            return
        
        step = len(table) // 2
        for j in range(len(table.variables)):
            new_table = TruthTable()
            for k in range(0, len(table)-step, step*2):
                for i in range(k, k + step):
                    new_table.append(table[i][:j] + table[i][j+1:-1])
                    new_table[-1].append(table[i][-1] ^ table[i + step][-1])
            other_variables = table.variables[:]
            if len(table.variables) > 1:
                other_variables.pop(j)
            self.derivatives[d_of_variables + table.variables[j]] = TruthTable(new_table, other_variables)            
            step //= 2
        new_table.variables = table.variables[1:]
        self.analyze(new_table, d_of_variables + table.variables[0])
        
    def _build_sdnf(self, table):
        if len(table.table) == 1:
            return str(table.table[0][0])
        clauses = []
        for row in table.table:
            values, result = row[:-1], row[-1]
            if result:
                lits = []
                for var, val in zip(table.variables, values):
                    lits.append(var if val else f"!{var}")
                clauses.append("(" + " & ".join(lits) + ")")
        return " | ".join(clauses) if clauses else "0"

    def _build_sknf(self, table):
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

    def print_derivative_canonical_forms(self):
        if not self.derivatives:
            print("Производные не вычислены")
            return

        print("\nКанонические формы булевых производных:")
        for var, tb in self.derivatives.items():
            sdnf = self._build_sdnf(tb)
            sknf = self._build_sknf(tb)
            print(f"\nПроизводная dF/d{var}:")
            print(f"СДНФ(dF/d{var}) = {sdnf if sdnf else '0'}")
            print(f"СКНФ(dF/d{var}) = {sknf if sknf else '1'}")