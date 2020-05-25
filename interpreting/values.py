from collections import defaultdict

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
            raise self.raise_runtime_error_for_action('+', other)

    def subtract(self, other):
        if isinstance(other, IntValue):
            return IntValue(self.value - other.value, context=self.context)
        elif isinstance(other, DoubleValue):
            return DoubleValue(self.value - other.value, context=self.context)
        else:
            raise self.raise_runtime_error_for_action('-', other)

    def multiply(self, other):
        if isinstance(other, IntValue):
            return IntValue(self.value * other.value, context=self.context)
        elif isinstance(other, DoubleValue):
            return DoubleValue(self.value * other.value, context=self.context)
        elif isinstance(other, StringValue):
            return StringValue(self.value * other.value, context=self.context)
        else:
            raise self.raise_runtime_error_for_action('*', other)

    def divide(self, other):
        if isinstance(other, IntValue):
            if other.value == 0:
                raise RunTimeError(other.pos_start, 'Division by zero.', self.context)
            return IntValue(self.value // other.value, context=self.context)
        elif isinstance(other, DoubleValue):
            return DoubleValue(self.value / other.value, context=self.context)
        else:
            raise self.raise_runtime_error_for_action('/', other)

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
            raise self.raise_runtime_error_for_action('+', other)

    def subtract(self, other):
        if isinstance(other, Number):
            return DoubleValue(self.value - other.value, context=self.context)
        else:
            raise self.raise_runtime_error_for_action('-', other)

    def multiply(self, other):
        if isinstance(other, Number):
            return DoubleValue(self.value * other.value, context=self.context)
        else:
            raise self.raise_runtime_error_for_action('*', other)

    def divide(self, other):
        if isinstance(other, Number):
            if other.value == 0:
                raise RunTimeError(other.pos_start, 'Division by zero.', self.context)
            return DoubleValue(self.value / other.value, context=self.context)
        else:
            raise self.raise_runtime_error_for_action('/', other)

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


class FunctionDefinition:
    def __init__(self, name, arguments, body, return_type_node, pos_start, pos_end):
        self.name = name
        self.body = body
        self.return_type = return_type_node
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.argument_definitions = arguments


class FunctionArgument:
    def __init__(self, name, type_node):
        self.name = name
        self.type = type_node.type.as_string()


class KeywordValue:
    def __init__(self, value, pos_start=None, pos_end=None):
        self.value = value
        self.pos_start = pos_start
        self.pos_end = pos_end

    def __eq__(self, other):
        if isinstance(other, KeywordValue):
            return self.value == other.value
        else:
            return False


class UnitValue(Value):
    type_ = 'unit'

    def __init__(self, value: defaultdict, pos_start, pos_end, context=None):
        super().__init__(value, pos_start, pos_end, context)
        self.reduce()

    def add(self, other):
        if isinstance(other, UnitValue):
            return UnitValue(self.value, self.pos_start, other.pos_end, context=self.context)
        else:
            raise self.raise_runtime_error_for_action('+', other)

    def subtract(self, other):
        if isinstance(other, UnitValue):
            return UnitValue(self.value, self.pos_start, other.pos_end, context=self.context)
        else:
            raise self.raise_runtime_error_for_action('-', other)

    def multiply(self, other):
        if isinstance(other, UnitValue):
            product = self.value.copy()
            for key in other.value:
                product[key] += other.value.get(key, 0)
            return UnitValue(product, self.pos_start, self.pos_end, context=self.context).reduce()
        else:
            raise self.raise_runtime_error_for_action('*', other)

    def divide(self, other):
        if isinstance(other, UnitValue):
            product = self.value.copy()
            for key in other.value:
                product[key] -= other.value.get(key, 0)
            return UnitValue(product, self.pos_start, self.pos_end, context=self.context).reduce()
        else:
            raise self.raise_runtime_error_for_action('/', other)

    def reduce(self):
        self.value = defaultdict(int, {key: value for key, value in self.value.items() if self.value[key] != 0})
        return self

    def copy(self):
        return UnitValue(self.value, self.pos_start, self.pos_end, self.context)

    def __repr__(self):
        result = '('
        nominator = [key for key in self.value if self.value[key] > 0]
        denominator = [key for key in self.value if self.value[key] < 0]
        nominator_exists = True if len(nominator) else False
        denominator_exists = True if len(denominator) else False
        print(self.value)
        if nominator_exists and not denominator_exists:
            for key in nominator:
                result += f'{key}^{self.value[key]}'
            return result + ')'
        elif nominator_exists and denominator_exists:
            for key in nominator:
                result += f'{key}^{self.value[key]}'
            result += '/'
            for key in denominator:
                result += f'{key}^{-self.value[key]}'
            return result + ')'
        elif denominator_exists and not nominator_exists:
            result += '1/'
            for key in denominator:
                result += f'{key}^{-self.value[key]}'
            return result + ')'
        else:
            return result + ')'

    def is_equal(self, other):
        return BoolValue(self.value == other.value, context=self.context)

    def is_not_equal(self, other):
        return BoolValue(self.value != other.value, context=self.context)


class PhysValue(Value):
    type_ = 'phys'

    def __init__(self, value, unit: UnitValue, pos_start=None, pos_end=None, context=None):
        super().__init__(value, pos_start, pos_end, context)
        self.unit = unit

    def add(self, other):
        if isinstance(other, PhysValue):
            if self.unit.is_equal(other.unit):
                sum = self.value.add(other.value)
                return PhysValue(sum, self.unit, self.pos_start, other.pos_end, context=self.context)
            else:
                raise RunTimeError(self.pos_start, f"Tried to add Phys with units: {self.unit}, {other.unit}",
                                   self.context)
        else:
            raise self.raise_runtime_error_for_action('+', other)

    def subtract(self, other):
        if isinstance(other, PhysValue):
            if self.unit.is_equal(other.unit):
                difference = self.value.subtract(other.value)
                return PhysValue(difference, self.unit, self.pos_start, other.pos_end, context=self.context)
            else:
                raise RunTimeError(self.pos_start, f"Tried to subtract Phys with units: {self.unit}, {other.unit}",
                                   self.context)
        else:
            raise self.raise_runtime_error_for_action('-', other)

    def multiply(self, other):
        if isinstance(other, PhysValue):
            value_product = self.value.multiply(other.value)
            unit_product = self.unit.multiply(other.unit)
            return PhysValue(value_product, unit_product, self.pos_start, self.pos_end, context=self.context)
        else:
            raise self.raise_runtime_error_for_action('*', other)

    def divide(self, other):
        if isinstance(other, PhysValue):
            value_quotient = self.value.divide(other.value)
            unit_quotient = self.unit.divide(other.unit)
            return PhysValue(value_quotient, unit_quotient, self.pos_start, self.pos_end, context=self.context)
        else:
            raise self.raise_runtime_error_for_action('/', other)

    def copy(self):
        return PhysValue(self.value, self.unit, self.pos_start, self.pos_end, self.context)

    def __repr__(self):
        return f'{self.value}*{self.unit}'


class ReturnValue(KeywordValue):
    def __init__(self, value, pos_start, pos_end):
        super().__init__(value, pos_start, pos_end)
        self.type = value.type_
