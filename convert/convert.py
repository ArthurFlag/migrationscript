import os
import pypandoc
import re
import shutil
import click


@click.command()
@click.option("--source_path", envvar="SRC_DOCS_PATH")
@click.option("--destination_repo", envvar="DEST_REPO_PATH")
@click.option("--image_source_path", envvar="SRC_IMG_PATH")
@click.option("--src_repo_path", envvar="SRC_REPO_PATH")
def main(source_path, destination_repo, image_source_path, src_repo_path):
    log_file_path = "log.txt"
    image_destination_path = os.path.join(destination_repo, "static/images")
    destination_docs_path = os.path.join(destination_repo, "docs")

    delete_folder(destination_docs_path)
    print("⚒️ Converting to RST...")
    for root, dirs, files in os.walk(source_path):
        for file in files:
            if file.endswith(".rst"):
                rst_file_path = os.path.join(root, file)
                relative_path = os.path.relpath(rst_file_path, source_path)
                md_file_path = os.path.join(
                    destination_docs_path, relative_path[:-4] + ".md"
                )
                os.makedirs(os.path.dirname(md_file_path), exist_ok=True)
                convert_rst_to_md(
                    rst_file_path,
                    md_file_path,
                    os.path.join(destination_docs_path, log_file_path),
                )
    print("\n🧹 Cleaning up MD files...")
    cleanup_md(destination_docs_path, src_repo_path)
    print("\n🧹 Delete complex files for now...")
    delete_complex_files(destination_docs_path)
    copy_folder_contents(image_source_path, image_destination_path)
    print("✅ Conversion done.")


def delete_file(file_path):
    try:
        os.remove(file_path)
        print(f"File deleted: {file_path}")
    except FileNotFoundError:
        print(f"File not found: {file_path}")


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
    match = re.search(r"^#\s*(.*)", md_content, re.MULTILINE)
    if match:
        title_without_backticks = match.group(1).replace("`", "")

        if ":" in title_without_backticks:
            title_without_backticks = f'"{title_without_backticks}"'

        yaml_front_matter = f"---\ntitle: {title_without_backticks}\n---\n"

        content_lines = md_content.split("\n", 1)
        if re.match(r"^#\s", content_lines[0]):
            md_content = yaml_front_matter + content_lines[1]

    return md_content


def convert_rst_to_md(input_path, output_path, log_file):
    content = pypandoc.convert_file(input_path, "md")
    with open(output_path, "w", encoding="utf-8") as md_file:
        md_file.write(content)


def fix_admonitions(md_content):
    return re.sub(
        r"\s+^\s*:::\s+title\s*$(.*?)^\s*:::\s*$",
        "",
        md_content,
        flags=re.MULTILINE | re.DOTALL,
    )


def extract_title(path):
    # Open the file located at the path
    try:
        with open(path, "r", encoding="utf-8") as file:
            md_content = file.read()
            title_match = re.search(r"^---\s*[\s\S]*?title:\s*(.*?)\s*---", md_content)
            if title_match:
                title = title_match.group(1)
                return title
            else:
                raise LookupError(f"⚠ (extract_title No title found ({path})")
    except IsADirectoryError:
        print(f"⚠️  Unexpected directory! Tried to fetch title of {path}")
    except FileNotFoundError:
        raise FileNotFoundError(f"⚠️ File not found ({path})")


def fix_no_name_links(md_content, src_repo_path):
    # look for `somepath`{.interpreted-text role=".*?"}
    pattern_link_no_title = r"`(((\.\.)|(\/)).*?)`{\.interpreted-text\s+role=\".*?\"}"
    match = re.search(pattern_link_no_title, md_content)
    if match:
        path = match.group(1)
        # print(f"  ---- Found link without name: {path}")
        if not os.path.isabs(path):
            resolved_path = os.path.normpath(os.path.join(src_repo_path, path))
        else:
            resolved_path = src_repo_path + path
        title = extract_title(resolved_path)
        newlink = f"[{title}]({path})"
        # print(f"  ---- Turning into: {newlink}")
        md_content = re.sub(pattern_link_no_title, newlink, md_content)
    return md_content


def fix_doc_links(md_content):
    # fixes link like with a name
    # look for `somename <somepath>`{.interpreted-text role="doc"}
    md_content_updated = md_content
    pattern_link = r"`(.*?)\s<(.*?)>`{\.interpreted-text\s*role=\"doc\"}"
    match = re.search(pattern_link, md_content)
    if match:
        name = match.group(1)
        path = match.group(2)
        newlink = f"[{name}]({path})"
        md_content_updated = re.sub(pattern_link, newlink, md_content)
    return md_content_updated


def cleanup_interpreted_text_ref(md_content):
    pattern = r"`(.*?)\s*<(.*?)>`{\.interpreted-text\s+role=\"ref\"}"
    return re.sub(pattern, r"[\1](\2)", md_content, flags=re.DOTALL)


def cleanup_md(md_folder_path, src_repo_path):
    for root, dirs, files in os.walk(md_folder_path):
        for file in files:
            if file.endswith(".md"):
                md_file_path = os.path.join(root, file)
                # print(f"\nWorking on {md_file_path}")

                with open(md_file_path, "r", encoding="utf-8") as md_file:
                    md_content = md_file.read()
                    md_content_titles_fixed = update_title(md_content)
                    md_content_titles_adm_fixed = fix_admonitions(
                        md_content_titles_fixed
                    )
                    md_content_titles_adm_docref_fixed = cleanup_interpreted_text_ref(
                        md_content_titles_adm_fixed
                    )
                    md_content_final = cleanup_interpreted_text_ref(
                        md_content_titles_adm_docref_fixed
                    )
                with open(md_file_path, "w", encoding="utf-8") as md_file:
                    md_file.write(md_content_final)

                with open(md_file_path, "r", encoding="utf-8") as md_file2:
                    md_content = md_file2.read()
                    try:
                        md_content_no_title_fixed = fix_no_name_links(
                            md_content, src_repo_path
                        )
                        md_content_link_fixed = fix_doc_links(md_content_no_title_fixed)

                        with open(md_file_path, "w", encoding="utf-8") as md_file2:
                            md_file2.write(md_content_link_fixed)
                    except FileNotFoundError:
                        print(f"⚠️  File not found! ({md_file_path})")
                    except LookupError:
                        print(f"⚠️  Title not found! ({md_file_path})")


def delete_complex_files(destination_repo):
    # delete files that we need to handle better later
    community_folder = os.path.join(destination_repo, "community")
    delete_folder(community_folder)
    delete_file(destination_repo+"community.md")


def copy_folder_contents(source_path, destination_path):
    print("📸 Copying images...")
    try:
        os.makedirs(destination_path, exist_ok=True)
        shutil.copytree(source_path, destination_path, dirs_exist_ok=True)
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
