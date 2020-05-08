from lexer.token.tokens import ValueToken


class NumberNode:
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
