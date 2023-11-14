import os
import pypandoc
import re
import shutil
import click

@click.command()
@click.option('--source_path',envvar='SRC_PATH')
@click.option('--destination_path',envvar='DEST_PATH')
@click.option('--image_source_path',envvar='IMG_SRC_PATH')
@click.option('--image_destination_path',envvar='IMG_DEST_PATH')
def main(source_path, destination_path, image_source_path, image_destination_path):
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
    copy_folder_contents(image_source_path, image_destination_path)
    print("Conversion done.")

def delete_folder(path):
    try:
        if os.path.exists(path):
            shutil.rmtree(path)
            print(f"Folder at {path} successfully deleted.")
        else:
            print(f"Folder at {path} does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")

def update_title(md_file_path, log_file_path):
    with open(md_file_path, 'r', encoding='utf-8') as md_file:
        content = md_file.read()

    match = re.search(r'^#\s*(.*)', content, re.MULTILINE)
    if match:
        title_without_backticks = match.group(1).replace('`', '')

        if ':' in title_without_backticks:
            title_without_backticks = f'"{title_without_backticks}"'

        yaml_front_matter = f"---\ntitle: {title_without_backticks}\n---\n"

        content_lines = content.split('\n', 1)
        if re.match(r'^#\s', content_lines[0]):
            content = content_lines[1]

            with open(md_file_path, 'w', encoding='utf-8') as md_file:
                md_file.write(yaml_front_matter)
                md_file.write(content)

    else:
        with open(log_file_path, 'a', encoding='utf-8') as log:
            log.write(f"Error in file: {md_file_path}\n"
                      "No H1 title found. Please check and correct.\n\n")

def convert_rst_to_md(input_path, output_path, log_file):
    content = pypandoc.convert_file(input_path, 'md')
    with open(output_path, 'w', encoding='utf-8') as md_file:
        md_file.write(content)

def fix_admonitions(md_file_path):
    with open(md_file_path, 'r', encoding='utf-8') as md_file:
        md_content = md_file.read()

    updated_content = re.sub(
        r'\s+^\s*:::\s+title\s*$(.*?)^\s*:::\s*$', '', md_content, flags=re.MULTILINE | re.DOTALL
    )

    with open(md_file_path, 'w', encoding='utf-8') as md_file:
        md_file.write(updated_content)

def cleanup_interpreted_text(md_file_path):
    with open(md_file_path, 'r', encoding='utf-8') as md_file:
        md_content = md_file.read()

    md_content = re.sub(r'{\.interpreted-text\s+role=\"doc\"}', '', md_content, flags=re.DOTALL)
    md_content = re.sub(r'{\.interpreted-text\s+role=\"ref\"}', '', md_content, flags=re.DOTALL)

    updated_content = re.sub(r'`(.*?)\s*<(.*?)>`', r'[\1](\2)', md_content, re.MULTILINE)

    with open(md_file_path, 'w', encoding='utf-8') as md_file:
        md_file.write(updated_content)

def cleanup(destination_path, log_file_path):
    for root, dirs, files in os.walk(destination_path):
        for file in files:
            if file.endswith(".md"):
                md_file_path = os.path.join(root, file)
                update_title(md_file_path, log_file_path)
                fix_admonitions(md_file_path)
                # cleanup_interpreted_text(md_file_path)

def copy_folder_contents(source_path, destination_path):
    try:
        os.makedirs(destination_path, exist_ok=True)
        shutil.copytree(source_path, destination_path, dirs_exist_ok=True)
        print(f"Contents of {source_path} copied to {destination_path} successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
