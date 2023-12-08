import os
import pypandoc
import re
import shutil
import click


@click.command()
@click.option("--docs_path", envvar="SRC_DOCS_PATH")
@click.option("--destination_repo", envvar="DEST_REPO_PATH")
@click.option("--image_source_path", envvar="SRC_IMG_PATH")
@click.option("--src_repo_path", envvar="SRC_REPO_PATH")
def main(docs_path, destination_repo, image_source_path, src_repo_path):
    log_file_path = "log.txt"
    include_source_path = os.path.join(src_repo_path, "includes")
    include_destination_path = os.path.join(destination_repo, "static/includes")
    image_destination_path = os.path.join(destination_repo, "static/images")
    destination_docs_path = os.path.join(destination_repo, "docs")
    code_source_path = os.path.join(docs_path, "../code")
    code_destination_path = os.path.join(destination_repo, "static/code")
    source_path_temp = os.path.join(os.path.dirname(__file__), "../temp")
    include_source_path_temp = os.path.join(os.path.dirname(__file__), "../includes_temp")

    print("🧹  Deleting output...")
    delete_folder(destination_docs_path)
    delete_folder(source_path_temp)
    delete_folder(include_destination_path)
    delete_folder(include_source_path_temp)
    copy_folder_contents(image_source_path, image_destination_path)
    copy_folder_contents(code_source_path, code_destination_path)
    copy_folder_contents(include_source_path, include_source_path_temp)
    copy_folder_contents(docs_path, source_path_temp)
    delete_file(os.path.join(docs_path, "community.rst"))

    # fix_include_paths(source_path_temp, include_source_path_temp)
    convert_includes_to_md(log_file_path, include_source_path, include_destination_path)
    convert_docs_to_md(
        source_path_temp, log_file_path, destination_docs_path
    )
    cleanup_md(destination_docs_path, destination_repo)
    add_includes(destination_docs_path)
    # delete_complex_files(destination_docs_path)
    print("✅  Conversion done.")
    nextsteps()

def add_includes(docs_path):

    files = [
        os.path.join(docs_path,"products/cassandra/reference/advanced-params.md"),
        os.path.join(docs_path,"products/clickhouse/reference/advanced-params.md"),
        os.path.join(docs_path,"products/flink/reference/advanced-params.md"),
        os.path.join(docs_path,"products/grafana/reference/advanced-params.md"),
        os.path.join(docs_path,"products/influxdb/reference/advanced-params.md"),
        os.path.join(docs_path,"products/kafka/reference/advanced-params.md"),
        os.path.join(docs_path,"products/m3db/reference/advanced-params.md"),
        os.path.join(docs_path,"products/mysql/reference/advanced-params.md"),
        os.path.join(docs_path,"products/opensearch/reference/advanced-params.md"),
        os.path.join(docs_path,"products/postgresql/reference/advanced-params.md"),
        os.path.join(docs_path,"products/redis/reference/advanced-params.md"),
    ]

    for file_path in files:
        service = file_path.split(os.path.sep)[len(docs_path.split(os.path.sep)) + 1]

        with open(file_path, 'a') as file:
            content_to_append = f'\nimport Reference from \'@site/static/includes/config-{service}.md\';\n\n<Reference />\n'
            file.write(content_to_append)

    path = os.path.join(docs_path,"products/m3db/reference/advanced-params-m3aggregator.md")
    with open(path, 'a') as file:
        content_to_append = f'\nimport Reference from \'@site/static/includes/config-m3aggregator.md\';\n\n<Reference />\n'
        file.write(content_to_append)

    path = os.path.join(docs_path,"products/kafka/kafka-connect/reference")
    with open(path, 'a') as file:
        content_to_append = f'\nimport Reference from \'@site/static/includes/config-kafka_connect.md\';\n\n<Reference />\n'
        file.write(content_to_append)

    path = os.path.join(docs_path,"products/kafka/kafka-mirrormaker/reference")
    with open(path, 'a') as file:
        content_to_append = f'\nimport Reference from \'@site/static/includes/config-kafka_mirrormaker.md\';\n\n<Reference />\n'
        file.write(content_to_append)

def convert_docs_to_md(
    source_path, log_file_path, destination_docs_path
):
    print(f"⚒️  Converting {source_path}...")
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


def convert_includes_to_md(
    log_file_path, include_source_path, include_destination_path
):
    """
    Converts the include to md
    """
    print(f"⚒️  Convert includes in {include_source_path}...")
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


def fix_include_paths(source_path,include_source_path):
    print(f"⚒️  Fixing include paths in {source_path}...")
    for root, dirs, files in os.walk(source_path):
        for file in files:
            if file.endswith(".rst"):
                rst_file_path = os.path.join(root, file)
                with open(rst_file_path, "r", encoding="utf-8") as rst_file:
                    rst_content = rst_file.read()

                rst_content = update_include_link_rst(rst_content,include_source_path)

                with open(rst_file_path, "w", encoding="utf-8") as rst_file:
                    rst_file.write(rst_content)

def update_include_link_rst(rst_content, include_source_path):
    pattern = r"\.\. include:: /includes/(.*?\.rst)"
    updated_content = re.sub(pattern, f".. include:: {include_source_path}/\\1", rst_content)

    return updated_content

def nextsteps():
    out = """
Take care of these topics manually:

- https://docs.aiven.io/docs/products/clickhouse/howto/data-service-integration
- https://docs.aiven.io/docs/products/mysql/concepts/max-number-of-connections
- /Users/arthurflageul/repos/aiven-docs/docs/products/postgresql/reference/list-of-extensions.md
- docs/products/kafka/howto/enable-oidc.rst

Tables:
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
            print(f"  Folder at {path} successfully deleted.")
        else:
            print(f"  Folder at {path} does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")


def update_title(md_content):
    match = re.search(r"^#\s*(.*)", md_content, re.MULTILINE)
    if match:
        title_without_backticks = match.group(1).replace("`", "")

        if ":" in title_without_backticks:
            title_without_backticks = f'"{title_without_backticks}"'

        title_without_backticks = title_without_backticks.replace("®\\*", "®*")
        title_without_backticks = title_without_backticks.replace("\\'s", "'s")

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
    md_content = re.sub(
        r"::: (\w+)", r":::\1", md_content, flags=re.MULTILINE  # ::: tip
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
            print(f"⚠️  Couldn't find title in {path}. Using None.")
            title = "None"
        newlink = f"[{title}]({path})"
        md_content = re.sub(pattern_link_no_title, newlink, md_content)
    return md_content


def fix_full_links(md_content):
    pattern = r"`(.*?)\s*<(.*?)>`{\.interpreted-text\s+role=\"...\"}"
    return re.sub(pattern, r"[\1](\2)", md_content)


def fix_literal_includes(md_content):
    language_pattern = re.compile(
        r"::: {\.literalinclude language=\"(.*?)\"}\n( *\/.*$)\n *:::", re.MULTILINE
    )
    path_pattern = re.compile(
        r"::: {\.literalinclude language=\".*?\"}\n( *\/.*$)\n *:::", re.MULTILINE
    )
    import_dict = {}
    component_counter = 1  # Initialize component_counter
    final = md_content

    def replace_line(match):
        nonlocal component_counter  # Use nonlocal to reference the outer component_counter
        language = match.group(1)
        path = next(path_generator)
        component_name = f"MyComponentSource{component_counter}"
        import_dict[component_name] = path
        replacement = (
            f"<CodeBlock language='{language}'>{{{component_name}}}</CodeBlock>"
        )
        component_counter += 1
        return replacement

    path_matches = path_pattern.finditer(md_content)
    path_generator = (match.group(1) for match in path_matches)
    output_text = language_pattern.sub(replace_line, md_content)
    imports = ["import CodeBlock from '@theme/CodeBlock';"]
    if import_dict:
        for k, v in import_dict.items():
            imports.append(f"import {k} from '!!raw-loader!{v.strip()}';")
            importsstr = "\n".join(imports) + "\n"
        final = re.sub(r"(---\ntitle.*\n---\n)", rf"\1\n{importsstr}", output_text)

    return final


def process_seealso_blocks(md_content):
    # Define the regular expression pattern to match ::seealso blocks
    pattern = r":::seealso\s*([\s\S]*?):::"

    def replace_block(match):
        # Replace the ::seealso block with :::note See also
        return ":::note See also\n" + match.group(1).strip() + "\n:::"

    # Use re.sub() to replace all occurrences of the pattern in the input content
    updated_content = re.sub(pattern, replace_block, md_content)

    return updated_content


def process_topic_blocks(md_content):
    pattern = r":::topic\n\*\*(.*?)\*\*\n"
    updated_content = re.sub(pattern, r":::note \1", md_content)

    return updated_content


def cleanup_md(md_folder_path, destination_repo_path):
    print("\n🧹 Cleaning up MD files...")
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
                    md_content = process_seealso_blocks(md_content)
                    md_content = process_topic_blocks(md_content)
                    md_content = process_custom_markup(md_content)
                    md_content = comment_out_mermaid(md_content)
                    # md_content_no_grids = process_grids(md_content_titles_adm_docref_fixed)

                # write the changes
                with open(md_file_path, "w", encoding="utf-8") as md_file:
                    # print(f"Wrote {md_file_path}")
                    md_file.write(md_content)

    # take a second round for link and title resolution
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

    md_content = re.sub(r"^::: {\.(.*?) .*", r"::: \1", md_content, flags=re.MULTILINE)
    md_content = re.sub(r"\[(.*)\]\{\..*?\}", r"`\1`", md_content, flags=re.MULTILINE)
    md_content = md_content.replace(
        "<hacks@Aiven.io>", "[hacks@aiven.io](mailto:hacks@aiven.io)"
    )
    md_content = md_content.replace(
        "<sales@Aiven.io>", "[sales@aiven.io](mailto:sales@aiven.io)"
    )
    md_content = md_content.replace(
        "<support@Aiven.io>", "[support@aiven.io](mailto:support@aiven.io)"
    )
    md_content = md_content.replace('{width="400px"}', "")
    md_content = md_content.replace('{width="500px"}', "")
    md_content = md_content.replace('{width="100.0%"}', "")
    md_content = md_content.replace('{height="342px"}', "")
    md_content = md_content.replace('{height="249px"}', "")
    md_content = md_content.replace('](avn_service_integration_endpoint_create)', "](/docs/tools/cli/service/integration#avn_service_integration_endpoint_create)")
    md_content = md_content.replace('](avn_service_integration_create)', "](/docs/tools/cli/service/integration#avn_service_integration_create)")
    md_content = md_content.replace('](avn_service_integration_endpoint_list)', "](/docs/tools/cli/service/integration#avn_service_integration_endpoint_list)")
    md_content = md_content.replace('](sales@aiven.io) ', "](mailto:sales@aiven.io)")
    md_content = md_content.replace("](avn-service-logs)","](/docs/tools/cli/service#avn-service-logs)")
    md_content = md_content.replace("::: {#Terminology", ":::Terminology")
    md_content = md_content.replace("](avn-create-update-project)","](/docs/tools/cli/service#avn-create-update-project)")

    md_content = md_content.replace("](avn-delete-project)","](/docs/tools/cli/service#avn-delete-project)")
    md_content = md_content.replace("](avn-cli-service-update)","](/docs/tools/cli/service#avn-cli-service-update)")
    md_content = md_content.replace("](avn-service-logs)","](/docs/tools/cli/service#avn-service-logs)")
    md_content = md_content.replace("](avn-service-metrics)","](/docs/tools/cli/service#avn-service-metrics)")
    md_content = md_content.replace("](avn-cli-service-terminate)","](/docs/tools/cli/service#avn-cli-service-terminate)")
    md_content = md_content.replace("](create-org-api)","](#create-org-api)")
    md_content = re.sub(r"{\.interpreted-text\s*?role=\"bdg-secondary\"}","",md_content)

    md_content = re.sub(
        r"\n:::\s?tableofcontents\n:::\n", r"", md_content, flags=re.MULTILINE
    )
    md_content = re.sub(r"<(https://.*)>", r"[\1](\1)", md_content, flags=re.MULTILINE)

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
    pattern = r"`([^<>]+)`{\.interpreted-text role=\"ref\"}"
    title_anchor_dict = extract_titles_with_anchors(md_content)

    # Define the substitution function
    def replace_match(match):
        title = title_anchor_dict.get(match.group(1), match.group(1))
        return f"[{title}](#{match.group(1)})"

    # Use re.sub to replace the matches with the dictionary values
    updated_content = re.sub(pattern, replace_match, md_content)

    return updated_content


def extract_titles_with_anchors(md_content):
    title_pattern = r"#+ (.+?) \{#(.+?)\}"
    title_matches = re.findall(title_pattern, md_content)
    titles_and_anchors = {anchor: title for title, anchor in title_matches}

    return titles_and_anchors

def comment_out_mermaid(md_content):
    pattern = r"(:::mermaid.*?:::)"
    updated_content = re.sub(pattern, r"<!--\n\1\n-->", md_content, flags=re.DOTALL)

    return updated_content

# TODO
# find `delete`{.interpreted-text role="bdg-secondary"}
# `console-authentication`{.interpreted-text role="ref"} (same page link)
# `avn_service_plan`{.interpreted-text role="ref"}
#
# check docs/products/kafka/howto/prevent-full-disks.md
# `api/examples`{.interpreted-text role="doc"}
# ``` {.bash caption="Expected output"}
# convert variables

if __name__ == "__main__":
    main()
