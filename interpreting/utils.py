from errors.error import RunTimeError
from interpreting.values import FunctionDefinition


def check_argument_correctness(function: FunctionDefinition, actual_arguments, context):
    check_arguments_amount(function, actual_arguments, context)
    check_argument_types(function, actual_arguments, context)


def check_arguments_amount(function: FunctionDefinition, actual_arguments, context):
    if len(actual_arguments) != len(function.argument_definitions):
        raise RunTimeError(function.pos_start,
                           f'Wrong amount of arguments. Expected: {len(function.argument_definitions)}.'
                           f' Got: {len(actual_arguments)}', context)


def check_argument_types(function: FunctionDefinition, actual_arguments, context):
    for argument, defined_argument in zip(actual_arguments, function.argument_definitions):
        if argument.type_ != defined_argument.type:
            raise RunTimeError(function.pos_start,
                               f'Wrong type of argument. Expected {defined_argument.type} 'f'got: {argument.type_}',
                               context)


def check_return_type(function: FunctionDefinition, result, context):
    if str(function.return_type) == 'void' and result.type_ is not None:
        raise RunTimeError(function.return_type.pos_start,
                           f'Expected return type: {str(function.return_type)} got {result.type_}', context)
    elif result.type_ != str(function.return_type.type):
        raise RunTimeError(function.return_type.pos_start,
                           f'Expected return type: {str(function.return_type)} got {result.type_}', context)
