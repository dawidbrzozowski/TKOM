class FunctionDefinition:
    def __init__(self, name, arguments, body, return_type_node, pos_start, pos_end):
        self.name = name
        self.body = body
        self.return_type = return_type_node
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.argument_definitions = arguments


class FunctionArgument:
    def __init__(self, name, type_node):
        self.name = name
        self.type = type_node.type.as_string()