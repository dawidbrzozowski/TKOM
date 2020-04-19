import re
import unittest
from lexer.regex2token import regex2token
from lexer.token.tokens import BaseToken, ValueToken
from lexer.token.token_type import TokenType


class TestRegex(unittest.TestCase):
    def setUp(self) -> None:
        self.regex2token = regex2token
        self.regex2token_compiled = {}
        for regex in regex2token:
            regex_compiled = re.compile(regex)
            self.regex2token_compiled[regex_compiled] = regex2token[regex]

    def find_token(self, line):
        token_args = self._find_token_args(line)
        if not token_args:
            return None
        token_type, value = token_args
        if token_type.has_value_field():
            token = ValueToken(token_type, value)
        else:
            token = BaseToken(token_type)
        return token

    def _find_token_args(self, line):
        for regex in self.regex2token_compiled:
            match = regex.match(line)
            if match:
                token_type = self.regex2token_compiled[regex]
                value = match.group(0)
                return token_type, value
        return None

    def test_double_value(self):
        line = "2.5"
        token = self.find_token(line)
        expected = ValueToken(TokenType.VT_DOUBLE, "2.5")
        self.assertEqual(expected, token)

    def test_string_value(self):
        line = '"test string"'
        token = self.find_token(line)
        expected = ValueToken(TokenType.VT_STRING, '"test string"')
        self.assertEqual(expected, token)

    def test_char_value(self):
        line = "'c'"
        token = self.find_token(line)
        expected = ValueToken(TokenType.VT_CHAR, "'c'")
        self.assertEqual(expected, token)

    def test_int_value(self):
        line = "152"
        token = self.find_token(line)
        expected = ValueToken(TokenType.VT_INT, "152")
        self.assertEqual(expected, token)

    def test_int(self):
        line = "int"
        token = self.find_token(line)
        expected = BaseToken(TokenType.T_INT)
        self.assertEqual(expected, token)

    def test_double(self):
        line = "double"
        token = self.find_token(line)
        expected = BaseToken(TokenType.T_DOUBLE)
        self.assertEqual(expected, token)

    def test_char(self):
        line = "char"
        token = self.find_token(line)
        expected = BaseToken(TokenType.T_CHAR)
        self.assertEqual(expected, token)

    def test_string(self):
        line = "string"
        token = self.find_token(line)
        expected = BaseToken(TokenType.T_STRING)
        self.assertEqual(expected, token)

    def test_bool(self):
        line = "bool"
        token = self.find_token(line)
        expected = BaseToken(TokenType.T_BOOL)
        self.assertEqual(expected, token)

    def test_comma(self):
        line = ","
        token = self.find_token(line)
        expected = BaseToken(TokenType.T_COMMA)
        self.assertEqual(expected, token)

    def test_dot(self):
        line = "."
        token = self.find_token(line)
        expected = BaseToken(TokenType.T_DOT)
        self.assertEqual(expected, token)

    def test_colon(self):
        line = ":"
        token = self.find_token(line)
        expected = BaseToken(TokenType.T_COLON)
        self.assertEqual(expected, token)

    def test_semicolon(self):
        line = ";"
        token = self.find_token(line)
        expected = BaseToken(TokenType.T_SEMICOLON)
        self.assertEqual(expected, token)

    def test_lbracket(self):
        line = "{"
        token = self.find_token(line)
        expected = BaseToken(TokenType.T_LBRACKET)
        self.assertEqual(expected, token)

    def test_rbracket(self):
        line = "}"
        token = self.find_token(line)
        expected = BaseToken(TokenType.T_RBRACKET)
        self.assertEqual(expected, token)

    def test_lparent(self):
        line = "("
        token = self.find_token(line)
        expected = BaseToken(TokenType.T_LPARENT)
        self.assertEqual(expected, token)

    def test_rparent(self):
        line = ")"
        token = self.find_token(line)
        expected = BaseToken(TokenType.T_RPARENT)
        self.assertEqual(expected, token)

    def test_plus(self):
        line = "+"
        token = self.find_token(line)
        expected = BaseToken(TokenType.T_PLUS)
        self.assertEqual(expected, token)

    def test_minus(self):
        line = "-"
        token = self.find_token(line)
        expected = BaseToken(TokenType.T_MINUS)
        self.assertEqual(expected, token)

    def test_mul(self):
        line = "*"
        token = self.find_token(line)
        expected = BaseToken(TokenType.T_MUL)
        self.assertEqual(expected, token)

    def test_div(self):
        line = "/"
        token = self.find_token(line)
        expected = BaseToken(TokenType.T_DIV)
        self.assertEqual(expected, token)

    def test_less_or_eq(self):
        line = "<="
        token = self.find_token(line)
        expected = BaseToken(TokenType.T_LESS_OR_EQ)
        self.assertEqual(expected, token)

    def test_less(self):
        line = "<"
        token = self.find_token(line)
        expected = BaseToken(TokenType.T_LESS)
        self.assertEqual(expected, token)

    def test_eq(self):
        line = "=="
        token = self.find_token(line)
        expected = BaseToken(TokenType.T_EQ)
        self.assertEqual(expected, token)

    def test_not_eq(self):
        line = "!="
        token = self.find_token(line)
        expected = BaseToken(TokenType.T_NOT_EQ)
        self.assertEqual(expected, token)

    def test_greater_or_eq(self):
        line = ">="
        token = self.find_token(line)
        expected = BaseToken(TokenType.T_GREATER_OR_EQ)
        self.assertEqual(expected, token)

    def test_greater(self):
        line = ">"
        token = self.find_token(line)
        expected = BaseToken(TokenType.T_GREATER)
        self.assertEqual(expected, token)

    def test_or(self):
        line = "or"
        token = self.find_token(line)
        expected = BaseToken(TokenType.T_OR)
        self.assertEqual(expected, token)

    def test_and(self):
        line = "and"
        token = self.find_token(line)
        expected = BaseToken(TokenType.T_AND)
        self.assertEqual(expected, token)

    def test_not(self):
        line = "not"
        token = self.find_token(line)
        expected = BaseToken(TokenType.T_NOT)
        self.assertEqual(expected, token)

    def test_if(self):
        line = "if"
        token = self.find_token(line)
        expected = BaseToken(TokenType.T_IF)
        self.assertEqual(expected, token)

    def test_else(self):
        line = "else"
        token = self.find_token(line)
        expected = BaseToken(TokenType.T_ELSE)
        self.assertEqual(expected, token)

    def test_true(self):
        line = "true"
        token = self.find_token(line)
        expected = BaseToken(TokenType.T_TRUE)
        self.assertEqual(expected, token)

    def test_false(self):
        line = "false"
        token = self.find_token(line)
        expected = BaseToken(TokenType.T_FALSE)
        self.assertEqual(expected, token)

    def test_return(self):
        line = "return"
        token = self.find_token(line)
        expected = BaseToken(TokenType.T_RETURN)
        self.assertEqual(expected, token)

    def test_while(self):
        line = "while"
        token = self.find_token(line)
        expected = BaseToken(TokenType.T_WHILE)
        self.assertEqual(expected, token)

    def test_assign(self):
        line = "="
        token = self.find_token(line)
        expected = BaseToken(TokenType.T_ASSIGN)
        self.assertEqual(expected, token)

    def test_void(self):
        line = "void"
        token = self.find_token(line)
        expected = BaseToken(TokenType.T_VOID)
        self.assertEqual(expected, token)

    def test_function(self):
        line = "function"
        token = self.find_token(line)
        expected = BaseToken(TokenType.T_FUNCTION)
        self.assertEqual(expected, token)

    def test_arrow(self):
        line = "->"
        token = self.find_token(line)
        expected = BaseToken(TokenType.T_ARROW)
        self.assertEqual(expected, token)

    def test_unit(self):
        line = "unit"
        token = self.find_token(line)
        expected = BaseToken(TokenType.T_UNIT)
        self.assertEqual(expected, token)

    def test_unit_value(self):
        line = "|m/s*s|"
        token = self.find_token(line)
        expected = ValueToken(TokenType.VT_UNIT, "|m/s*s|")
        self.assertEqual(expected, token)


if __name__ == '__main__':
    unittest.main()
