from lexer.token.tokens import ValueToken


class IntNode:
    def __init__(self, token):
        self.token = token
        self.pos_start = token.pos_start
        self.pos_end = token.pos_end

    def __repr__(self):
        return f'{self.token}'


class BoolNode:
    def __init__(self, token):
        self.token = token
        self.pos_start = token.pos_start
        self.pos_end = token.pos_end

    def __repr__(self):
        return f'{self.token}'


class DoubleNode:
    def __init__(self, token):
        self.token = token
        self.pos_start = token.pos_start
        self.pos_end = token.pos_end

    def __repr__(self):
        return f'{self.token}'


class StringNode:
    def __init__(self, token):
        self.token = token
        self.pos_start = token.pos_start
        self.pos_end = token.pos_end

    def __repr__(self):
        return f'{self.token}'


class BinaryOperationNode:
    def __init__(self, left, operation, right):
        self.left = left
        self.operation = operation
        self.right = right
        self.pos_start = left.pos_start
        self.pos_end = right.pos_end

    def __repr__(self):
        return f'({self.left}{self.operation}{self.right})'


class UnaryOperationNode:
    def __init__(self, operation, node):
        self.operation = operation
        self.node = node
        self.pos_start = operation.pos_start
        self.pos_end = node.pos_end

    def __repr__(self):
        return f'({self.operation} {self.node})'


class VariableAccessNode:
    def __init__(self, name: ValueToken):
        self.name = name

        self.pos_start = self.name.pos_start
        self.pos_end = self.name.pos_end

    def __repr__(self):
        return f'{self.name}'


class VariableAssignmentNode:
    def __init__(self, var_type, name: ValueToken, value):
        self.type = var_type
        self.name = name
        self.value = value

        self.pos_start = self.name.pos_start
        self.pos_end = self.value.pos_end

    def __repr__(self):
        return f'(Assignment: {self.type} {self.name}={self.value})'


class IfNode:
    def __init__(self, cases, else_case):
        self.cases = cases
        self.else_case = else_case

        self.pos_start = self.cases[0][0].pos_start
        self.pos_end = (self.else_case or self.cases[-1][0]).pos_end

    def __repr__(self):
        result = '(If:'
        for case in self.cases:
            result += str(case)
        result += str(self.else_case)
        return result + ')'


class WhileNode:
    def __init__(self, condition_node, body_node):
        self.condition_node = condition_node
        self.body_node = body_node

        self.pos_start = condition_node.pos_start
        self.pos_end = condition_node.pos_end

    def __repr__(self):
        return f'(While: {self.condition_node} Do:{self.body_node})'


class FunctionDefinitionNode:
    def __init__(self, function_name: ValueToken, arguments, body, return_type):
        self.function_name = function_name
        self.arguments = arguments
        self.body = body
        self.return_type = return_type

        self.pos_start = self.function_name.pos_start
        self.pos_end = self.body.pos_end

    def __repr__(self):
        return f'(Function:{self.function_name}->{self.return_type} Args:{self.arguments} Body:{self.body})'


class CallFunctionNode:
    def __init__(self, function_name, arguments):
        self.function_name = function_name
        self.arguments = arguments

        self.pos_start = self.function_name.pos_start

        if len(self.arguments):
            self.pos_end = self.arguments[-1].pos_end
        else:
            self.pos_end = self.function_name.pos_end

    def __repr__(self):
        return f'(Call: {self.function_name} Args:{self.arguments})'


class StatementsNode:
    def __init__(self, statements, pos_start, pos_end):
        self.statements = statements

        self.pos_start = pos_start
        self.pos_end = pos_end

    def __repr__(self):
        result = '(' + '\n'.join(str(statement) for statement in self.statements) + ')'
        return result


class ReturnNode:
    def __init__(self, node, pos_start, pos_end):
        self.node = node
        self.pos_start = pos_start
        self.pos_end = pos_end

    def __repr__(self):
        if self.node:
            return f'<Return> {self.node}'
        else:
            return '<Return>'


class TypeNode:
    def __init__(self, token):
        self.type = token.type
        self.pos_start = token.pos_start
        self.pos_end = token.pos_end

    def __repr__(self):
        return f'{self.type}'


class FunctionArgumentNode:
    def __init__(self, argument_name, argument_type):
        self.name = argument_name
        self.type = argument_type

        self.pos_start = argument_name.pos_start
        self.pos_end = argument_type.pos_end

    def __repr__(self):
        return f'({self.name}:{self.type})'


class UnitNode:
    def __init__(self, nominator, denominator, pos_start, pos_end):
        self.nominator = nominator
        self.denominator = denominator
        self.pos_start = pos_start
        self.pos_end = pos_end

    def __repr__(self):
        return f'(Unit: {self.nominator}/{self.denominator})'


class PhysNode:
    def __init__(self, value, unit):
        self.value = value
        self.unit = unit

        self.pos_start = value.pos_start
        self.pos_end = unit.pos_end

    def __repr__(self):
        return f'(Phys: {self.value}*{self.unit})'


class BreakNode:
    def __init__(self, pos_start, pos_end):
        self.pos_start = pos_start
        self.pos_end = pos_end

    def __repr__(self):
        return 'Break'


class ContinueNode:
    def __init__(self, pos_start, pos_end):
        self.pos_start = pos_start
        self.pos_end = pos_end

    def __repr__(self):
        return 'Continue'
