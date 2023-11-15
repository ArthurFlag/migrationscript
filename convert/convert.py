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
@click.option('--repo_path',envvar='REPO_PATH')
def main(source_path, destination_path, image_source_path, image_destination_path, repo_path):
    log_file_path = "log.txt"

    delete_folder(destination_path)
    print("⚒️ Converting to RST...")
    for root, dirs, files in os.walk(source_path):
        for file in files:
            if file.endswith(".rst"):
                rst_file_path = os.path.join(root, file)
                relative_path = os.path.relpath(rst_file_path, source_path)
                md_file_path = os.path.join(destination_path, relative_path[:-4] + ".md")
                os.makedirs(os.path.dirname(md_file_path), exist_ok=True)
                convert_rst_to_md(rst_file_path, md_file_path, os.path.join(destination_path, log_file_path))
    print("\n🧹 Cleaning up MD files...")
    cleanup_md(destination_path,repo_path)
    copy_folder_contents(image_source_path, image_destination_path)
    print("✅ Conversion done.")

def delete_folder(path):
    try:
        if os.path.exists(path):
            shutil.rmtree(path)
            print(f"Folder at {path} successfully deleted.")
        else:
            print(f"Folder at {path} does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")

def update_title(md_content):
    match = re.search(r'^#\s*(.*)', md_content, re.MULTILINE)
    if match:
        title_without_backticks = match.group(1).replace('`', '')

        if ':' in title_without_backticks:
            title_without_backticks = f'"{title_without_backticks}"'

        yaml_front_matter = f"---\ntitle: {title_without_backticks}\n---\n"

        content_lines = md_content.split('\n', 1)
        if re.match(r'^#\s', content_lines[0]):
            md_content = yaml_front_matter + content_lines[1]

    return md_content

def convert_rst_to_md(input_path, output_path, log_file):
    content = pypandoc.convert_file(input_path, 'md')
    with open(output_path, 'w', encoding='utf-8') as md_file:
        md_file.write(content)

def fix_admonitions(md_content):
    return re.sub(
        r'\s+^\s*:::\s+title\s*$(.*?)^\s*:::\s*$', '', md_content, flags=re.MULTILINE | re.DOTALL
    )

def cleanup_interpreted_text_doc(md_content, repo_path):
    # look for `somepath`{.interpreted-text role="doc"}
    pattern = r'`\s*([^`]+)\s*`\s*{\.interpreted-text\s+role=\"doc\"}'

    def replace(match):
        path = match.group(1)
        print(f'path:{path}')
        full_path = os.path.join(repo_path, path)

        # Open the file located at the path
        try:
            with open(full_path, 'r', encoding='utf-8') as file:
                # Read the content of the file
                file_content = file.read()

                # Use a regular expression to find the title in the file content
                title_match = re.search(r'^title:\s*(.*?)(\n|$)', file_content)
                if title_match:
                    title = title_match.group(1)
                else:
                    # If no title is found, use a default value
                    title = 'No Title Found'
                    print(f'️⚠ No title found in {path}')

                # Replace the matched string with the formatted title and path
                return f'[{title}]({path})'
        except FileNotFoundError:
            # If the file is not found, return the original match
            print(f'️⚠ File not found ({path})')
            return match.group(0)

    # Use re.sub() with a custom replacement function
    updated_content = re.sub(pattern, replace, md_content)

    return updated_content

def cleanup_interpreted_text_ref(md_content):
    pattern = r'`(.*?)\s*<(.*?)>`{\.interpreted-text\s+role=\"ref\"}'
    return re.sub(pattern, r'[\1](\2)', md_content, flags=re.DOTALL)

def cleanup_md(md_folder_path, repo_path):
    for root, dirs, files in os.walk(md_folder_path):
        for file in files:
            if file.endswith(".md"):
                md_file_path = os.path.join(root, file)
                print(f'Working on {md_file_path}')

                with open(md_file_path, 'r', encoding='utf-8') as md_file:
                    md_content = md_file.read()

                md_content_titles_fixed = update_title(md_content)
                md_content_titles_adm_fixed = fix_admonitions(md_content_titles_fixed)
                md_content_titles_adm_doc_fixed = cleanup_interpreted_text_doc(md_content_titles_adm_fixed,repo_path)
                md_content_titles_adm_docref_fixed = cleanup_interpreted_text_ref(md_content_titles_adm_doc_fixed)
                md_content_final = cleanup_interpreted_text_ref(md_content_titles_adm_docref_fixed)

                with open(md_file_path, 'w', encoding='utf-8') as md_file:
                    md_file.write(md_content_final)

def copy_folder_contents(source_path, destination_path):
    print("📸 Copying images...")
    try:
        os.makedirs(destination_path, exist_ok=True)
        shutil.copytree(source_path, destination_path, dirs_exist_ok=True)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()