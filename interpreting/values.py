from errors.error import RunTimeError
from lexer.token.token_type import TokenType
from lexer.token.token_type_repr import token_type_repr


class Value:
    def __init__(self, value, pos_start=None, pos_end=None, context=None):
        self.value = value
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.context = context

    def set_position(self, pos_start, pos_end):
        self.pos_start = pos_start
        self.pos_end = pos_end

    def set_context(self, context):
        self.context = context

    def __repr__(self):
        return str(self.value)

    def add(self, other):
        self.raise_runtime_error_for_operation('+', other)

    def subtract(self, other):
        self.raise_runtime_error_for_operation('-', other)

    def multiply(self, other):
        self.raise_runtime_error_for_operation('*', other)

    def divide(self, other):
        self.raise_runtime_error_for_operation('/', other)

    def raise_runtime_error_for_operation(self, operator, other):
        raise RunTimeError(self.pos_start,
                           f'{operator} not defined for type {token_type_repr.get(inversed_matching.get(type(self)))}'
                           f' and {token_type_repr.get(inversed_matching.get(type(other)))}',
                           self.context)


class Number(Value):
    def __init__(self, value, pos_start=None, pos_end=None, context=None):
        super().__init__(value, pos_start, pos_end, context)

    def is_equal(self, other):
        if isinstance(other, Number):
            return BoolValue(self.value == other.value, self.context)
        else:
            raise RunTimeError(self.pos_start, f"Can't compare values of type {type(self.value)}, {type(other.value)}",
                               self.context)

    def is_not_equal(self, other):
        return BoolValue(1 if not self.is_equal(other).value else 0)

    def is_greater_than(self, other):
        if isinstance(other, Number):
            return BoolValue(self.value > other.value, self.pos_start, self.pos_end, self.context)
        else:
            raise RunTimeError(self.pos_start, f"Can't compare values of type {type(self.value)}, {type(other.value)}",
                               self.context)

    def is_less_or_eq(self, other):
        return BoolValue(1 if not self.is_greater_than(other).value else 0)

    def is_less_than(self, other):
        if isinstance(other, Number):
            return BoolValue(self.value < other.value, self.pos_start, self.pos_end, self.context)
        else:
            raise RunTimeError(self.pos_start, f"Can't compare values of type {type(self.value)}, {type(other.value)}",
                               self.context)

    def is_greater_or_eq(self, other):
        return BoolValue(1 if not self.is_less_than(other).value else 0)

    def and_(self, other):
        if isinstance(other, Number):
            return BoolValue(self.value and other.value, self.pos_start, self.pos_end, self.context)
        else:
            raise RunTimeError(self.pos_start, f"Can't compare values of type {type(self.value)}, {type(other.value)}",
                               self.context)

    def or_(self, other):
        if isinstance(other, Number):
            return BoolValue(self.value or other.value, self.pos_start, self.pos_end, self.context)
        else:
            raise RunTimeError(self.pos_start, f"Can't compare values of type {type(self.value)}, {type(other.value)}",
                               self.context)

    def not_(self):
        return BoolValue(1 if self.value == 0 else 0, self.pos_start, self.pos_end, self.context)


class IntValue(Number):

    def __init__(self, value, pos_start=None, pos_end=None, context=None):
        super().__init__(int(value), pos_start, pos_end, context)

    def add(self, other):
        if isinstance(other, IntValue):
            return IntValue(self.value + other.value, context=self.context)
        elif isinstance(other, DoubleValue):
            return DoubleValue(self.value + other.value, context=self.context)
        else:
            raise RunTimeError(other.pos_start, f"Can't add values of type int and {type(other)}", self.context)

    def subtract(self, other):
        if isinstance(other, IntValue):
            return IntValue(self.value - other.value, context=self.context)
        elif isinstance(other, DoubleValue):
            return DoubleValue(self.value - other.value, context=self.context)
        else:
            raise RunTimeError(other.pos_start, f"Can't subtract values of type int and {type(other)}", self.context)

    def multiply(self, other):
        if isinstance(other, IntValue):
            return IntValue(self.value * other.value, context=self.context)
        elif isinstance(other, DoubleValue):
            return DoubleValue(self.value * other.value, context=self.context)
        elif isinstance(other, StringValue):
            return StringValue(self.value * other.value, context=self.context)
        else:
            raise RunTimeError(other.pos_start, f"Can't subtract values of type int and {type(other)}", self.context)

    def divide(self, other):
        if isinstance(other, IntValue):
            if other.value == 0:
                raise RunTimeError(other.pos_start, 'Division by zero.', self.context)
            return IntValue(self.value // other.value, context=self.context)
        elif isinstance(other, DoubleValue):
            return DoubleValue(self.value / other.value, context=self.context)
        else:
            raise RunTimeError(other.pos_start, f"Can't subtract values of type int and {type(other)}", self.context)

    def copy(self):
        return IntValue(self.value, self.pos_start, self.pos_end, self.context)


class DoubleValue(Number):

    def __init__(self, value, pos_start=None, pos_end=None, context=None):
        super().__init__(float(value), pos_start, pos_end, context)

    def add(self, other):
        if isinstance(other, Number):
            return DoubleValue(self.value + other.value, context=self.context)

    def subtract(self, other):
        if isinstance(other, Number):
            return IntValue(self.value - other.value, context=self.context)

    def multiply(self, other):
        if isinstance(other, Number):
            return IntValue(self.value * other.value, context=self.context)

    def divide(self, other):
        if isinstance(other, Number):
            if other.value == 0:
                raise RunTimeError(other.pos_start, 'Division by zero.', self.context)
            return IntValue(self.value / other.value, context=self.context)

    def copy(self):
        return DoubleValue(self.value, self.pos_start, self.pos_end, self.context)


class BoolValue(Value):
    def __init__(self, value, pos_start=None, pos_end=None, context=None):
        super().__init__(value, pos_start, pos_end, context)

    def __repr__(self):
        return 'true' if self.value else 'false'


class StringValue(Value):
    def __init__(self, value, pos_start=None, pos_end=None, context=None):
        super().__init__(value, pos_start, pos_end, context)

    def add(self, other):
        if isinstance(other, StringValue):
            return StringValue(self.value + other.value, context=self.context)
        self.raise_runtime_error_for_operation('+', other)

    def multiply(self, other):
        if isinstance(other, IntValue):
            return StringValue(self.value * other.value, context=self.context)
        self.raise_runtime_error_for_operation('*', other)


matching_types = {
    TokenType.T_BOOL: BoolValue,
    TokenType.T_INT: IntValue,
    TokenType.T_DOUBLE: DoubleValue,
    TokenType.T_STRING: StringValue
}

inversed_matching = {
    BoolValue: TokenType.T_BOOL,
    IntValue: TokenType.T_INT,
    DoubleValue: TokenType.T_DOUBLE,
    StringValue: TokenType.T_STRING
}
