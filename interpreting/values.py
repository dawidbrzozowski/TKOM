from errors.error import RunTimeError
from lexer.token.token_type_repr import token_type_repr


class Value:
    type_ = None

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
        self.raise_runtime_error_for_action('+', other)

    def subtract(self, other):
        self.raise_runtime_error_for_action('-', other)

    def multiply(self, other):
        self.raise_runtime_error_for_action('*', other)

    def divide(self, other):
        self.raise_runtime_error_for_action('/', other)

    def is_equal(self, other):
        self.raise_runtime_error_for_action('==', other)

    def is_not_equal(self, other):
        self.raise_runtime_error_for_action('!=', other)

    def is_greater_than(self, other):
        self.raise_runtime_error_for_action('>', other)

    def is_less_than(self, other):
        self.raise_runtime_error_for_action('<', other)

    def is_greater_or_eq(self, other):
        self.raise_runtime_error_for_action('>=', other)

    def is_less_or_eq(self, other):
        self.raise_runtime_error_for_action('<=', other)

    def raise_runtime_error_for_action(self, operator, other):
        raise RunTimeError(self.pos_start,
                           f'{operator} not defined for type {self.type_} and {other.type_}', self.context)

    def and_(self, other):
        self.raise_runtime_error_for_action('and', other)

    def or_(self, other):
        self.raise_runtime_error_for_action('or', other)

    def not_(self):
        raise RunTimeError(self.pos_start, f"'not' not defined for type: {self.type_}", self.context)


class Number(Value):
    def __init__(self, value, pos_start=None, pos_end=None, context=None):
        super().__init__(value, pos_start, pos_end, context)

    def is_equal(self, other):
        if isinstance(other, Number):
            return BoolValue(self.value == other.value, self.context)
        else:
            self.raise_runtime_error_for_action('==', other)

    def is_not_equal(self, other):
        if isinstance(other, Number):
            return BoolValue(self.value != other.value, self.context)
        else:
            self.raise_runtime_error_for_action('!=', other)

    def is_greater_than(self, other):
        if isinstance(other, Number):
            return BoolValue(self.value > other.value, self.pos_start, self.pos_end, self.context)
        else:
            self.raise_runtime_error_for_action('>', other)

    def is_less_or_eq(self, other):
        if isinstance(other, Number):
            return BoolValue(self.value <= other.value, self.pos_start, self.pos_end, self.context)
        else:
            self.raise_runtime_error_for_action('<=', other)

    def is_less_than(self, other):
        if isinstance(other, Number):
            return BoolValue(self.value < other.value, self.pos_start, self.pos_end, self.context)
        else:
            self.raise_runtime_error_for_action('<', other)

    def is_greater_or_eq(self, other):
        if isinstance(other, Number):
            return BoolValue(self.value >= other.value, self.pos_start, self.pos_end, self.context)
        else:
            self.raise_runtime_error_for_action('>=', other)


class IntValue(Number):
    type_ = 'int'

    def __init__(self, value, pos_start=None, pos_end=None, context=None):
        value = int(value) if value else None
        super().__init__(value, pos_start, pos_end, context)

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
    type_ = 'double'

    def __init__(self, value, pos_start=None, pos_end=None, context=None):
        value = float(value) if value else None
        super().__init__(value, pos_start, pos_end, context)

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
    type_ = 'bool'

    def __init__(self, value, pos_start=None, pos_end=None, context=None):
        super().__init__(value, pos_start, pos_end, context)

    def __repr__(self):
        return 'true' if self.value else 'false'

    def and_(self, other):
        if isinstance(other, Number):
            return BoolValue(self.value and other.value, self.pos_start, self.pos_end, self.context)
        else:
            self.raise_runtime_error_for_action('and', other)

    def or_(self, other):
        if isinstance(other, Number):
            return BoolValue(self.value or other.value, self.pos_start, self.pos_end, self.context)
        else:
            self.raise_runtime_error_for_action('or', other)

    def not_(self):
        return BoolValue(not self.value, self.pos_start, self.pos_end, self.context)


class StringValue(Value):
    type_ = 'string'

    def __init__(self, value, pos_start=None, pos_end=None, context=None):
        super().__init__(value, pos_start, pos_end, context)

    def add(self, other):
        if isinstance(other, StringValue):
            return StringValue(self.value + other.value, context=self.context)
        self.raise_runtime_error_for_action('+', other)

    def multiply(self, other):
        if isinstance(other, IntValue):
            return StringValue(self.value * other.value, context=self.context)
        self.raise_runtime_error_for_action('*', other)


class Function:
    def __init__(self, name, arguments, body, return_type_node, context, pos_start, pos_end):
        self.name = name
        self.body = body
        self.return_type = return_type_node
        self.context = context
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.argument_definitions = arguments


class FunctionArgument:
    def __init__(self, name, type_node):
        self.name = name
        self.type = token_type_repr.get(type_node.type)


class ReturnValue:
    def __init__(self, value):
        self.value = value
        self.type = value.type_
