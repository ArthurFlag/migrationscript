import unittest
import os
import tempfile
from io import StringIO
from contextlib import redirect_stdout
from convert.convert import (
    delete_folder,
    update_title,
    fix_admonitions,
    cleanup_interpreted_text_doc,
    cleanup_interpreted_text_ref,
)


class TestConvert(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.maxDiff = None

    def tearDown(self):
        delete_folder(self.test_dir)

    def create_test_file(self, content, file_name):
        file_path = os.path.join(self.test_dir, file_name)
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(content)
        return file_path

    def test_update_title(self):
        input_file_path = os.path.join(
            os.path.dirname(__file__), "md_files/title_test.md"
        )
        expected_output_file_path = os.path.join(
            os.path.dirname(__file__), "md_files/title_test_expected.md"
        )

        with open(input_file_path, "r", encoding="utf-8") as input_file:
            input_content = input_file.read()

        with open(
            expected_output_file_path, "r", encoding="utf-8"
        ) as expected_output_file:
            expected_output_content = expected_output_file.read()

        updated_content = update_title(input_content)

        self.assertEqual(updated_content, expected_output_content)

    def test_update_title_backticks(self):
        input_file_path = os.path.join(
            os.path.dirname(__file__), "md_files/title_backtick_test.md"
        )
        expected_output_file_path = os.path.join(
            os.path.dirname(__file__), "md_files/title_backtick_expected.md"
        )

        with open(input_file_path, "r", encoding="utf-8") as input_file:
            input_content = input_file.read()

        with open(
            expected_output_file_path, "r", encoding="utf-8"
        ) as expected_output_file:
            expected_output_content = expected_output_file.read()

        updated_content = update_title(input_content)

        self.assertEqual(updated_content, expected_output_content)

    def test_fix_admonitions(self):
        md_content = "Some content\n::: title\nAdmonition content\n:::"
        md_file = self.create_test_file(md_content, "test_file.md")

        fix_admonitions(md_file)

    def test_cleanup_interpreted_text_ref(self):
        input_file_path = os.path.join(
            os.path.dirname(__file__), "md_files/interpreted_ref_text_test.md"
        )
        expected_output_file_path = os.path.join(
            os.path.dirname(__file__), "md_files/interpreted_ref_text_expected.md"
        )

        with open(input_file_path, "r", encoding="utf-8") as input_file:
            input_content = input_file.read()

        with open(
            expected_output_file_path, "r", encoding="utf-8"
        ) as expected_output_file:
            expected_output_content = expected_output_file.read()

        updated_content = cleanup_interpreted_text_ref(input_content)

        self.assertEqual(updated_content, expected_output_content)

    def test_cleanup_interpreted_text_doc(self):
       input_file_path = os.path.join(
            os.path.dirname(__file__), "md_files/interpreted_doc_text_test.md"
        )
        expected_output_file_path = os.path.join(
            os.path.dirname(__file__), "md_files/interpreted_doc_text_expected.md"
        )

        with open(input_file_path, "r", encoding="utf-8") as input_file:
            input_content = input_file.read()

        with open(
            expected_output_file_path, "r", encoding="utf-8"
        ) as expected_output_file:
            expected_output_content = expected_output_file.read()

        updated_content = cleanup_interpreted_text_ref(input_content)

        self.assertEqual(updated_content, expected_output_content)

if __name__ == "__main__":
    unittest.main()