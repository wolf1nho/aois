from src.TruthTable import TruthTable

class CalculationMinimizer:
    def __init__(self):
        self.table = TruthTable()
        self.minimized_sdnf = ""
        self.minimized_sknf = ""
    
    def _minimize_terms(self, minimized_terms, form):
        print(f"Минимизация расчетным методом ({form.upper()}):\n")
        print(f"Этап 1 ({form.upper()}): Исходные термы")
        self._print_terms(minimized_terms)
        
        minimized_terms_new = []
        impossible_to_merge = False
        stage = 2

        while not impossible_to_merge:
            print(f"Этап {stage} ({form.upper()}): Склеивание")
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
                print("Склеивание завершено, новых термов нет.\n")
                stage += 1
            else:
                minimized_terms = minimized_terms_new[:]
                minimized_terms_new = []
                self._print_terms(minimized_terms)
                stage += 1

        if any(all(x == 2 for x in term) for term in minimized_terms):
            self._print_terms(minimized_terms)
            return minimized_terms

        print(f"Этап {stage} ({form.upper()}): Удаление избыточных импликант")
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

        self._print_terms(minimized_terms)
        return minimized_terms

    def _print_terms(self, terms):
        for term in terms:
            print(''.join('-' if x == 2 else str(x) for x in term))
        print()

    def _build_clauses(self, minimized_terms, variables, form):
        if not minimized_terms:
            return "1" if form == 'sknf' else "0"

        for row in minimized_terms:
            if all(val == 2 for val in row):
                result = "1" if form == 'sdnf' else "0"
                print(f"Финальный результат ({form.upper()}): {result}\n")
                return result
        
        clauses = []
        for row in minimized_terms:
            lits = []
            for var, val in zip(variables, row):
                if form == 'sknf':
                    if val == 1:
                        lits.append(f"!{var}")
                    elif val == 0:
                        lits.append(var)
                elif form == 'sdnf':
                    if val == 1:
                        lits.append(var)
                    elif val == 0:
                        lits.append(f"!{var}")
            if lits: 
                if form == 'sknf':
                    clauses.append("(" + " | ".join(lits) + ")")
                elif form == 'sdnf':
                    clauses.append("(" + " & ".join(lits) + ")")
        result = ""
        if form == 'sknf':
            result = " & ".join(clauses) if clauses else "1"
        elif form == 'sdnf':
            result = " | ".join(clauses) if clauses else "0"
        print(f"Финальный результат ({form.upper()}): {result}\n")
        return result
    
    def minimize_sknf(self, table):
        self.table = table
        variables = table.variables
        
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
            return self.minimized_sknf
        
        minimized_terms = self._minimize_terms(minimized_terms, 'sknf')
        
        self.minimized_sknf = self._build_clauses(minimized_terms, variables, 'sknf')
        return self.minimized_sknf

    def minimize_sdnf(self, table):
        self.table = table
        variables = table.variables

        if not table.table:
            return ""
        if len(self.table) == 1:
            return self.table[0][0]
        
        
        minimized_terms = []
        for row in self.table:
            if row[-1] == 1:
                minimized_terms.append(row[:-1])
        if not minimized_terms:
            self.minimized_sdnf = "0"
            return self.minimized_sdnf
        
        minimized_terms = self._minimize_terms(minimized_terms, 'sdnf')
        
        self.minimized_sdnf = self._build_clauses(minimized_terms, variables, 'sdnf')
        return self.minimized_sdnf

    def get_minimized_sknf(self):
        return self.minimized_sknf

    def get_minimized_sdnf(self):
        return self.minimized_sdnf     