from collections import defaultdict

from errors.error import RunTimeError
from interpreting.values.basic_values import Value, BoolValue


class UnitValue(Value):
    type_ = 'unit'

    def __init__(self, value: defaultdict, pos_start, pos_end, context=None):
        super().__init__(value, pos_start, pos_end, context)
        self.reduce()

    def add(self, other):
        if isinstance(other, UnitValue):
            return UnitValue(self.value, self.pos_start, other.pos_end, context=self.context)
        else:
            raise self._raise_runtime_error_for_action('+', other)

    def subtract(self, other):
        if isinstance(other, UnitValue):
            return UnitValue(self.value, self.pos_start, other.pos_end, context=self.context)
        else:
            raise self._raise_runtime_error_for_action('-', other)

    def multiply(self, other):
        if isinstance(other, UnitValue):
            product = self.value.copy()
            for key in other.value:
                product[key] += other.value.get(key, 0)
            return UnitValue(product, self.pos_start, self.pos_end, context=self.context).reduce()
        else:
            raise self._raise_runtime_error_for_action('*', other)

    def divide(self, other):
        if isinstance(other, UnitValue):
            product = self.value.copy()
            for key in other.value:
                product[key] -= other.value.get(key, 0)
            return UnitValue(product, self.pos_start, self.pos_end, context=self.context).reduce()
        else:
            raise self._raise_runtime_error_for_action('/', other)

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
            raise self._raise_runtime_error_for_action('+', other)

    def subtract(self, other):
        if isinstance(other, PhysValue):
            if self.unit.is_equal(other.unit):
                difference = self.value.subtract(other.value)
                return PhysValue(difference, self.unit, self.pos_start, other.pos_end, context=self.context)
            else:
                raise RunTimeError(self.pos_start, f"Tried to subtract Phys with units: {self.unit}, {other.unit}",
                                   self.context)
        else:
            raise self._raise_runtime_error_for_action('-', other)

    def multiply(self, other):
        if isinstance(other, PhysValue):
            value_product = self.value.multiply(other.value)
            unit_product = self.unit.multiply(other.unit)
            return PhysValue(value_product, unit_product, self.pos_start, self.pos_end, context=self.context)
        else:
            raise self._raise_runtime_error_for_action('*', other)

    def divide(self, other):
        if isinstance(other, PhysValue):
            value_quotient = self.value.divide(other.value)
            unit_quotient = self.unit.divide(other.unit)
            return PhysValue(value_quotient, unit_quotient, self.pos_start, self.pos_end, context=self.context)
        else:
            raise self._raise_runtime_error_for_action('/', other)

    def copy(self):
        return PhysValue(self.value, self.unit, self.pos_start, self.pos_end, self.context)

    def is_equal(self, other):
        is_eq = self.value.is_equal(other.value).value and self.unit.is_equal(other.unit).value
        return BoolValue(is_eq, context=self.context)

    def is_not_equal(self, other):
        is_not_eq = not self.value.is_equal(other.value).value or not self.unit.is_equal(other.unit).value

        return BoolValue(is_not_eq, context=self.context)

    def __repr__(self):
        return f'{self.value}*{self.unit}'