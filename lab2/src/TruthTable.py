class TruthTable:
    def __init__(
            self,
            table: list[int] | None = None,
            variables: list[str] | None = None
            ):
        self._variables = variables or []
        self._table = table or []

    def __str__(self):
        if not self._table:
            return ""
        if len(self._table) == 0:
            return self._table[0][0]
        header = "  ".join(self._variables) + " | " + "f\n"
        result = header 
        result += "-" * len(header) + "\n"
        for row in self._table:
            v_str = "  ".join(str(int(v)) for v in row[:-1])
            result += f"{v_str} | {int(bool(row[-1]))}\n"
        return result

    def append(self, row):
        self._table.append(row)

    def __getitem__(self, key):
        return self._table[key]

    def __setitem__(self, key, value):
        self._table[key] = value

    def __len__(self):
        return len(self._table)

    @property
    def variables(self):
        return self._variables
    
    @variables.setter
    def variables(self, value):
        self._variables = value

    @property
    def table(self):
        return self._table

    @table.setter
    def table(self, value):
        self._table = value
