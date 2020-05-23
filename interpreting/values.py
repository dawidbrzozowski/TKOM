from errors.error import RunTimeError


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


class Number(Value):
    def __init__(self, value, pos_start=None, pos_end=None, context=None):
        super().__init__(value, pos_start, pos_end, context)

    def is_equal(self, other):
        if isinstance(other, Number):
            return BoolValue(self.value == other.value, self.pos_start, self.pos_end, self.context)
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


class IntNumber(Number):

    def __init__(self, value, pos_start=None, pos_end=None, context=None):
        super().__init__(int(value), pos_start, pos_end, context)

    def add(self, other):
        if isinstance(other, IntNumber):
            return IntNumber(self.value + other.value, context=self.context)
        elif isinstance(other, DoubleNumber):
            return DoubleNumber(self.value + other.value, context=self.context)
        else:
            raise RunTimeError(other.pos_start, f"Can't add values of type int and {type(other)}", self.context)

    def subtract(self, other):
        if isinstance(other, IntNumber):
            return IntNumber(self.value - other.value, context=self.context)
        elif isinstance(other, DoubleNumber):
            return DoubleNumber(self.value - other.value, context=self.context)
        else:
            raise RunTimeError(other.pos_start, f"Can't subtract values of type int and {type(other)}", self.context)

    def multiply(self, other):
        if isinstance(other, IntNumber):
            return IntNumber(self.value * other.value, context=self.context)
        elif isinstance(other, DoubleNumber):
            return DoubleNumber(self.value * other.value, context=self.context)
        else:
            raise RunTimeError(other.pos_start, f"Can't subtract values of type int and {type(other)}", self.context)

    def divide(self, other):
        if isinstance(other, IntNumber):
            if other.value == 0:
                raise RunTimeError(other.pos_start, 'Division by zero.', self.context)
            return IntNumber(self.value // other.value, context=self.context)
        elif isinstance(other, DoubleNumber):
            return DoubleNumber(self.value / other.value, context=self.context)
        else:
            raise RunTimeError(other.pos_start, f"Can't subtract values of type int and {type(other)}", self.context)

    def copy(self):
        return IntNumber(self.value, self.pos_start, self.pos_end, self.context)


class DoubleNumber(Number):

    def __init__(self, value, pos_start=None, pos_end=None, context=None):
        super().__init__(float(value), pos_start, pos_end, context)

    def add(self, other):
        if isinstance(other, Number):
            return DoubleNumber(self.value + other.value, context=self.context)

    def subtract(self, other):
        if isinstance(other, Number):
            return IntNumber(self.value - other.value, context=self.context)

    def multiply(self, other):
        if isinstance(other, Number):
            return IntNumber(self.value * other.value, context=self.context)

    def divide(self, other):
        if isinstance(other, Number):
            if other.value == 0:
                raise RunTimeError(other.pos_start, 'Division by zero.', self.context)
            return IntNumber(self.value / other.value, context=self.context)

    def copy(self):
        return DoubleNumber(self.value, self.pos_start, self.pos_end, self.context)


class BoolValue(Value):
    def __init__(self, value, pos_start=None, pos_end=None, context=None):
        super().__init__(value, pos_start, pos_end, context)

    def __repr__(self):
        return 'true' if self.value else 'false'
