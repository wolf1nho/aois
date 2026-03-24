class CalculationMinimizer:
    def __init__(self):
        self.table = []
        self.variables = []
        self.minimized_sdnf = ""
        self.minimized_sknf = ""
    
    def minimize_sknf(self, tb, variables):
        self.table = tb
        self.variables = variables
        if not self.table:
            return ""
        if len(self.table) == 0:
            return self.table[0][0]
        
        minimized_terms = []
        for row in self.table:
            if row[-1] == 0:
                minimized_terms.append(row[:-1])
        if not minimized_terms:
            self.minimized_sknf = "1"
            return 
        
        minimized_terms_new = []

        impossible_to_merge = False

        while not impossible_to_merge:

            for i in range(len(minimized_terms)):
                for j in range(i+1, len(minimized_terms)):
                    index = -1
                    for k in range(len(minimized_terms[i])):
                        if minimized_terms[i][k] != minimized_terms[j][k]:
                            if index == -1:
                                index = k
                            else:
                                index = -1
                                break
                    if index != -1:
                        minimized_terms_new.append(minimized_terms[i][:])
                        minimized_terms_new[-1][index] = 2

            if not minimized_terms_new:
                impossible_to_merge = True
            else:
                minimized_terms = minimized_terms_new[:]
                minimized_terms_new = []
            print(minimized_terms)

        i = 0
        while i < len(minimized_terms):
            count = 0
            for k in range(len(minimized_terms[i])):
                if minimized_terms[i][k] == 2:
                    count += 1
                    continue
                for j in range(0, len(minimized_terms)):
                    if j == i:
                        continue
                    if minimized_terms[i][k] == minimized_terms[j][k]:
                        count += 1
                        break
            if count == len(minimized_terms[i]):
                minimized_terms.pop(i)    
            else:
                i += 1

        clauses = []
        for row in minimized_terms:
                lits = []
                for var, val in zip(variables, row):
                    if val == 1:
                        lits.append(f"!{var}")
                    elif val == 0:
                        lits.append(var)
                if lits: 
                    clauses.append("(" + " | ".join(lits) + ")")
        self.minimized_sknf = " & ".join(clauses) if clauses else "1"

    def minimize_sdnf(self, tb, variables):
        self.table = tb
        self.variables = variables
        if not self.table:
            return ""
        if len(self.table) == 0:
            return self.table[0][0]
        
        
        minimized_terms = []
        for row in self.table:
            if row[-1] == 1:
                minimized_terms.append(row[:-1])
        if not minimized_terms:
            self.minimized_sknf = "0"
            return 
        
        minimized_terms_new = []

        impossible_to_merge = False

        while not impossible_to_merge:

            for i in range(len(minimized_terms)):
                for j in range(i+1, len(minimized_terms)):
                    index = -1
                    for k in range(len(minimized_terms[i])):
                        if minimized_terms[i][k] != minimized_terms[j][k]:
                            if index == -1:
                                index = k
                            else:
                                index = -1
                                break
                    if index != -1:
                        minimized_terms_new.append(minimized_terms[i][:])
                        minimized_terms_new[-1][index] = 2

            if not minimized_terms_new:
                impossible_to_merge = True
            else:
                minimized_terms = minimized_terms_new[:]
                minimized_terms_new = []
            print(minimized_terms)

        i = 0
        while i < len(minimized_terms):
            count = 0
            for k in range(len(minimized_terms[i])):
                if minimized_terms[i][k] == 2:
                    count += 1
                    continue
                for j in range(0, len(minimized_terms)):
                    if j == i:
                        continue
                    if minimized_terms[i][k] == minimized_terms[j][k]:
                        count += 1
                        break
            if count == len(minimized_terms[i]):
                minimized_terms.pop(i)    
            else:
                i += 1

        clauses = []
        for row in minimized_terms:
                lits = []
                for var, val in zip(variables, row):
                    if val == 1:
                        lits.append(var)
                    elif val == 0:
                        lits.append(f"!{var}")
                if lits: 
                    clauses.append("(" + " & ".join(lits) + ")")
        self.minimized_sdnf = " | ".join(clauses) if clauses else "0"

    def get_minimized_sknf(self):
        return self.minimized_sknf

    def get_minimized_sdnf(self):
        return self.minimized_sdnf     