import unittest
import os
import tempfile
from io import StringIO
from contextlib import redirect_stdout
from convert.convert import *


class TestConvert(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.maxDiff = None

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
            os.path.dirname(__file__), "md_files/title_backtick.md"
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

    def test_fix_full_links(self):
        input_file_path = os.path.join(
            os.path.dirname(__file__), "md_files/full_links.md"
        )
        expected_output_file_path = os.path.join(
            os.path.dirname(__file__), "md_files/full_links_expected.md"
        )

        with open(input_file_path, "r", encoding="utf-8") as input_file:
            input_content = input_file.read()

        with open(
            expected_output_file_path, "r", encoding="utf-8"
        ) as expected_output_file:
            expected_output_content = expected_output_file.read()

        updated_content = fix_full_links(input_content)

        self.assertEqual(updated_content, expected_output_content)

    def test_extract_title(self):
        input_file_path = os.path.join(
            os.path.dirname(__file__), "md_files", "extract_title.md"
        )
        extracted_title = extract_title(input_file_path)
        self.assertEqual(extracted_title, "Some title here")

    def test_fix_no_title_link(self):
        input_file_path = os.path.join(
            os.path.dirname(__file__), "md_files", "no_name_links.md"
        )
        expected_output_file_path = os.path.join(
            os.path.dirname(__file__), "md_files/no_name_links_expected.md"
        )
        with open(input_file_path, "r", encoding="utf-8") as input_file:
            input_content = input_file.read()
        repo_path = os.path.join(os.path.dirname(__file__), "md_files")
        fixed_content = fix_no_name_links(input_content, repo_path)
        with open(
            expected_output_file_path, "r", encoding="utf-8"
        ) as expected_output_file:
            expected_output_content = expected_output_file.read()
        self.assertEqual(fixed_content, expected_output_content)

    def test_fix_standalone_links(self):
        input_file_path = os.path.join(
            os.path.dirname(__file__), "md_files", "standalone_links.md"
        )
        expected_output_file_path = os.path.join(
            os.path.dirname(__file__), "md_files/standalone_links_expected.md"
        )
        with open(input_file_path, "r", encoding="utf-8") as input_file:
            input_content = input_file.read()
        repo_path = os.path.join(os.path.dirname(__file__), "md_files")
        fixed_content = fix_standalone_links(input_content)
        with open(
            expected_output_file_path, "r", encoding="utf-8"
        ) as expected_output_file:
            expected_output_content = expected_output_file.read()
        self.assertEqual(fixed_content, expected_output_content)

    def test_process_custom_markup(self):
        input_file_path = os.path.join(
            os.path.dirname(__file__), "md_files", "custom_markup.md"
        )
        expected_output_file_path = os.path.join(
            os.path.dirname(__file__), "md_files", "custom_markup_expected.md"
        )
        with open(input_file_path, "r", encoding="utf-8") as input_file:
            input_content = input_file.read()
        fixed_content = process_custom_markup(input_content)
        with open(
            expected_output_file_path, "r", encoding="utf-8"
        ) as expected_output_file:
            expected_output_content = expected_output_file.read()

        self.assertEqual(fixed_content, expected_output_content)

    def test_anchor_links(self):
        input_file_path = os.path.join(
            os.path.dirname(__file__), "md_files", "anchor_links.md"
        )
        expected_output_file_path = os.path.join(
            os.path.dirname(__file__), "md_files", "anchor_links_expected.md"
        )
        with open(input_file_path, "r", encoding="utf-8") as input_file:
            input_content = input_file.read()
        fixed_content = fix_anchor_links(input_content)
        with open(
            expected_output_file_path, "r", encoding="utf-8"
        ) as expected_output_file:
            expected_output_content = expected_output_file.read()

        self.assertEqual(fixed_content, expected_output_content)

    def test_titles_with_anchors_extraction(self):
        input_file_path = os.path.join(
            os.path.dirname(__file__), "md_files", "title_extractions.md"
        )
        with open(input_file_path, "r", encoding="utf-8") as input_file:
            input_content = input_file.read()
        extracted = extract_titles_with_anchors(input_content)
        expected = {"some-anchor": "A title with anchor", "anchor" : "Another title"}
        self.assertEqual(extracted, expected)

    def test_literal_includes(self):
        input_file_path = os.path.join(
            os.path.dirname(__file__), "md_files", "literal_includes.md"
        )
        expected_output_file_path = os.path.join(
            os.path.dirname(__file__), "md_files", "literal_includes_expected.md"
        )
        with open(input_file_path, "r", encoding="utf-8") as input_file:
            input_content = input_file.read()
        fixed_content = fix_literal_includes(input_content)
        with open(
            expected_output_file_path, "r", encoding="utf-8"
        ) as expected_output_file:
            expected_output_content = expected_output_file.read()

        self.assertEqual(fixed_content, expected_output_content)

if __name__ == "__main__":
    unittest.main()
