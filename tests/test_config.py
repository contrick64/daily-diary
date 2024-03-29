import time
import unittest
from daily.config import load_conf, parse_time_format_string

class ConfigTests(unittest.TestCase):

    def test_load_conf(self):
        config = load_conf()
        self.assertIsInstance(config, dict)
        self.assertIn("journal_dir", config)
        self.assertIn("filename_format", config)
        self.assertIn("h1_title_format", config)
        self.assertIn("h2_inline_format", config)
        self.assertIn("h2_format", config)
        self.assertIn("wrap_width", config)

        # Add more specific assertions for each key-value pair in the config dictionary
        self.assertEqual(config["journal_dir"], "~/notes/daily")
        self.assertEqual(config["filename_format"], "%Y-%m-%d_log.md")
        self.assertEqual(config["h1_title_format"], "%Y-%m-%d daily log")
        self.assertEqual(config["h2_inline_format"], '%I:%M %p %o (%O)\n%E')
        self.assertEqual(config["h2_format"], '%I:%M %p')
        self.assertEqual(config["wrap_width"], 54)

    def test_parse_time_format_string(self):
        """
        Test the parse_time_format_string function.

        This function takes a time format string and replaces the custom directives with the provided values.
        It returns the formatted string.

        """
        # Test case 1: No custom directives
        time_format = "%Y-%m-%d %H:%M:%S"
        formatted_string = parse_time_format_string(time_format)
        self.assertEqual(formatted_string, time.strftime(time_format))

        # Test case 2: Custom directives present
        time_format = "%I:%M %p %o (%O)\n%E"
        kwargs = {
            'mood_char': 'A',
            'mood_words': 'Happy',
            'entry': 'Hello World!'
        }
        expected_string = f"{time.strftime('%I:%M %p')} A (Happy)\nHello World!"
        formatted_string = parse_time_format_string(time_format, **kwargs)
        self.assertEqual(formatted_string, expected_string)

if __name__ == "__main__":
    unittest.main()