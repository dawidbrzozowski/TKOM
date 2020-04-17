from enum import Enum, auto


class TokenType(Enum):
    """
    TokenTypes with no value.
    """

    T_IGNORE = auto()
    # data types
    T_INT = auto()
    T_DOUBLE = auto()
    T_CHAR = auto()
    T_BOOL = auto()
    T_STRING = auto()

    # punctuation
    T_COMMA = auto()
    T_DOT = auto()
    T_COLON = auto()
    T_SEMICOLON = auto()
    T_LBRACKET = auto()
    T_RBRACKET = auto()
    T_LPARENT = auto()
    T_RPARENT = auto()

    # math operations
    T_PLUS = auto()
    T_MINUS = auto()
    T_MUL = auto()
    T_DIV = auto()

    # math order types
    T_LESS_OR_EQ = auto()
    T_LESS = auto()
    T_GREATER_OR_EQ = auto()
    T_GREATER = auto()
    T_EQ = auto()
    T_NOT_EQ = auto()

    # logical types
    T_OR = auto()
    T_AND = auto()
    T_NOT = auto()

    # other
    T_ARROW = auto()
    T_EOT = auto()
    T_IF = auto()
    T_ELSE = auto()
    T_TRUE = auto()
    T_FALSE = auto()
    T_RETURN = auto()
    T_WHILE = auto()
    T_ASSIGN = auto()
    T_VOID = auto()
    T_FUNCTION = auto()

    """
    TokenTypes that must have a value
    """

    # tokens specific to task
    T_UNIT = auto()
    T_PHYS = auto()

    # const values
    VT_CHAR = auto()
    VT_STRING = auto()
    VT_DOUBLE = auto()
    VT_INT = auto()
    VT_UNIT = auto()
    VT_PHYS = auto()
    # variable names etc.
    VT_ID = auto()

    def has_value_field(self):
        return True if self.name.startswith("V") else False
