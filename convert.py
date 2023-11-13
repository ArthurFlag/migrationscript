import os
import sys
import pypandoc
import re

def extract_title_from_rst(file_path):
    """
    Extract the title from a reStructuredText file.
    """
    with open(file_path, 'r', encoding='utf-8') as rst_file:
        # Read the first line as the title
        title = rst_file.readline().strip()

    return title

def convert_rst_to_md(input_path, output_path, log_file):
    """
    Convert a reStructuredText file to Markdown using pypandoc.
    Include the title at the top in YAML front matter.
    Remove the first H1 title from the Markdown file.
    Log errors if two H1 titles are found.
    """
    title = extract_title_from_rst(input_path)

    # Create YAML front matter
    yaml_front_matter = f"---\ntitle: {title}\n---\n\n"

    # Convert the rest of the file to Markdown
    content = pypandoc.convert_file(input_path, 'md')

    # Remove the first H1 title
    lines = content.split('\n', 1)
    if re.match(r'^#\s', lines[0]) or re.match(r'^#$', lines[0]):
        content = lines[1]

        # Check for a second H1 title
        if re.search(r'^#\s', content):
            with open(log_file, 'a', encoding='utf-8') as log:
                log.write(f"Error in file: {input_path}\n"
                          "Multiple H1 titles found. Please check and correct.\n\n")
    else:
        with open(log_file, 'a', encoding='utf-8') as log:
            log.write(f"Error in file: {input_path}\n"
                      "No H1 title found. Please check and correct.\n\n")

    # Write the combined content to the Markdown file
    with open(output_path, 'w', encoding='utf-8') as md_file:
        md_file.write(yaml_front_matter)
        md_file.write(content)

def fix_admonitions(md_file_path):
    """
    Fix admonitions in a Markdown file.
    Remove lines containing "::: title".
    """
    with open(md_file_path, 'r', encoding='utf-8') as md_file:
        md_content = md_file.read()

    # Remove lines containing "::: title"
    updated_content = re.sub(r'^\s*:::\s+title\s*$', '', md_content, flags=re.MULTILINE)

    # Write the updated content back to the Markdown file
    with open(md_file_path, 'w', encoding='utf-8') as md_file:
        md_file.write(updated_content)

def cleanup_interpreted_text(md_file_path):
    """
    Cleanup interpreted text in a Markdown file.
    Convert {.interpreted-text role="doc"} links to standard Markdown links.
    """
    with open(md_file_path, 'r', encoding='utf-8') as md_file:
        md_content = md_file.read()

    # Search for the pattern and replace it
    updated_content = re.sub(r'(\S+)\s*<(.*?)>`{\.interpreted-text\s*role=".*?"}', r'[\1](\2)', md_content)

    # Write the updated content back to the Markdown file
    with open(md_file_path, 'w', encoding='utf-8') as md_file:
        md_file.write(updated_content)

def process_folder(folder_path, destination_path):
    """
    Recursively process a folder and convert each .rst file to Markdown.
    """
    log_file_path = os.path.join(destination_path, "log.txt")

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".rst"):
                rst_file_path = os.path.join(root, file)
                relative_path = os.path.relpath(rst_file_path, folder_path)
                md_file_path = os.path.join(destination_path, relative_path[:-4] + ".md")

                # Ensure the destination folder exists
                os.makedirs(os.path.dirname(md_file_path), exist_ok=True)

                convert_rst_to_md(rst_file_path, md_file_path, log_file_path)
                cleanup_interpreted_text(md_file_path)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py folder_path destination_path")
        sys.exit(1)

    folder_path = sys.argv[1]
    destination_path = sys.argv[2]

    process_folder(folder_path, destination_path)
    print("Conversion and cleanup completed successfully.")
