import unittest

from parsing.parser import Parser
from tests.test_utils import TestSource, TestLexer


class ParserTest(unittest.TestCase):
    def setUp(self) -> None:
        self.source = TestSource()
        self.lexer = TestLexer(self.source)
        self.parser = Parser(self.lexer)

    def parse(self, text):
        self.source.put_text(text)
        self.lexer.lex()
        return self.parser.parse()

    def test_parsing_int_value(self):
        result = self.parse('1;')
        self.assertEqual('(int value:1)', str(result))

    def test_parsing_double_value(self):
        result = self.parse('1.0;')
        self.assertEqual('(double value:1.0)', str(result))

    def test_parsing_string_value(self):
        result = self.parse('"text";')
        self.assertEqual('(string value:text)', str(result))

    def test_parsing_true_value(self):
        result = self.parse('true;')
        self.assertEqual('(true)', str(result))

    def test_parsing_false_value(self):
        result = self.parse('false;')
        self.assertEqual('(false)', str(result))

    def test_parsing_phys_value(self):
        result = self.parse('3&|m/s|;')
        self.assertEqual('((Phys: int value:3*(Unit:m^1s^-1)))', str(result))

    def test_parsing_unit_value(self):
        result = self.parse('|m*m/s*n*x|;')
        self.assertEqual('((Unit:m^2s^-1n^-1x^-1))', str(result))

    def test_parsing_while_statement_value(self):
        result = self.parse('while (true) {1;}')
        self.assertEqual('((While: true Do:(int value:1)))', str(result))

    def test_parsing_if_statement_value(self):
        result = self.parse('if (false) {"x";} else{3;}')
        self.assertEqual('((If:(false, (string value:x))(int value:3)))', str(result))

    def test_parsing_variable_assignment_value(self):
        result = self.parse('int x = 5;')
        self.assertEqual('((Assignment: int identifier:x=int value:5))', str(result))

    def test_parsing_variable_access_value(self):
        result = self.parse('x;')
        self.assertEqual('(identifier:x)', str(result))

    def test_parsing_function_definition(self):
        result = self.parse('function add (a:int, b:int)->int{ return a+b; }')
        self.assertEqual(
            '((Function:identifier:add->int Args:[(identifier:a:int), (identifier:b:int)]'
            ' Body:(<Return> (identifier:a+identifier:b))))',
            str(result))

    def test_parsing_type_int(self):
        result = self.parse('int x = 4;')
        self.assertEqual('((Assignment: int identifier:x=int value:4))', str(result))

    def test_parsing_type_string(self):
        result = self.parse('string s = "string";')
        self.assertEqual('((Assignment: string identifier:s=string value:string))', str(result))

    def test_parsing_type_bool(self):
        result = self.parse('bool v = true;')
        self.assertEqual('((Assignment: bool identifier:v=true))', str(result))

    def test_parsing_type_double(self):
        result = self.parse('double v = 2.0;')
        self.assertEqual('((Assignment: double identifier:v=double value:2.0))', str(result))

    def test_parsing_type_phys(self):
        result = self.parse('phys v = 3&|m/s|;')
        self.assertEqual('((Assignment: phys identifier:v=(Phys: int value:3*(Unit:m^1s^-1))))', str(result))

    def test_parsing_type_unit(self):
        result = self.parse('unit u = |a*s*x/c|;')
        self.assertEqual('((Assignment: unit identifier:u=(Unit:a^1s^1x^1c^-1)))', str(result))


if __name__ == '__main__':
    unittest.main()
