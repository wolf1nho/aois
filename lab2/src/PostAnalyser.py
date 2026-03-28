class PostAnalyser:
    def __init__(self):
        self.t0 = False
        self.t1 = False
        self.s = False
        self.m = False
        self.l = False
    
    def execute(self, table):
        if not any(table[0]):
            self.t0 = True
        
        if all(table[-1]) == 1:
            self.t1 = True

        self.s = self.is_self_dual(table)

        self.m = self.is_monotone(table)

    def is_self_dual(self, table):
        n = len(table) // 2
        if n == 0:
            return False
        for i in range(n):
            if table[i][-1] == table[-1-i][-1]:
                return False
        return True
    
    def is_monotone(self, table):
        n = len(table)
        i = 0
        while i < n:
            if table[i][-1] == 1:
                while i < n:
                    if table[i][-1] == 0:
                        return False
                    i += 1
            i += 1
        return True