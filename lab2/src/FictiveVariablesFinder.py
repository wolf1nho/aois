class FictiveVariablesFinder:
    @staticmethod
    def find(table):
        step = len(table) // 2
        is_fictive = []
        for j in range(len(table.variables)):
            fictive = True
            for k in range(0, len(table)-step, step*2):
                for i in range(k, k + step):
                    if table[i][-1] != table[i + step][-1]:
                        fictive = False
                        break
                if not fictive:
                    break
            if fictive:
                is_fictive.append(1)
            else:
                is_fictive.append(0)
            step //= 2
        result = []
        for i in range(len(table.variables)):
            if is_fictive[i]:
                result.append(table.variables[i])
        
        return FictiveVariablesFinder.to_str(result)
        
    @staticmethod
    def to_str(variables):
        if not variables:
            return "отсутствуют"
        return ", ".join(variables)

        