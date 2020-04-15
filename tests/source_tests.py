from lexer.stream import FileSource, StdInSource

import unittest

TEST_SOURCE_1_LINE = 'test_files/testfile1.txt'
TEST_SOURCE_3_LINES = 'test_files/testfile3.txt'


class TestSource(unittest.TestCase):

    def test_file_source(self):
        file_source = FileSource(TEST_SOURCE_1_LINE)
        text = file_source.read_line()
        self.assertEqual("test text", text, msg='Error in first line.')
        self.assertEqual(True, file_source.is_end_of_text(), 'Error when checking EOF')

    def test_file_source_three_lines(self):
        file_source = FileSource(TEST_SOURCE_3_LINES)
        text = file_source.read_line()
        self.assertEqual("test text1\n", text, msg='Error in first line.')
        text = file_source.read_line()
        self.assertEqual("test text2\n", text, msg='Error in second line.')
        file_source.read_line()
        self.assertEqual(True, file_source.is_end_of_text(), 'Error when checking EOF')


if __name__ == '__main__':
    unittest.main()
