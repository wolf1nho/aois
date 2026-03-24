class ZhegalkinBuilder:
    def __init__(self):
        self.polynomial = []

    def build(self, table, variables):
        n = len(variables)
        m = len(table)
        column = []
        for row in table:
            column.append(row[-1])
        triangle = [column[:]]
        for i in range(1, m):
            row = []
            for j in range(1, len(triangle[-1])):
                row.append((triangle[-1][j] + triangle[-1][j - 1]) % 2)
            triangle.append(row)
        result = []
        for row in triangle:
            result.append(row[0])
        
        self.polynomial = []
        for i in range(m):
            if result[i]:
                summand = []
                for j in range(n): 
                    if table[i][j]:
                        summand.append(variables[j])
                if not summand:
                    self.polynomial.append("1")
                else:
                    self.polynomial.append("".join(summand))
        
        zhegalkin_str = " + ".join(self.polynomial) if self.polynomial else "0"
        print("Формула Жегалкина: ", zhegalkin_str)
    
    def is_linear(self):
        return all(len(summand) == 1 for summand in self.polynomial)
        
