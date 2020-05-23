from errors.error import RunTimeError

from lexer.token.token_type_repr import token_type_repr


def check_type_match(defined_type_token, actual_value, context):
    if defined_type_token and not actual_value.type_ == token_type_repr.get(defined_type_token.type):
        raise RunTimeError(defined_type_token.pos_start,
                           f'Expected type: {token_type_repr.get(defined_type_token.type)}'
                           f' got {actual_value.type_} instead.', context)
