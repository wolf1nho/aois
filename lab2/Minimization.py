class Mini:
    def __init__(self):
        self.minimized_sdnf = ""
        self.minimized_sknf = ""
        self.sdnf_stages = []
        self.sknf_stages = []
        self.variables = []

    def minimize(self, table, variables):
        self.variables = variables[:]
        self.sdnf_stages = []
        self.sknf_stages = []

        self.minimized_sdnf, self.sdnf_stages = self._minimize_form(
            table, variables, target_value=1, is_dnf=True
        )
        self.minimized_sknf, self.sknf_stages = self._minimize_form(
            table, variables, target_value=0, is_dnf=False
        )

        self._print_stages("СДНФ", self.sdnf_stages, is_dnf=True)
        self._print_stages("СКНФ", self.sknf_stages, is_dnf=False)

    def get_minimized_sdnf(self):
        return self.minimized_sdnf

    def get_minimized_sknf(self):
        return self.minimized_sknf

    def _minimize_form(self, table, variables, target_value, is_dnf):
        base_terms = []
        indexes = []

        for row_index, row in enumerate(table):
            if row[-1] == target_value:
                base_terms.append(tuple(int(value) for value in row[:-1]))
                indexes.append(row_index)

        if not base_terms:
            return ("0" if is_dnf else "1"), []

        if len(base_terms) == len(table):
            return ("1" if is_dnf else "0"), []

        current_terms = [
            {
                "pattern": term,
                "covers": {index},
            }
            for term, index in zip(base_terms, indexes)
        ]

        stages = [self._clone_stage(current_terms)]
        prime_implicants = []

        while current_terms:
            next_terms, leftovers = self._glue_terms(current_terms)
            prime_implicants.extend(leftovers)

            if not next_terms:
                break

            current_terms = next_terms
            stages.append(self._clone_stage(current_terms))

        prime_implicants = self._deduplicate_terms(prime_implicants)
        chosen_terms = self._choose_minimal_cover(prime_implicants, indexes)
        minimized = self._format_expression(chosen_terms, variables, is_dnf)
        return minimized, stages

    def _clone_stage(self, terms):
        return [dict(pattern=term["pattern"], covers=set(term["covers"])) for term in terms]

    def _glue_terms(self, terms):
        next_terms = []
        used = [False] * len(terms)

        for i in range(len(terms)):
            for j in range(i + 1, len(terms)):
                glued_pattern = self._combine_patterns(
                    terms[i]["pattern"], terms[j]["pattern"]
                )
                if glued_pattern is None:
                    continue

                used[i] = True
                used[j] = True
                next_terms.append(
                    {
                        "pattern": glued_pattern,
                        "covers": terms[i]["covers"] | terms[j]["covers"],
                    }
                )

        leftovers = [terms[i] for i in range(len(terms)) if not used[i]]
        return self._deduplicate_terms(next_terms), leftovers

    def _combine_patterns(self, first, second):
        diff_index = -1

        for index, (left, right) in enumerate(zip(first, second)):
            if left == right:
                continue
            if left == -1 or right == -1:
                return None
            if diff_index != -1:
                return None
            diff_index = index

        if diff_index == -1:
            return None

        combined = list(first)
        combined[diff_index] = -1
        return tuple(combined)

    def _deduplicate_terms(self, terms):
        unique = {}
        for term in terms:
            pattern = term["pattern"]
            if pattern not in unique:
                unique[pattern] = {
                    "pattern": pattern,
                    "covers": set(term["covers"]),
                }
            else:
                unique[pattern]["covers"].update(term["covers"])
        return list(unique.values())

    def _choose_minimal_cover(self, prime_implicants, required_indexes):
        required = set(required_indexes)
        essential = []
        covered = set()

        for index in required_indexes:
            candidates = [term for term in prime_implicants if index in term["covers"]]
            if len(candidates) == 1 and candidates[0] not in essential:
                essential.append(candidates[0])

        for term in essential:
            covered.update(term["covers"])

        remaining = [term for term in prime_implicants if term not in essential]
        uncovered = required - covered

        if not uncovered:
            return essential

        best_subset = None

        for mask in range(1 << len(remaining)):
            subset = []
            subset_covered = set(covered)

            for bit in range(len(remaining)):
                if mask & (1 << bit):
                    subset.append(remaining[bit])
                    subset_covered.update(remaining[bit]["covers"])

            if not uncovered.issubset(subset_covered):
                continue

            candidate = essential + subset
            if best_subset is None or self._is_better_cover(candidate, best_subset):
                best_subset = candidate

        return best_subset if best_subset is not None else essential

    def _is_better_cover(self, candidate, current_best):
        candidate_score = (
            len(candidate),
            sum(self._literal_count(term["pattern"]) for term in candidate),
        )
        current_score = (
            len(current_best),
            sum(self._literal_count(term["pattern"]) for term in current_best),
        )
        return candidate_score < current_score

    def _literal_count(self, pattern):
        return sum(1 for value in pattern if value != -1)

    def _format_expression(self, terms, variables, is_dnf):
        if not terms:
            return "0" if is_dnf else "1"

        formatted_terms = []
        sorted_terms = sorted(terms, key=lambda term: term["pattern"])

        for term in sorted_terms:
            literals = []
            for variable, value in zip(variables, term["pattern"]):
                if value == -1:
                    continue
                if is_dnf:
                    literals.append(variable if value == 1 else f"!{variable}")
                else:
                    literals.append(variable if value == 0 else f"!{variable}")

            if not literals:
                return "1" if is_dnf else "0"

            separator = " & " if is_dnf else " | "
            formatted_terms.append("(" + separator.join(literals) + ")")

        joiner = " | " if is_dnf else " & "
        return joiner.join(formatted_terms)

    def _format_pattern(self, pattern, variables, is_dnf):
        literals = []
        for variable, value in zip(variables, pattern):
            if value == -1:
                continue
            if is_dnf:
                literals.append(variable if value == 1 else f"!{variable}")
            else:
                literals.append(variable if value == 0 else f"!{variable}")

        if not literals:
            return "1" if is_dnf else "0"

        separator = " & " if is_dnf else " | "
        return "(" + separator.join(literals) + ")"

    def _print_stages(self, form_name, stages, is_dnf):
        print(f"\nСтадии склеивания для {form_name}:")
        if not stages:
            print("Склеивание не требуется")
            return

        for index, stage in enumerate(stages, start=1):
            print(f"{index}-я стадия:")
            for term in stage:
                pattern = self._format_pattern(
                    term["pattern"],
                    self.variables,
                    is_dnf,
                )
                print(pattern)