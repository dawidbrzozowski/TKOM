class Context:
    def __init__(self, name, parent=None, position=None):
        self.name = name
        self.parent = parent
        self.position = position
        self.symbol_table = SymbolTable(parent.symbol_table) if parent else SymbolTable()


class SymbolTable:
    def __init__(self, symbol_table=None):
        self.symbols = dict(symbol_table.symbols) if symbol_table else {}

    def get(self, name):
        return self.symbols.get(name)

    def set(self, name, value):
        self.symbols[name] = value

    def remove(self, name):
        del self.symbols[name]
