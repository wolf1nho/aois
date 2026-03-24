import math
import re

class DerivativeAnalyzer:
    def __init__(self):
        self.derivatives = {}

    def analyze(self, table, variables, d_of_variables = ""):
        if not table or not variables:
            return
        # if len(variables) == 1 and len(table) == 2:
            # result = [row[:] for row in table]
            # result[0][1] = table[0][1] ^ table[1][1]
            # result[1][1] = table[0][1] ^ table[1][1]
            # self.derivatives[d_of_variables + variables[0]] = TruthTable(result, variables)
            # return
        step = len(table) // 2
        for j in range(len(variables)):
            new_table = []
            for k in range(0, len(table)-step, step*2):
                for i in range(k, k + step):
                    new_table.append(table[i][:j] + table[i][j+1:-1])
                    new_table[-1].append(table[i][-1] ^ table[i + step][-1])
            other_variables = variables[:]
            if len(variables) > 1:
                other_variables.pop(j)
            self.derivatives[d_of_variables + variables[j]] = TruthTable(new_table, other_variables)            
            step //= 2
        self.analyze(new_table, variables[1:], d_of_variables + variables[0])

        
    def _build_sdnf(self, tb):
        if len(tb.table) == 1:
            return str(tb.table[0][0])
        clauses = []
        for row in tb.table:
            values, result = row[:-1], row[-1]
            if result:
                lits = []
                for var, val in zip(tb.variables, values):
                    lits.append(var if val else f"!{var}")
                clauses.append("(" + " & ".join(lits) + ")")
        return " | ".join(clauses) if clauses else "0"

    def _build_sknf(self, tb):
        if len(tb.table) == 1:
            return str(tb.table[0][0])
        clauses = []
        for row in tb.table:
            values, result = row[:-1], row[-1]
            if not result:
                lits = []
                for var, val in zip(tb.variables, values):
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

class TruthTable:
    def __init__(self, table, variables):
        self.variables = variables
        self.table = table

    def __repr__(self):
        if not self.table:
            return ""
        if len(self.table) == 0:
            return self.table[0][0]
        header = "  ".join(self.variables) + " | " + "f\n"
        result = header 
        result += "-" * len(header) + "\n"
        for row in self.table:
            v_str = "  ".join(str(int(v)) for v in row[:-1])
            result += f"{v_str} | {int(bool(row[-1]))}\n"
        return result