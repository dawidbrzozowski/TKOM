import unittest

from interpreting.interpreter import Interpreter
from parsing.parser import Parser
from tests.test_utils import TestSource, TestLexer


class InterpreterTest(unittest.TestCase):
    def setUp(self) -> None:
        self.source = TestSource()
        self.lexer = TestLexer(self.source)
        self.parser = Parser(self.lexer)
        self.interpreter = Interpreter()

    def interpret(self, text):
        self.source.put_text(text)
        self.lexer.lex()
        ast = self.parser.parse()
        return self.interpreter.interpret(ast)

    def test_interpreting_int_value(self):
        result = self.interpret('1;')

        self.assertEqual('1', str(result))

    def test_interpreting_double_value(self):
        result = self.interpret('1.0;')

        self.assertEqual('1.0', str(result))

    def test_interpreting_string_value(self):
        result = self.interpret('"hakuna matata";')

        self.assertEqual('hakuna matata', str(result))

    def test_interpreting_bool_value(self):
        result = self.interpret('true;')

        self.assertEqual('true', str(result))

    def test_interpreting_phys_value(self):
        result = self.interpret('3&|m/s|;')

        self.assertEqual('3*(m^1/s^1)', str(result))

    def test_interpreting_unit_value(self):
        result = self.interpret('|m/s*s*s|;')

        self.assertEqual('(m^1/s^3)', str(result))

    def test_interpreting_if_statement(self):
        statement = """
                int x = 5;
                if (x==5){
                    bool y = true;
                } 
                else{
                    bool y=false;
                } 
                y;
                """
        result = self.interpret(statement)

        self.assertEqual('true', str(result))

    def test_interpreting_while_statement(self):
        statement = """
                    int counter = 1; int x = 2;
                     while(counter < 5){
                        x = x * 2;
                        counter = counter + 1;
                    } 
                    x;
                """
        result = self.interpret(statement)

        self.assertEqual('32', str(result))

    def test_interpreting_function_statement(self):
        statement = """
                function multiply_phys_values(a:phys,b:phys)->phys{
                    return a*b;
                }
                phys x = 1&|m/s|; phys y = 3&|m/s*s|;
                phys result = multiply_phys_values(x,y);
                result;
                """
        result = self.interpret(statement)

        self.assertEqual('3*(m^2/s^3)', str(result))

    def test_interpreting_multiple_ifs_statement(self):
        statement = """
                int x = 5;
                int result = 0;
                if (x < 4){
                    result = 1;
                }
                elseif(x > 6){
                    result = 2;
                }
                elseif (x==5){
                    result = 3;
                }
                result;
        """
        result = self.interpret(statement)

        self.assertEqual('3', str(result))
