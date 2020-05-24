from lexer.token.tokens import Position


class LexerError(Exception):
    def __init__(self, illegal_char, position: Position):
        self.illegal_char = illegal_char
        self.position = position

    def print_error_and_exit(self):
        print(f'Error: unexpected character: {self.illegal_char} at: {self.position.print_location()}')
        exit()


class InvalidSyntaxError(Exception):
    def __init__(self, position: Position, message):
        self.pos_start = position
        self.message = message

    def print_error_and_exit(self):
        print(f'Error: invalid syntax at: {self.pos_start.print_location()} {self.message}')
        exit()


class RunTimeError(Exception):
    def __init__(self, position: Position, message, context):
        self.pos_start = position
        self.message = message
        self.context = context

    def print_error_and_exit(self):
        print(f'Error: {self.message} at: {self.pos_start.print_location()}')
        print(self.get_traceback())
        exit()

    def get_traceback(self):
        traceback = ''
        position = self.pos_start
        context = self.context

        while True:
            traceback = f'Line: {str(position.row)}, in {context.name}\n' + traceback
            if context.parent:
                context = context.parent
                position = context.position
            else:
                break
        return 'Traceback (most recent call last): \n' + traceback
