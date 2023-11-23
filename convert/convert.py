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
    include_source_path = os.path.join(src_repo_path, "includes")
    include_destination_path = os.path.join(destination_repo, "static/includes")
    image_destination_path = os.path.join(destination_repo, "static/images")
    destination_docs_path = os.path.join(destination_repo, "docs")
    
    print("🧹 Deleting output...")
    delete_folder(destination_docs_path)
    delete_folder(include_destination_path) 
    copy_folder_contents(image_source_path, image_destination_path)
    
    print(f"⚒️ Converting {include_source_path}...")
    for root, dirs, files in os.walk(include_source_path):
        for file in files:
            if file.endswith(".rst"):
                rst_file_path = os.path.join(root, file)
                relative_path = os.path.relpath(rst_file_path, include_source_path)
                md_file_path = os.path.join(
                    include_destination_path, relative_path[:-4] + ".md"
                )
                os.makedirs(os.path.dirname(md_file_path), exist_ok=True)
                convert_rst_to_md(
                    rst_file_path,
                    md_file_path,
                    os.path.join(include_destination_path, log_file_path),
                )
                
    print(f"⚒️ Converting {source_path}...")
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
    cleanup_md(destination_docs_path, destination_repo)
    # delete_complex_files(destination_docs_path)
    print("✅ Conversion done.")
    nextsteps()

def nextsteps():
    out ="""
Now take care of these topics manually:
- https://docs.aiven.io/docs/products/clickhouse/howto/data-service-integration
- https://docs.aiven.io/docs/products/mysql/concepts/max-number-of-connections
- /Users/arthurflageul/repos/aiven-docs/docs/products/postgresql/reference/list-of-extensions.md
- docs/products/kafka/howto/enable-oidc.rst 
- products/kafka/reference/advanced-params
- kafka/prevent-full-disks
- build the docs and search for ---+ in the build folder to fix broken tables.
"""
    print(out)
    
    
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
            
        
        title_without_backticks = title_without_backticks.replace("®\\*","®*")

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
    md_content = re.sub(
        r"\s+^\s*:::\s+title\s*$(.*?)^\s*:::\s*$",
        "",
        md_content,
        flags=re.MULTILINE | re.DOTALL,
    )
    md_content =re.sub(
        r"::: (\w+)", # ::: tip
        ":::\1",
        md_content,
        flags=re.MULTILINE | re.DOTALL,
    )
    return md_content

def fix_standalone_links(md_content):
    # <somelink>
    return re.sub(
        r"^\<(.*?)\>$",
        r"[](\1)",
        md_content,
        flags=re.MULTILINE | re.DOTALL,
    )


def extract_title(path):
    # Open the file located at the path
    if not os.path.splitext(path)[1]:
      path += ".md"

    # print(f"extracting title from {path}")
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
        print(f"⚠️  File not found ({path})")


def fix_no_name_links(md_content, repo_path):
    # look for `somepath`{.interpreted-text role=".*?"}
    pattern_link_no_title = r"`(((\.\.)|(\/)).*?)`{\.interpreted-text\s+role=\".*?\"}"
    match = re.search(pattern_link_no_title, md_content)
    if match:
        path = match.group(1)
        # print(f"  ---- Found link without name: {path}")
        if not os.path.isabs(path):
            resolved_path = os.path.normpath(os.path.join(repo_path, path))
        else:
            resolved_path = repo_path + path
        try:
            title = extract_title(resolved_path)
        except LookupError:
            print(f"⚠️ Couldn't find title in {path}. Using None.")
            title = "None"
        newlink = f"[{title}]({path})"
        md_content = re.sub(pattern_link_no_title, newlink, md_content)
    return md_content


def fix_full_links(md_content):
    pattern = r"`(.*?)\s*<(.*?)>`{\.interpreted-text\s+role=\"...\"}"
    return re.sub(pattern, r"[\1](\2)", md_content)

def fix_literal_includes(md_content):
    pattern = r"::: {\.literalinclude language=\"(.*)\"}"
    return re.sub(pattern,r"::: literalinclude \1", md_content)
    
def cleanup_md(md_folder_path, destination_repo_path):
    for root, dirs, files in os.walk(md_folder_path):
        for file in files:
            if file.endswith(".md"):
                md_file_path = os.path.join(root, file)
                # print(f"Working on {md_file_path}")

                with open(md_file_path, "r", encoding="utf-8") as md_file:
                    md_content = md_file.read()
                    md_content = update_title(md_content)
                    md_content = fix_admonitions(md_content)
                    md_content = fix_anchor_links(md_content)
                    md_content = fix_full_links(md_content)
                    md_content = fix_standalone_links(md_content)
                    md_content = fix_literal_includes(md_content)
                    md_content = process_custom_markup(md_content)
                    # md_content_no_grids = process_grids(md_content_titles_adm_docref_fixed)

                # write the changes
                with open(md_file_path, "w", encoding="utf-8") as md_file:
                    # print(f"Wrote {md_file_path}")
                    md_file.write(md_content)

    # take a second round for link and title resolution
    print("Second pass...")
    for root, dirs, files in os.walk(md_folder_path):
        for file in files:
            if file.endswith(".md"):
                md_file_path = os.path.join(root, file)
                # print(f"Working on {md_file_path}")

                with open(md_file_path, "r", encoding="utf-8") as md_file:
                    md_content = md_file.read()
                    md_content = fix_no_name_links(md_content, destination_repo_path)

                with open(md_file_path, "w", encoding="utf-8") as md_file:
                    md_file.write(md_content)

def process_grids(md_content):
    # deletes grid instructions from the content
    card_declaration = r"`^::: \{\.grid-item-card.*?\n(.*?)^:::$\n`"
    grid_declaration = r"`^::: grid\n.*?$\n(.*?)^:::$`"
    content_fixed = re.sub(
        card_declaration, "", md_content, flags=re.MULTILINE | re.DOTALL
    )
    content_final = re.sub(
        grid_declaration, "", content_fixed, flags=re.MULTILINE | re.DOTALL
    )
    return content_final

def process_custom_markup(md_content):
    # prevents build error on custom markup. Should be solved properly later.
    # ex  "[destination]{.title-ref}"" or ""::: {.grid...}"

    md_content = re.sub(r"^::: {\.(.*?) .*",r"::: \1",md_content, flags=re.MULTILINE)
    md_content = re.sub(r"\[(.*)\]\{\..*?\}",r"`\1`",md_content, flags=re.MULTILINE)
    md_content = md_content.replace("<hacks@Aiven.io>","[hacks@aiven.io](mailto:hacks@aiven.io)")
    md_content = md_content.replace("<sales@Aiven.io>","[sales@aiven.io](mailto:sales@aiven.io)")
    md_content = md_content.replace("<support@Aiven.io>","[support@aiven.io](mailto:support@aiven.io)")
    md_content = md_content.replace("{width=\"400px\"}","")
    md_content = md_content.replace("{width=\"100.0%\"}","")
    md_content = re.sub(r"\n:::\s?tableofcontents\n:::\n",r"",md_content,flags=re.MULTILINE)
    md_content = re.sub(r"<(https://.*)>",r"[\1](\1)",md_content,flags=re.MULTILINE)
    
    return md_content

def delete_complex_files(destination_repo):
    # delete files that we need to handle better later
    community_folder = os.path.join(destination_repo, "community")
    delete_folder(community_folder)
    delete_file(destination_repo + "community.md")


def copy_folder_contents(source_path, destination_path):
    print(f"📸 Copying {source_path} into {destination_path}...")
    try:
        os.makedirs(destination_path, exist_ok=True)
        shutil.copytree(source_path, destination_path, dirs_exist_ok=True)
    except Exception as e:
        print(f"An error occurred: {e}")

def fix_anchor_links(md_content):
    # Define a regular expression pattern to find occurrences of {#...}
    pattern = r'`([^<>]+)`{\.interpreted-text role=\"ref\"}'
    title_anchor_dict = extract_titles_with_anchors(md_content)
    # Define the substitution function
    def replace_match(match):
        title = title_anchor_dict.get(match.group(1), match.group(1))
        return f'[{title}](#{match.group(1)})'

    # Use re.sub to replace the matches with the dictionary values
    updated_content = re.sub(pattern, replace_match, md_content)

    return updated_content

def extract_titles_with_anchors(md_content):
    
    title_pattern = r'#+ (.+?) \{#(.+?)\}'
    title_matches = re.findall(title_pattern, md_content)
    titles_and_anchors = {anchor: title for title, anchor in title_matches}

    return titles_and_anchors



      

# TODO
# find `delete`{.interpreted-text role="bdg-secondary"}
# `console-authentication`{.interpreted-text role="ref"} (same page link)
# `avn_service_plan`{.interpreted-text role="ref"} 
# ::: {.literalinclude language="properties"}
# variables
# check docs/products/kafka/howto/prevent-full-disks.md
# # `api/examples`{.interpreted-text role="doc"}
# ::: {#Terminology MM2ClusterAliasducts/opensearch/howto/connect-with-pytho}
# 


if __name__ == "__main__":
    main()
