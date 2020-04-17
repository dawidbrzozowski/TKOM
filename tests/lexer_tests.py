from lexer.lexer import LexerBase
import unittest

from lexer.token.tokens import BaseToken, ValueToken
from lexer.token.token_type import TokenType


class LexerTest(unittest.TestCase):

    def setUp(self) -> None:
        self.lexer = LexerBase()

    def test_lex_data_types(self):
        line = "int double char bool string "
        predicted = self.lexer._get_tokens_from_line(line)
        expected = [BaseToken(TokenType.T_INT),
                    BaseToken(TokenType.T_DOUBLE),
                    BaseToken(TokenType.T_CHAR),
                    BaseToken(TokenType.T_BOOL),
                    BaseToken(TokenType.T_STRING)]
        self.assertEqual(expected, predicted)

    def test_lex_punctuation_types(self):
        line = ", . : ; { } ( )"
        predicted = self.lexer._get_tokens_from_line(line)
        expected = [BaseToken(TokenType.T_COMMA),
                    BaseToken(TokenType.T_DOT),
                    BaseToken(TokenType.T_COLON),
                    BaseToken(TokenType.T_SEMICOLON),
                    BaseToken(TokenType.T_LBRACKET),
                    BaseToken(TokenType.T_RBRACKET),
                    BaseToken(TokenType.T_LPARENT),
                    BaseToken(TokenType.T_RPARENT)]
        self.assertEqual(expected, predicted)

    def test_lex_math_operations_types(self):
        line = "+ - * /"
        predicted = self.lexer._get_tokens_from_line(line)
        expected = [BaseToken(TokenType.T_PLUS),
                    BaseToken(TokenType.T_MINUS),
                    BaseToken(TokenType.T_MUL),
                    BaseToken(TokenType.T_DIV)]
        self.assertEqual(expected, predicted)

    def test_math_order_types(self):
        line = "<= < >= > == !="
        predicted = self.lexer._get_tokens_from_line(line)
        expected = [BaseToken(TokenType.T_LESS_OR_EQ),
                    BaseToken(TokenType.T_LESS),
                    BaseToken(TokenType.T_GREATER_OR_EQ),
                    BaseToken(TokenType.T_GREATER),
                    BaseToken(TokenType.T_EQ),
                    BaseToken(TokenType.T_NOT_EQ)]
        self.assertEqual(expected, predicted)

    def test_logical_types(self):
        line = "or and not"
        predicted = self.lexer._get_tokens_from_line(line)
        expected = [BaseToken(TokenType.T_OR),
                    BaseToken(TokenType.T_AND),
                    BaseToken(TokenType.T_NOT)]
        self.assertEqual(expected, predicted)

    def test_other_types(self):
        line = "if else true false return while = void function"
        predicted = self.lexer._get_tokens_from_line(line)
        expected = [BaseToken(TokenType.T_IF),
                    BaseToken(TokenType.T_ELSE),
                    BaseToken(TokenType.T_TRUE),
                    BaseToken(TokenType.T_FALSE),
                    BaseToken(TokenType.T_RETURN),
                    BaseToken(TokenType.T_WHILE),
                    BaseToken(TokenType.T_ASSIGN),
                    BaseToken(TokenType.T_VOID),
                    BaseToken(TokenType.T_FUNCTION)]
        self.assertEqual(expected, predicted)

    def test_specific_to_task_types(self):
        line = "unit phys"
        predicted = self.lexer._get_tokens_from_line(line)
        expected = [BaseToken(TokenType.T_UNIT),
                    BaseToken(TokenType.T_PHYS)]
        self.assertEqual(expected, predicted)

    def test_const_values(self):
        line = "'c' \"string\" 5 2.5"
        predicted = self.lexer._get_tokens_from_line(line)
        expected = [ValueToken(TokenType.VT_CHAR, "'c'"),
                    ValueToken(TokenType.VT_STRING, '"string"'),
                    ValueToken(TokenType.VT_INT, "5"),
                    ValueToken(TokenType.VT_DOUBLE, "2.5")]
        self.assertEqual(expected, predicted)

    def test_id(self):
        line = "var_name x y z"
        predicted = self.lexer._get_tokens_from_line(line)
        expected = [ValueToken(TokenType.VT_ID, "var_name"),
                    ValueToken(TokenType.VT_ID, "x"),
                    ValueToken(TokenType.VT_ID, "y"),
                    ValueToken(TokenType.VT_ID, "z")]
        self.assertEqual(expected, predicted)


if __name__ == '__main__':
    unittest.main()
