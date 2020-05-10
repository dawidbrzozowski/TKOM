from lexer.token.token_type import TokenType

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
    TokenType.T_TRUE: 'True',
    TokenType.T_FALSE: 'False',
    TokenType.T_RETURN: 'return',
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
