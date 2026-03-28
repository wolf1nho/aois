class CalculationTabularMinimizer:
    def __init__(self):
        self.minimized_sdnf = ""
        self.minimized_sknf = ""

    def _find_prime_implicants(self, terms, form):
        print(f"Минимизация расчетно-табличным методом ({form.upper()}):")
        current_terms = set(tuple(t) for t in terms)
        prime_implicants = set()
        stage = 1

        print(f"Этап {stage} ({form.upper()}): Исходные термы")
        self._print_terms(current_terms)
        stage += 1

        while True:
            next_terms = set()
            used = set()
            term_list = list(current_terms)
            
            print(f"Этап {stage} ({form.upper()}): Склеивание")
            for i in range(len(term_list)):
                for j in range(i + 1, len(term_list)):
                    diff_count = 0
                    diff_index = -1
                    
                    for k in range(len(term_list[i])):
                        if term_list[i][k] != term_list[j][k]:
                            diff_count += 1
                            diff_index = k
                    
                    if diff_count == 1:
                        new_term = list(term_list[i])
                        new_term[diff_index] = 2
                        next_terms.add(tuple(new_term))
                        used.add(term_list[i])
                        used.add(term_list[j])
            
            for t in current_terms:
                if t not in used:
                    prime_implicants.add(t)
            
            if not next_terms:
                print("Склеивание завершено, новых термов нет.\n")
                stage += 1
                break
            else:
                current_terms = next_terms
                self._print_terms(current_terms)
                stage += 1

        print(f"Этап {stage} ({form.upper()}): Удаление избыточных импликант")
        self._print_terms(prime_implicants)
        return prime_implicants

    def _print_terms(self, terms):
        for term in terms:
            print(''.join('-' if x == 2 else str(x) for x in term))
        print()

    def _print_coverage_chart(self, chart, prime_list, initial_terms):
        print("Таблица покрытия:")
        term_labels = [''.join(str(x) for x in term) for term in initial_terms]
        max_term_len = max(len(label) for label in term_labels)
        max_prime_len = max(len(''.join('-' if x == 2 else str(x) for x in prime)) for prime in prime_list)
        
        header = f"{'':<{max_prime_len}} | " + " | ".join(f"{label:<{max_term_len}}" for label in term_labels)
        print(header)
        print("-" * len(header))
        for i, prime in enumerate(prime_list):
            prime_str = ''.join('-' if x == 2 else str(x) for x in prime)
            row = f"{prime_str:<{max_prime_len}} | " + " | ".join(f"{'X' if chart[i][j] else ' ':<{max_term_len}}" for j in range(len(initial_terms)))
            print(row)
        print()

    def _build_coverage_chart(self, prime_list, initial_terms, variables):
        chart = [[False] * len(initial_terms) for _ in range(len(prime_list))]
        
        for i, prime in enumerate(prime_list):
            for j, start in enumerate(initial_terms):
                match = True
                for k in range(len(variables)):
                    if prime[k] != 2 and prime[k] != start[k]:
                        match = False
                        break
                chart[i][j] = match
        
        return chart

    def _select_minimal_cover(self, chart, num_columns, core_selection='last'):
        selected_indices = set()
        covered_columns = [False] * num_columns

        for j in range(num_columns):
            covering = [i for i in range(len(chart)) if chart[i][j]]
            count = len(covering)
            if count == 1:
                if core_selection == 'last':
                    selected_indices.add(covering[-1])
                elif core_selection == 'first':
                    selected_indices.add(covering[0])

        for idx in selected_indices:
            for j in range(num_columns):
                if chart[idx][j]:
                    covered_columns[j] = True

        while not all(covered_columns):
            best_i = -1
            max_new_cover = 0
            for i in range(len(chart)):
                if i not in selected_indices:
                    new_cover = sum(1 for j in range(num_columns) if chart[i][j] and not covered_columns[j])
                    if new_cover > max_new_cover:
                        max_new_cover = new_cover
                        best_i = i
            if best_i != -1:
                selected_indices.add(best_i)
                for j in range(num_columns):
                    if chart[best_i][j]:
                        covered_columns[j] = True
            else:
                break

        return selected_indices

    def minimize_sdnf(self, table):
        variables = table.variables
        
        if not table.table:
            return "0"

        minimized_terms = [row[:-1] for row in table if row[-1] == 1]
        
        if not minimized_terms:
            self.minimized_sdnf = "0"
            return "0"
        
        initial_terms = [tuple(t) for t in minimized_terms]
        
        prime_implicants = self._find_prime_implicants(minimized_terms, 'sdnf')

        prime_list = list(prime_implicants)
        chart = self._build_coverage_chart(prime_list, initial_terms, variables)
        self._print_coverage_chart(chart, prime_list, initial_terms)

        selected_indices = self._select_minimal_cover(chart, len(initial_terms), 'last')

        result_parts = []
        for idx in selected_indices:
            term = prime_list[idx]
            if all(val == 2 for val in term):
                self.minimized_sdnf = "1"
                return "1"
                
            clause = []
            for i in range(len(variables)):
                if term[i] == 1:
                    clause.append(variables[i])
                elif term[i] == 0:
                    clause.append(f"!{variables[i]}")
            
            if len(clause) > 1:
                result_parts.append(f"({' & '.join(clause)})")
            elif len(clause):
                result_parts.append(clause[0])
        
        self.minimized_sdnf = " | ".join(result_parts) if result_parts else "0"
        return self.minimized_sdnf

    def minimize_sknf(self, table):
        variables = table.variables

        if not table.table:
            return "1"

        minimized_terms = [row[:-1] for row in table if row[-1] == 0]
        
        if not minimized_terms:
            self.minimized_sknf = "1"
            return "1"
        
        initial_terms = [tuple(t) for t in minimized_terms]
        
        prime_implicants = self._find_prime_implicants(minimized_terms, 'sknf')

        prime_list = list(prime_implicants)
        chart = self._build_coverage_chart(prime_list, initial_terms, variables)
        self._print_coverage_chart(chart, prime_list, initial_terms)

        selected_indices = self._select_minimal_cover(chart, len(initial_terms), 'first')

        result_parts = []
        for idx in selected_indices:
            term = prime_list[idx]
            if all(val == 2 for val in term):
                self.minimized_sknf = "0"
                return "0"

            clause = []
            for i in range(len(variables)):
                if term[i] == 0:
                    clause.append(variables[i])
                elif term[i] == 1:
                    clause.append(f"!{variables[i]}")
            
            if len(clause) > 1:
                result_parts.append(f"({' | '.join(clause)})")
            elif len(clause):
                result_parts.append(clause[0])

        self.minimized_sknf = " & ".join(result_parts) if result_parts else "1"
        return self.minimized_sknf

    def get_minimized_sdnf(self):
        return self.minimized_sdnf

    def get_minimized_sknf(self):
        return self.minimized_sknf

        

        
