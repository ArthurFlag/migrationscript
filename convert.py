import os
import sys
import pypandoc
import re
import shutil

def delete_folder(path):
    try:
        # Check if the folder exists
        if os.path.exists(path):
            # Use shutil.rmtree to delete the folder and its contents
            shutil.rmtree(path)
            print(f"Folder at {path} successfully deleted.")
        else:
            print(f"Folder at {path} does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")

def update_title(md_file_path, log_file_path):
    """
    Extract the H1 title from a Markdown file.
    """
    with open(md_file_path, 'r', encoding='utf-8') as md_file:
        content = md_file.read()

    # Find the first H1 title
    match = re.search(r'^#\s*(.*)', content, re.MULTILINE)
    if match:
        # Create YAML front matter using only group 1
        yaml_front_matter = f"---\ntitle: {match.group(1)}\n---\n\n"

        # Remove the first H1 title
        content_lines = content.split('\n', 1)
        if re.match(r'^#\s', content_lines[0]):
            content = content_lines[1]

            # Write the combined content to the Markdown file
            with open(md_file_path, 'w', encoding='utf-8') as md_file:
                md_file.write(yaml_front_matter)
                md_file.write(content)

    else:
        with open(log_file_path, 'a', encoding='utf-8') as log:
            log.write(f"Error in file: {md_file_path}\n"
                      "No H1 title found. Please check and correct.\n\n")

    return None

def convert_rst_to_md(input_path, output_path, log_file):
    """
    Convert a reStructuredText file to Markdown using pypandoc.
    """

    # Convert the rest of the file to Markdown
    content = pypandoc.convert_file(input_path, 'md')
    with open(output_path, 'w', encoding='utf-8') as md_file:
      md_file.write(content)

def fix_admonitions(md_file_path):
    """
    Fix admonitions in a Markdown file.
    Remove lines containing "::: title" followed by a generic title and ":::".
    """
    with open(md_file_path, 'r', encoding='utf-8') as md_file:
        md_content = md_file.read()

    # Remove lines containing "::: title" and ":::" for various admonition types
    updated_content = re.sub(
        r'^\s*:::\s+title\s*$(.*?)^\s*:::\s*$', '', md_content, flags=re.MULTILINE | re.DOTALL
    )

    # Write the updated content back to the Markdown file
    with open(md_file_path, 'w', encoding='utf-8') as md_file:
        md_file.write(updated_content)

def cleanup_interpreted_text(md_file_path):
    """
    Cleanup interpreted text in a Markdown file.
    Convert any interpreted-text role="doc" links to standard Markdown links.
    """
    with open(md_file_path, 'r', encoding='utf-8') as md_file:
        md_content = md_file.read()

    # Remove occurrences of {.interpreted-text role="doc"}
    md_content = re.sub(r'{\.interpreted-text\s+role=\"doc\"}', '', md_content, flags=re.DOTALL)
    md_content = re.sub(r'{\.interpreted-text\s+role=\"ref\"}', '', md_content, flags=re.DOTALL)

    # Search for the pattern and replace it
    updated_content = re.sub(r'`(.*?)\s*<(.*?)>`', r'[\1](\2)', md_content, re.MULTILINE)

    # Write the updated content back to the Markdown file
    with open(md_file_path, 'w', encoding='utf-8') as md_file2:
        md_file2.write(updated_content)

def cleanup(destination_path, log_file_path):
    """
    Clean up each .md file in the destination folder.
    """

    for root, dirs, files in os.walk(destination_path):
        for file in files:
            if file.endswith(".md"):
                md_file_path = os.path.join(root, file)
                update_title(md_file_path,log_file_path)
                fix_admonitions(md_file_path)
                cleanup_interpreted_text(md_file_path)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py source_path destination_path")
        sys.exit(1)

    source_path = sys.argv[1]
    destination_path = sys.argv[2]
    log_file_path = "log.txt"
    delete_folder(destination_path)
    for root, dirs, files in os.walk(source_path):
        for file in files:
            if file.endswith(".rst"):
                rst_file_path = os.path.join(root, file)
                relative_path = os.path.relpath(rst_file_path, source_path)
                md_file_path = os.path.join(destination_path, relative_path[:-4] + ".md")
                os.makedirs(os.path.dirname(md_file_path), exist_ok=True)
                convert_rst_to_md(rst_file_path, md_file_path, os.path.join(destination_path, log_file_path))

    cleanup(destination_path, log_file_path)
    print("Conversion done.")
