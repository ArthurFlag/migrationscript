# test_convert.py

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
    cleanup,
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
        # Create a test Markdown file
        md_content = "# Test Title\nSome content here."
        md_file = self.create_test_file(md_content, "test_file.md")

        # Call the update_title function
        update_title(md_file, os.path.join(self.test_dir, "log.txt"))

        # Assert that the title has been updated as expected

    def test_convert_rst_to_md(self):
        # Create a test reStructuredText file
        rst_content = "Your test reStructuredText content here."
        rst_file = self.create_test_file(rst_content, "test_file.rst")

        # Call the convert_rst_to_md function
        convert_rst_to_md(rst_file, os.path.join(self.test_dir, "output.md"), os.path.join(self.test_dir, "log.txt"))

        # Assert that the Markdown conversion has been performed

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

    def test_cleanup(self):
        # Create a test Markdown file
        md_content = "# Test Title\nSome content here."
        md_file = self.create_test_file(md_content, "test_file.md")

        # Call the cleanup function
        cleanup(self.test_dir, os.path.join(self.test_dir, "log.txt"))

        # Assert that cleanup has been performed

    def test_copy_folder_contents(self):
        # Create a source folder with contents
        source_folder = os.path.join(self.test_dir, 'source_folder')
        os.makedirs(source_folder)
        self.create_test_file('Test content', os.path.join('source_folder', 'test_file.txt'))

        # Call the copy_folder_contents function
        copy_folder_contents(source_folder, os.path.join(self.test_dir, 'destination_folder'))

        # Assert that contents have been copied

if __name__ == '__main__':
    unittest.main()
