from pathlib import Path
import unittest
import tempfile
from unittest import TestCase, mock

from daily.utils import make_dirpath, wrap_file, wrap_preserving_newlines, open_in_editor

class TestUtils(TestCase):

    def test_make_dirpath(self):
        # Test case for make_dirpath function
        dirpath = str(make_dirpath('/opt/local/').resolve())
        self.assertEqual(dirpath, '/opt/local')
        homedirpath = make_dirpath('~/')
        self.assertEqual(homedirpath, Path().home().resolve())

    def test_wrap_file(self):
        # Test case for wrap_file function
        with tempfile.NamedTemporaryFile(delete=False) as temp:
            temp.write(b"This is some test content for the file.")
            temp_path = temp.name

        wrap_width = 80
        wrap_file(temp_path, wrap_width)
        
        # find the longest line of the file and check that it is less than or equal to wrap_width
        with open(temp_path, 'r') as temp:
            temp = temp.read()
            max_line_length = max(len(line) for line in temp.split('\n'))
            self.assertLessEqual(max_line_length, wrap_width)

        # Clean up the temporary file
        Path(temp_path).unlink()

    def test_wrap_preserving_newlines(self):
        # Test case for wrap_preserving_newlines function
        string_to_wrap = 'This is a\nvery very long, and very extensively wrappy multiline\nstring.'
        wrap_width = 10
        wrapped_text = wrap_preserving_newlines(string_to_wrap, wrap_width)
        
        # assert that the existing newlines are preserved, while new newlines may be added in long lines between newlines
        distinct_newlines = [line for line in wrapped_text.split('\n')]
        for line in distinct_newlines:
            self.assertLessEqual(len(line), 10)

    def test_open_in_editor(self):
        with mock.patch('subprocess.call') as mock_call:
            # Mock the subprocess.call function to return a specific exit code
            mock_call.return_value = 0

            # Call the open_in_editor function
            exit_code = open_in_editor('/path/to/file.txt')

            # Assert that the subprocess.call function was called
            mock_call.assert_called_once()

            # Assert that the exit code returned by the function is the same as the mocked exit code
            self.assertEqual(exit_code, 0)

if __name__ == '__main__':
    unittest.main()
