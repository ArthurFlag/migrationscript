import unittest
import os
import tempfile
from io import StringIO
from contextlib import redirect_stdout
from convert.convert import (
    delete_folder,
    update_title,
    convert_rst_to_md,
    fix_admonitions,
    cleanup_interpreted_text,
    cleanup_md,
    copy_folder_contents,
)

class TestConvert(unittest.TestCase):

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        delete_folder(self.test_dir)

    def create_test_file(self, content, file_name):
        file_path = os.path.join(self.test_dir, file_name)
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
        return file_path

    def test_update_title(self):
        # Define file paths
        input_file_path =  os.path.join(os.path.dirname(__file__), 'md_files/title_test.md')
        expected_output_file_path =  os.path.join(os.path.dirname(__file__), 'md_files/title_test_expected.md')

        # Read content from the input file
        with open(input_file_path, 'r', encoding='utf-8') as input_file:
            input_content = input_file.read()

        # Get the expected output content from the expected output file
        with open(expected_output_file_path, 'r', encoding='utf-8') as expected_output_file:
            expected_output_content = expected_output_file.read()

        # Apply the update_title function to the input content
        updated_content = update_title(input_content)

        # Assert that the updated content matches the expected output content
        self.assertEqual(updated_content, expected_output_content)

    def test_update_title_backticks(self):
        # Define file paths
        input_file_path =  os.path.join(os.path.dirname(__file__), 'md_files/title_backtick_test.md')
        expected_output_file_path =  os.path.join(os.path.dirname(__file__), 'md_files/title_backtick_expected.md')

        # Read content from the input file
        with open(input_file_path, 'r', encoding='utf-8') as input_file:
            input_content = input_file.read()

        # Get the expected output content from the expected output file
        with open(expected_output_file_path, 'r', encoding='utf-8') as expected_output_file:
            expected_output_content = expected_output_file.read()

        # Apply the update_title function to the input content
        updated_content = update_title(input_content)

        # Assert that the updated content matches the expected output content
        self.assertEqual(updated_content, expected_output_content)

    def test_fix_admonitions(self):
        # Create a test Markdown file with admonitions
        md_content = "Some content\n::: title\nAdmonition content\n:::"
        md_file = self.create_test_file(md_content, "test_file.md")

        # Call the fix_admonitions function
        fix_admonitions(md_file)

        # Assert that admonitions have been fixed

    def test_cleanup_interpreted_text(self):
        # Create a test Markdown file with interpreted text
        md_content = "Some `interpreted-text` content here."
        md_file = self.create_test_file(md_content, "test_file.md")

        # Call the cleanup_interpreted_text function
        cleanup_interpreted_text(md_file)

        # Assert that interpreted text has been cleaned up



if __name__ == '__main__':
    unittest.main()
