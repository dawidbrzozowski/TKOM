from lexer.source import FileSource

import unittest

TEST_SOURCE_1_LINE = 'test_files/testfile1line.txt'
TEST_SOURCE_2_LINES = 'test_files/testfile2lines.txt'


class TestSource(unittest.TestCase):

    def test_file_source(self):
        file_source = FileSource(TEST_SOURCE_1_LINE)
        text = file_source.read_line()
        self.assertEqual("test int 5 double 1", text, msg='Error in first line.')
        self.assertEqual(True, file_source.is_end_of_text(), 'Error when checking EOF')

    def test_file_source_three_lines(self):
        file_source = FileSource(TEST_SOURCE_2_LINES)
        text = file_source.read_line()
        self.assertEqual("test text1\n", text, msg='Error in first line.')
        text = file_source.read_line()
        self.assertEqual("test text2", text, msg='Error in second line.')
        self.assertEqual(True, file_source.is_end_of_text(), msg='Error when checking EOF')


if __name__ == '__main__':
    unittest.main()
