from enum import Enum, auto


class TokenType(Enum):
    """
    TokenTypes with no value.
    """

    def has_value_field(self):
        return True if self.name.startswith("V") else False

    def as_string(self):
        return token_type_repr.get(self)

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
    T_VERTICAL_BAR = auto()
    T_AMPERSAND = auto()

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
    T_ELSEIF = auto()
    T_TRUE = auto()
    T_FALSE = auto()
    T_RETURN = auto()
    T_WHILE = auto()
    T_ASSIGN = auto()
    T_VOID = auto()
    T_FUNCTION = auto()
    T_BREAK = auto()
    T_CONTINUE = auto()

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
    # variable names etc.
    VT_ID = auto()


token_type_repr = {
    # data types
    TokenType.T_INT: 'int',
    TokenType.T_DOUBLE: 'double',
    TokenType.T_CHAR: 'char',
    TokenType.T_BOOL: 'bool',
    TokenType.T_STRING: 'string',

    # punctuation
    TokenType.T_COMMA: ',',
    TokenType.T_DOT: '.',
    TokenType.T_COLON: ':',
    TokenType.T_SEMICOLON: ';',
    TokenType.T_LBRACKET: '{',
    TokenType.T_RBRACKET: '}',
    TokenType.T_LPARENT: '(',
    TokenType.T_RPARENT: ')',
    TokenType.T_VERTICAL_BAR: '|',
    TokenType.T_AMPERSAND: '&',

    # math operations
    TokenType.T_PLUS: '+',
    TokenType.T_MINUS: '-',
    TokenType.T_MUL: '*',
    TokenType.T_DIV: '/',

    # math order types
    TokenType.T_LESS_OR_EQ: '<=',
    TokenType.T_LESS: '<',
    TokenType.T_GREATER_OR_EQ: '>=',
    TokenType.T_GREATER: '>',
    TokenType.T_EQ: '==',
    TokenType.T_NOT_EQ: '!=',

    # logical types
    TokenType.T_OR: 'or',
    TokenType.T_AND: 'and',
    TokenType.T_NOT: 'not',

    # other
    TokenType.T_ARROW: '->',
    TokenType.T_EOT: 'End of text',
    TokenType.T_IF: 'if',
    TokenType.T_ELSE: 'else',
    TokenType.T_ELSEIF: 'elseif',
    TokenType.T_TRUE: 'true',
    TokenType.T_FALSE: 'false',
    TokenType.T_RETURN: 'return',
    TokenType.T_BREAK: 'break',
    TokenType.T_CONTINUE: 'continue',
    TokenType.T_WHILE: 'while',
    TokenType.T_ASSIGN: '=',
    TokenType.T_VOID: 'void',
    TokenType.T_FUNCTION: 'function',
    TokenType.T_UNIT: 'unit',
    TokenType.T_PHYS: 'phys',

    # const values
    TokenType.VT_CHAR: 'char value',
    TokenType.VT_STRING: 'string value',
    TokenType.VT_DOUBLE: 'double value',
    TokenType.VT_INT: 'int value',
    # variable names etc.
    TokenType.VT_ID: 'identifier',
}
