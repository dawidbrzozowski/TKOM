from lexer.token.tokens import ValueToken


class IntNode:
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
        return f'({self.left}, {self.operation}, {self.right})'


class UnaryOperationNode:
    def __init__(self, operation, node):
        self.operation = operation
        self.node = node
        self.pos_start = operation.pos_start
        self.pos_end = node.pos_end

    def __repr__(self):
        return f'({self.operation}, {self.node})'


class VarAccessNode:
    def __init__(self, name: ValueToken):
        self.name = name

        self.pos_start = self.name.pos_start
        self.pos_end = self.name.pos_end


class VariableAssignmentNode:
    def __init__(self, name: ValueToken, value: ValueToken):
        self.name = name
        self.value = value

        self.pos_start = self.name.pos_start
        self.pos_end = self.value.pos_end

    def __repr__(self):
        return f'({self.name}: {self.value})'


class IfNode:
    def __init__(self, cases, else_case):
        self.cases = cases
        self.else_case = else_case

        self.pos_start = self.cases[0][0].pos_start
        self.pos_end = (self.else_case or self.cases[-1][0]).pos_end

    def __repr__(self):
        result = ''
        for case in self.cases:
            result += str(case)
        return result


class WhileNode:
    def __init__(self, condition_node, body_node):
        self.condition_node = condition_node
        self.body_node = body_node

        self.pos_start = condition_node.pos_start
        self.pos_end = condition_node.pos_end

    def __repr__(self):
        return f'({self.condition_node}, {self.body_node})'


class FunctionDefinitionNode:
    def __init__(self, function_name: ValueToken, argument_names, body):
        self.function_name = function_name
        self.argument_names = argument_names
        self.body = body

        self.pos_start = self.function_name.pos_start
        self.pos_end = self.body.pos_end


class CallFunctionNode:
    def __init__(self, call_function, arguments):
        self.call_function = call_function
        self.arguments = arguments

        self.pos_start = self.call_function.pos_start

        if len(self.arguments):
            self.pos_end = self.arguments[-1].pos_end
        else:
            self.pos_end = self.call_function.pos_end
