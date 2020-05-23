class Context:
    def __init__(self, name, parent=None, parent_position=None, symbol_table=None):
        self.name = name
        self.parent = parent
        self.parent_start_pos = parent_position
        self.symbol_table = symbol_table if symbol_table is not None else SymbolTable()


class SymbolTable:
    def __init__(self):
        self.symbols = {}
        self.parent = None

    def get(self, name):
        value = self.symbols.get(name)
        if value is None and self.parent:
            return self.parent.get(name)
        return value

    def set(self, name, value):
        self.symbols[name] = value

    def remove(self, name):
        del self.symbols[name]
