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
        all_titles = {
            input_file_path: {
                "title": "Assign standalone",
                "create-org-api": "Create an organization"
            }
        }
        fixed_content = fix_anchor_links_same_page(input_content, all_titles, input_file_path )
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
        expected = {"some-anchor": "A title with anchor", "anchor": "Another title"}
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

    def test_process_seealso_blocks(self):
        input_file_path = os.path.join(
            os.path.dirname(__file__), "md_files", "seealso_block.md"
        )
        expected_output_file_path = os.path.join(
            os.path.dirname(__file__), "md_files", "seealso_block_expected.md"
        )

        with open(input_file_path, "r", encoding="utf-8") as input_file:
            input_content = input_file.read()

        fixed_content = process_seealso_blocks(input_content)

        with open(
            expected_output_file_path, "r", encoding="utf-8"
        ) as expected_output_file:
            expected_output_content = expected_output_file.read()

        self.assertEqual(fixed_content, expected_output_content)

    def test_process_topic_blocks(self):
        input_file_path = os.path.join(
            os.path.dirname(__file__), "md_files", "topic.md"
        )
        expected_output_file_path = os.path.join(
            os.path.dirname(__file__), "md_files", "topic_expected.md"
        )

        with open(input_file_path, "r", encoding="utf-8") as input_file:
            input_content = input_file.read()

        fixed_content = process_topic_blocks(input_content)

        with open(
            expected_output_file_path, "r", encoding="utf-8"
        ) as expected_output_file:
            expected_output_content = expected_output_file.read()

        self.assertEqual(fixed_content, expected_output_content)

    def test_fix_include_path(self):
        input_file_path = os.path.join(
            os.path.dirname(__file__), "rst_files", "include.rst"
        )
        expected_output_file_path = os.path.join(
            os.path.dirname(__file__), "rst_files", "include_expected.rst"
        )

        with open(input_file_path, "r", encoding="utf-8") as input_file:
            input_content = input_file.read()

        fixed_content = update_include_link_rst(input_content,"../includes")

        with open(
            expected_output_file_path, "r", encoding="utf-8"
        ) as expected_output_file:
            expected_output_content = expected_output_file.read()

        self.assertEqual(fixed_content, expected_output_content)

    def test_comment_out_mermaid(self):
        input_file_path = os.path.join(
            os.path.dirname(__file__), "md_files", "mermaid.md"
        )
        expected_output_file_path = os.path.join(
            os.path.dirname(__file__),  "md_files", "mermaid_expected.md"
        )

        with open(input_file_path, "r", encoding="utf-8") as input_file:
            input_content = input_file.read()

        fixed_content = comment_out_mermaid(input_content)

        with open(
            expected_output_file_path, "r", encoding="utf-8"
        ) as expected_output_file:
            expected_output_content = expected_output_file.read()

        self.assertEqual(fixed_content, expected_output_content)

    def test_refs(self):
        titles={
            "/thing/docs/myfolder/mypage":{
                "avn_service_integration_create": "Creating integration"
            }
        }
        input_file_path = os.path.join(
            os.path.dirname(__file__), "md_files", "ref.md"
        )
        expected_output_file_path = os.path.join(
            os.path.dirname(__file__),  "md_files", "ref_expected.md"
        )

        with open(input_file_path, "r", encoding="utf-8") as input_file:
            input_content = input_file.read()

        fixed_content = fix_refs(input_content,titles)

        with open(
            expected_output_file_path, "r", encoding="utf-8"
        ) as expected_output_file:
            expected_output_content = expected_output_file.read()

        self.assertEqual(fixed_content, expected_output_content)

    def test_refs_name(self):
        titles={
            "/thing/docs/myfolder/mypage":{
                "avn_service_integration_create": "Creating integration"
            }
        }
        input_file_path = os.path.join(
            os.path.dirname(__file__), "md_files", "ref_name.md"
        )
        expected_output_file_path = os.path.join(
            os.path.dirname(__file__),  "md_files", "ref_name_expected.md"
        )

        with open(input_file_path, "r", encoding="utf-8") as input_file:
            input_content = input_file.read()

        fixed_content = fix_refs_name(input_content,titles)

        with open(
            expected_output_file_path, "r", encoding="utf-8"
        ) as expected_output_file:
            expected_output_content = expected_output_file.read()

        self.assertEqual(fixed_content, expected_output_content)

    def test_anchor_mapping(self):

        input_file_path = os.path.join(
            os.path.dirname(__file__), "md_files", "anchor_mapping.md"
        )
        expected_output_file_path = os.path.join(
            os.path.dirname(__file__),  "md_files", "anchor_mapping_expected.md"
        )

        with open(input_file_path, "r", encoding="utf-8") as input_file:
            input_content = input_file.read()

        fixed_content = replace_anchors_in_content(input_content)

        with open(
            expected_output_file_path, "r", encoding="utf-8"
        ) as expected_output_file:
            expected_output_content = expected_output_file.read()

        self.assertEqual(fixed_content, expected_output_content)

    def test_dropdowns(self):

        input_file_path = os.path.join(
            os.path.dirname(__file__), "md_files", "dropdown.md"
        )
        expected_output_file_path = os.path.join(
            os.path.dirname(__file__),  "md_files", "dropdown_expected.md"
        )

        with open(input_file_path, "r", encoding="utf-8") as input_file:
            input_content = input_file.read()

        fixed_content = process_dropdowns(input_content)

        with open(
            expected_output_file_path, "r", encoding="utf-8"
        ) as expected_output_file:
            expected_output_content = expected_output_file.read()

        self.assertEqual(fixed_content, expected_output_content)

if __name__ == "__main__":
    unittest.main()
