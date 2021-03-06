from errors.error import RunTimeError


class Value:
    type_ = None

    def __init__(self, value, pos_start=None, pos_end=None, context=None):
        self.value = value
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.context = context

    def __repr__(self):
        return str(self.value)

    def set_position(self, pos_start, pos_end):
        self.pos_start = pos_start
        self.pos_end = pos_end

    def set_context(self, context):
        self.context = context

    def add(self, other):
        self._raise_runtime_error_for_action('+', other)

    def subtract(self, other):
        self._raise_runtime_error_for_action('-', other)

    def multiply(self, other):
        self._raise_runtime_error_for_action('*', other)

    def divide(self, other):
        self._raise_runtime_error_for_action('/', other)

    def is_equal(self, other):
        self._raise_runtime_error_for_action('==', other)

    def is_not_equal(self, other):
        self._raise_runtime_error_for_action('!=', other)

    def is_greater_than(self, other):
        self._raise_runtime_error_for_action('>', other)

    def is_less_than(self, other):
        self._raise_runtime_error_for_action('<', other)

    def is_greater_or_eq(self, other):
        self._raise_runtime_error_for_action('>=', other)

    def is_less_or_eq(self, other):
        self._raise_runtime_error_for_action('<=', other)

    def _raise_runtime_error_for_action(self, operator, other):
        raise RunTimeError(self.pos_start,
                           f'{operator} not defined for type {self.type_} and {other.type_}', self.context)

    def and_(self, other):
        self._raise_runtime_error_for_action('and', other)

    def or_(self, other):
        self._raise_runtime_error_for_action('or', other)

    def not_(self):
        raise RunTimeError(self.pos_start, f"'not' not defined for type: {self.type_}", self.context)


class Number(Value):
    def __init__(self, value, pos_start=None, pos_end=None, context=None):
        super().__init__(value, pos_start, pos_end, context)

    def is_equal(self, other):
        if isinstance(other, Number):
            return BoolValue(self.value == other.value, self.context)
        else:
            self._raise_runtime_error_for_action('==', other)

    def is_not_equal(self, other):
        if isinstance(other, Number):
            return BoolValue(self.value != other.value, self.context)
        else:
            self._raise_runtime_error_for_action('!=', other)

    def is_greater_than(self, other):
        if isinstance(other, Number):
            return BoolValue(self.value > other.value, self.pos_start, self.pos_end, self.context)
        else:
            self._raise_runtime_error_for_action('>', other)

    def is_less_or_eq(self, other):
        if isinstance(other, Number):
            return BoolValue(self.value <= other.value, self.pos_start, self.pos_end, self.context)
        else:
            self._raise_runtime_error_for_action('<=', other)

    def is_less_than(self, other):
        if isinstance(other, Number):
            return BoolValue(self.value < other.value, self.pos_start, self.pos_end, self.context)
        else:
            self._raise_runtime_error_for_action('<', other)

    def is_greater_or_eq(self, other):
        if isinstance(other, Number):
            return BoolValue(self.value >= other.value, self.pos_start, self.pos_end, self.context)
        else:
            self._raise_runtime_error_for_action('>=', other)


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
            raise self._raise_runtime_error_for_action('+', other)

    def subtract(self, other):
        if isinstance(other, IntValue):
            return IntValue(self.value - other.value, context=self.context)
        elif isinstance(other, DoubleValue):
            return DoubleValue(self.value - other.value, context=self.context)
        else:
            raise self._raise_runtime_error_for_action('-', other)

    def multiply(self, other):
        if isinstance(other, IntValue):
            return IntValue(self.value * other.value, context=self.context)
        elif isinstance(other, DoubleValue):
            return DoubleValue(self.value * other.value, context=self.context)
        elif isinstance(other, StringValue):
            return StringValue(self.value * other.value, context=self.context)
        else:
            raise self._raise_runtime_error_for_action('*', other)

    def divide(self, other):
        if isinstance(other, IntValue):
            if other.value == 0:
                raise RunTimeError(other.pos_start, 'Division by zero.', self.context)
            return IntValue(self.value // other.value, context=self.context)
        elif isinstance(other, DoubleValue):
            return DoubleValue(self.value / other.value, context=self.context)
        else:
            raise self._raise_runtime_error_for_action('/', other)

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
        else:
            raise self._raise_runtime_error_for_action('+', other)

    def subtract(self, other):
        if isinstance(other, Number):
            return DoubleValue(self.value - other.value, context=self.context)
        else:
            raise self._raise_runtime_error_for_action('-', other)

    def multiply(self, other):
        if isinstance(other, Number):
            return DoubleValue(self.value * other.value, context=self.context)
        else:
            raise self._raise_runtime_error_for_action('*', other)

    def divide(self, other):
        if isinstance(other, Number):
            if other.value == 0:
                raise RunTimeError(other.pos_start, 'Division by zero.', self.context)
            return DoubleValue(self.value / other.value, context=self.context)
        else:
            raise self._raise_runtime_error_for_action('/', other)

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
            self._raise_runtime_error_for_action('and', other)

    def or_(self, other):
        if isinstance(other, Number):
            return BoolValue(self.value or other.value, self.pos_start, self.pos_end, self.context)
        else:
            self._raise_runtime_error_for_action('or', other)

    def not_(self):
        return BoolValue(not self.value, self.pos_start, self.pos_end, self.context)

    def copy(self):
        return BoolValue(self.value, self.pos_start, self.pos_end, self.context)


class StringValue(Value):
    type_ = 'string'

    def __init__(self, value, pos_start=None, pos_end=None, context=None):
        super().__init__(value, pos_start, pos_end, context)

    def add(self, other):
        if isinstance(other, StringValue):
            return StringValue(self.value + other.value, context=self.context)
        self._raise_runtime_error_for_action('+', other)

    def multiply(self, other):
        if isinstance(other, IntValue):
            return StringValue(self.value * other.value, context=self.context)
        self._raise_runtime_error_for_action('*', other)

    def is_equal(self, other):
        if isinstance(other, StringValue):
            return BoolValue(self.value == other.value, context=self.context)
        else:
            self._raise_runtime_error_for_action('==', other)

    def is_not_equal(self, other):
        if isinstance(other, StringValue):
            return BoolValue(self.value != other.value, context=self.context)
        else:
            self._raise_runtime_error_for_action('!=', other)

    def copy(self):
        return StringValue(self.value, self.pos_start, self.pos_end, self.context)


