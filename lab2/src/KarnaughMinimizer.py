class KarnaughMinimizer:
    def __init__(self):
        self.minimized_sdnf = ""
        self.minimized_sknf = ""

    def minimize_sdnf(self, table):
        self.table = table
        self.minimized_sdnf = self._minimize(table.table, table.variables, target_value=1, is_dnf=True)
        return self.minimized_sdnf

    def minimize_sknf(self, table):
        self.table = table
        self.minimized_sknf = self._minimize(table.table, table.variables, target_value=0, is_dnf=False)
        return self.minimized_sknf

    def print_karnaugh_map(self, table):
        if not table:
            print("\nКарта Карно: пустая таблица")
            return
        
        variables = table.variables 

        row_bits = len(variables) // 2
        col_bits = len(variables) - row_bits
        row_vars = variables[:row_bits]
        col_vars = variables[row_bits:]
        row_codes = self._gray_code(row_bits)
        col_codes = self._gray_code(col_bits)

        print("\nКарта Карно:")
        row_label = "".join(row_vars) if row_vars else "-"
        col_label = "".join(col_vars) if col_vars else "-"
        header = [f"{row_label}\\{col_label}"]
        header.extend(self._bits_to_label(code) for code in col_codes)

        row_labels = [self._bits_to_label(code) for code in row_codes]
        cell_width = max(
            max(len(item) for item in header),
            max(len(item) for item in row_labels),
            1,
        )

        header_line = " | ".join(item.rjust(cell_width) for item in header)
        print(header_line)
        print("-" * len(header_line))

        for row_code in row_codes:
            row = [self._bits_to_label(row_code)]
            for col_code in col_codes:
                bits = row_code + col_code
                cell_index = self._bits_to_int(bits)
                row.append(str(table[cell_index][-1]))
            print(" | ".join(item.rjust(cell_width) for item in row))

    def _minimize(self, table, variables, target_value, is_dnf):
        if not table:
            return "0" if is_dnf else "1"

        target_cells = {
            index
            for index, row in enumerate(table)
            if row[-1] == target_value
        }

        if not target_cells:
            return "0" if is_dnf else "1"

        if len(target_cells) == len(table):
            return "1" if is_dnf else "0"

        groups = self._find_groups(table, len(variables), target_cells)
        chosen_groups = self._choose_minimal_cover(groups, target_cells)
        return self._format_expression(chosen_groups, variables, is_dnf)

    def _find_groups(self, table, var_count, target_cells):
        groups_by_pattern = {}

        for pattern in self._pattern_variants(var_count):
            covered = {
                index
                for index, row in enumerate(table)
                if self._matches_pattern(row[:-1], pattern)
            }
            if not covered or not covered.issubset(target_cells):
                continue

            literal_count = sum(1 for value in pattern if value != -1)
            groups_by_pattern[pattern] = {
                "pattern": pattern,
                "covers": covered,
                "literal_count": literal_count,
            }

        return list(groups_by_pattern.values())

    def _choose_minimal_cover(self, groups, target_cells):
        groups = self._remove_dominated_groups(groups)
        essential = []
        covered = set()

        for cell in target_cells:
            candidates = [group for group in groups if cell in group["covers"]]
            if len(candidates) == 1 and candidates[0] not in essential:
                essential.append(candidates[0])

        for group in essential:
            covered.update(group["covers"])

        uncovered = target_cells - covered
        if not uncovered:
            return essential

        remaining = [group for group in groups if group not in essential]
        groups_by_cell = {
            cell: [group for group in remaining if cell in group["covers"]]
            for cell in uncovered
        }
        best_subset = self._search_best_cover(uncovered, groups_by_cell, [])
        return essential + (best_subset if best_subset is not None else [])

    def _is_better_cover(self, candidate, current_best):
        candidate_score = (
            len(candidate),
            sum(group["literal_count"] for group in candidate),
        )
        current_score = (
            len(current_best),
            sum(group["literal_count"] for group in current_best),
        )
        return candidate_score < current_score

    def _format_expression(self, groups, variables, is_dnf):
        if not groups:
            return "0" if is_dnf else "1"

        formatted = []
        sorted_groups = sorted(groups, key=lambda group: group["pattern"])

        for group in sorted_groups:
            literals = []
            for variable, value in zip(variables, group["pattern"]):
                if value == -1:
                    continue
                if is_dnf:
                    literals.append(variable if value == 1 else f"!{variable}")
                else:
                    literals.append(variable if value == 0 else f"!{variable}")

            if not literals:
                return "1" if is_dnf else "0"

            separator = " & " if is_dnf else " | "
            # if len(literals) == 1:
            #     formatted.append(literals[0])
            # else:
            formatted.append("(" + separator.join(literals) + ")")

        joiner = " | " if is_dnf else " & "
        return joiner.join(formatted)

    def _remove_dominated_groups(self, groups):
        filtered = []

        for index, group in enumerate(groups):
            dominated = False
            for other_index, other in enumerate(groups):
                if index == other_index:
                    continue
                if not group["covers"].issubset(other["covers"]):
                    continue
                if (group["covers"] < other["covers"] and
                        other["literal_count"] <= group["literal_count"]):
                    dominated = True
                    break
                if (group["covers"] == other["covers"] and
                        other["literal_count"] < group["literal_count"]):
                    dominated = True
                    break
            if not dominated:
                filtered.append(group)

        return filtered

    def _search_best_cover(self, uncovered, groups_by_cell, current):
        if not uncovered:
            return current[:]

        target_cell = min(uncovered, key=lambda cell: len(groups_by_cell[cell]))
        candidates = sorted(
            groups_by_cell[target_cell],
            key=lambda group: (-len(group["covers"] & uncovered), group["literal_count"]),
        )

        best = None
        for group in candidates:
            new_current = current + [group]
            if best is not None and not self._is_better_cover(new_current, best):
                continue

            new_uncovered = uncovered - group["covers"]
            candidate = self._search_best_cover(new_uncovered, groups_by_cell, new_current)
            if candidate is None:
                continue
            if best is None or self._is_better_cover(candidate, best):
                best = candidate

        return best

    def _pattern_variants(self, length):
        if length == 0:
            return [()]

        variants = [()]
        for _ in range(length):
            next_variants = []
            for variant in variants:
                next_variants.append(variant + (-1,))
                next_variants.append(variant + (0,))
                next_variants.append(variant + (1,))
            variants = next_variants

        return variants

    def _matches_pattern(self, values, pattern):
        for value, expected in zip(values, pattern):
            if expected != -1 and value != expected:
                return False
        return True

    def _gray_code(self, bit_count):
        if bit_count == 0:
            return [()]
        if bit_count == 1:
            return [(0,), (1,)]

        previous = self._gray_code(bit_count - 1)
        return (
            [(0,) + code for code in previous]
            + [(1,) + code for code in reversed(previous)]
        )

    def _bits_to_int(self, bits):
        value = 0
        for bit in bits:
            value = value * 2 + bit
        return value

    def _bits_to_label(self, bits):
        if not bits:
            return "-"
        return "".join(str(bit) for bit in bits)
