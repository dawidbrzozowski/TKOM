from errors.error import RunTimeError
from interpreting.values import BoolValue, IntNumber, DoubleNumber
from lexer.token.token_type import TokenType
from lexer.token.token_type_repr import token_type_repr

matching_types = {
    TokenType.T_BOOL: BoolValue,
    TokenType.T_INT: IntNumber,
    TokenType.T_DOUBLE: DoubleNumber,
}

inversed_matching = {
    BoolValue: TokenType.T_BOOL,
    IntNumber: TokenType.T_INT,
    DoubleNumber: TokenType.T_DOUBLE
}


def check_type_match(defined_type_token, actual_value, context):
    if not type(actual_value) == matching_types.get(defined_type_token.type):
        raise RunTimeError(defined_type_token.pos_start,
                           f'Expected type: {token_type_repr.get(defined_type_token.type)}'
                           f' got {token_type_repr.get(inversed_matching[type(actual_value)])} instead.', context)
