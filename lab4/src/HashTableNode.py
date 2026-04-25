class HashTableNode:
    def __init__(self, key=None, value=None):
        self.key = key
        self.value = value

        self.C = False   # флажок коллизий (True, если есть коллизия по этому базовому адресу)
        self.U = (key is not None)    # флажок «занято»
        self.P0 = None   # указатель (индекс) на следующую запись в цепочке