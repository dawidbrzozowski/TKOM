from interpreting.values.basic_values import Value


class KeywordValue(Value):
    def __init__(self, value, pos_start=None, pos_end=None, context=None):
        super().__init__(value, pos_start, pos_end, context)

    def __eq__(self, other):
        if isinstance(other, KeywordValue):
            return self.value == other.value
        else:
            return False


class ReturnValue(KeywordValue):
    def __init__(self, value, pos_start, pos_end):
        super().__init__(value, pos_start, pos_end)
        self.type = value.type_