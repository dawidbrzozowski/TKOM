from errors.error import RunTimeError
from interpreting.values import FunctionDefinition
from lexer.token.tokens import ValueToken


class Context:
    def __init__(self, name, parent=None, position=None, use_parent_symbol_table=False):
        self.name = name
        self.parent = parent
        self.position = position
        self.symbol_table = SymbolTable(parent.symbol_table) if parent and use_parent_symbol_table else SymbolTable()

    def copy_symbols_from(self, other):
        self.symbol_table.update(other.symbol_table)

    def get_variable(self, variable_name: ValueToken):
        variable = self.symbol_table.get(variable_name.value)
        if variable is None:
            raise RunTimeError(variable_name.pos_start, f'{variable_name.value} not defined.', self)
        return variable

    def add_variable(self, variable_name, value):
        self.symbol_table.set(variable_name, value)


class SymbolTable:
    def __init__(self, symbol_table=None):
        self.symbols = dict(symbol_table.symbols) if symbol_table else {}

    def get(self, name):
        return self.symbols.get(name)

    def set(self, name, value):
        self.symbols[name] = value

    def remove(self, name):
        del self.symbols[name]

    def update(self, other):
        self.symbols.update(other.symbols)


class ContextManager:
    def __init__(self):
        self.global_context = Context('<global>')
        self.current_context = Context('<main>')
        self.current_context.copy_symbols_from(self.global_context)

    def switch_context_to(self, function: FunctionDefinition):
        function_context = Context(function.name, self.current_context, self.current_context.position)
        function_context.copy_symbols_from(self.global_context)
        self.current_context = function_context
        self.current_context.position = function.pos_start.copy()

    def switch_to_parent_context(self):
        if not self.current_context.parent:
            raise RunTimeError(self.current_context.position, f'No parent for context: {self.current_context.name}',
                               self)
        self.current_context = self.current_context.parent

    def get_variable(self, variable_name):
        return self.current_context.get_variable(variable_name)

    def add_function(self, function_name, function):
        self.global_context.add_variable(function_name, function)

    def get_function(self, function_name):
        return self.global_context.get_variable(function_name)

    def add_variable(self, variable_name, value, expected_type):
        self.verify_assignment(variable_name, value, expected_type)
        self.current_context.add_variable(variable_name.value, value)

    def verify_assignment(self, variable_name: ValueToken, value, expected_type):
        self.check_type_match(expected_type, value)
        if expected_type is None:
            current_value = self.get_variable(variable_name)
            if not current_value:
                raise RunTimeError(variable_name.pos_start,
                                   'This variable has not been defined yet. Put a type.', self.current_context)

            if current_value.type_ != value.type_:
                raise RunTimeError(value.pos_start,
                                   f'Tried to put a value of type {value.type_}'
                                   f' to a variable of type {current_value.type_}', self.current_context)

    def check_type_match(self, expected_type, actual_value):
        if expected_type and actual_value and not actual_value.type_ == str(expected_type):
            raise RunTimeError(expected_type.pos_start,
                               f'Expected type: {str(expected_type)} got {actual_value.type_} instead.',
                               self.current_context)
