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
    include_source_path_temp = os.path.join(
        os.path.dirname(__file__), "../includes_temp"
    )

    print("🧹  Deleting output...")
    delete_folder(destination_docs_path)
    delete_folder(source_path_temp)
    delete_folder(include_destination_path)
    delete_folder(include_source_path_temp)
    delete_folder(code_destination_path)
    copy_folder_contents(image_source_path, image_destination_path)
    copy_folder_contents(code_source_path, code_destination_path)
    copy_folder_contents(include_source_path, include_source_path_temp)
    delete_file(os.path.join(include_source_path_temp, "platform-variables.rst"))
    copy_folder_contents(docs_path, source_path_temp)

    # fix_include_paths(source_path_temp, include_source_path_temp)
    convert_includes_to_md(log_file_path, include_source_path, include_destination_path)
    convert_docs_to_md(source_path_temp, log_file_path, destination_docs_path)
    cleanup_md_docs_files(destination_docs_path, destination_repo)
    delete_file(os.path.join(include_destination_path, "platform-variables.md"))
    cleanup_includes(include_destination_path)
    add_includes(destination_docs_path)
    delete_lines(os.path.join(destination_docs_path, "products"))
    fix_specific_files(destination_repo)
    print("✅  Conversion done.")
    nextsteps()


def cleanup_includes(md_folder_path):
    print("\n🧹 Cleaning up MD includes...")
    for root, dirs, files in os.walk(md_folder_path):
        for file in files:
            if file.endswith(".md"):
                md_file_path = os.path.join(root, file)

                with open(md_file_path, "r", encoding="utf-8") as md_file:
                    md_content = md_file.read()
                    md_content = fix_admonitions(md_content)
                    md_content = fix_full_links(md_content)
                    md_content = fix_standalone_links(md_content)
                    md_content = fix_literal_includes(md_content)
                    md_content = process_seealso_blocks(md_content)
                    md_content = process_dropdowns(md_content)
                    md_content = process_topic_blocks(md_content)
                    md_content = comment_out_mermaid(md_content)
                    md_content = fix_codeblock_title(md_content)
                    md_content = process_grids(md_content)

                # write the changes
                with open(md_file_path, "w", encoding="utf-8") as md_file:
                    # print(f"Wrote {md_file_path}")
                    md_file.write(md_content)


def add_includes(docs_path):
    files = [
        os.path.join(docs_path, "products/cassandra/reference/advanced-params.md"),
        os.path.join(docs_path, "products/clickhouse/reference/advanced-params.md"),
        os.path.join(docs_path, "products/flink/reference/advanced-params.md"),
        os.path.join(docs_path, "products/grafana/reference/advanced-params.md"),
        os.path.join(docs_path, "products/influxdb/reference/advanced-params.md"),
        os.path.join(docs_path, "products/kafka/reference/advanced-params.md"),
        os.path.join(docs_path, "products/m3db/reference/advanced-params.md"),
        os.path.join(docs_path, "products/mysql/reference/advanced-params.md"),
        os.path.join(docs_path, "products/opensearch/reference/advanced-params.md"),
        os.path.join(docs_path, "products/redis/reference/advanced-params.md"),
    ]
    # deal with this one
    # os.path.join(docs_path,"products/postgresql/reference/advanced-params.md"),

    for file_path in files:
        service = file_path.split(os.path.sep)[len(docs_path.split(os.path.sep)) + 1]

        with open(file_path, "a") as file:
            content_to_append = f"\nimport Reference from '@site/static/includes/config-{service}.md';\n\n<Reference />\n"
            file.write(content_to_append)

    path = os.path.join(
        docs_path, "products/m3db/reference/advanced-params-m3aggregator.md"
    )
    with open(path, "a") as file:
        content_to_append = f"\nimport Reference from '@site/static/includes/config-m3aggregator.md';\n\n<Reference />\n"
        file.write(content_to_append)

    path = os.path.join(
        docs_path, "products/kafka/kafka-connect/reference/advanced-params.md"
    )
    with open(path, "a") as file:
        content_to_append = f"\nimport Reference from '@site/static/includes/config-kafka_connect.md';\n\n<Reference />\n"
        file.write(content_to_append)

    path = os.path.join(
        docs_path, "products/kafka/kafka-mirrormaker/reference/advanced-params.md"
    )
    with open(path, "a") as file:
        content_to_append = f"\nimport Reference from '@site/static/includes/config-kafka_mirrormaker.md';\n\n<Reference />\n"
        file.write(content_to_append)


def convert_docs_to_md(source_path, log_file_path, destination_docs_path):
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


def fix_include_paths(source_path, include_source_path):
    print(f"⚒️  Fixing include paths in {source_path}...")
    for root, dirs, files in os.walk(source_path):
        for file in files:
            if file.endswith(".rst"):
                rst_file_path = os.path.join(root, file)
                with open(rst_file_path, "r", encoding="utf-8") as rst_file:
                    rst_content = rst_file.read()

                rst_content = update_include_link_rst(rst_content, include_source_path)

                with open(rst_file_path, "w", encoding="utf-8") as rst_file:
                    rst_file.write(rst_content)


def update_include_link_rst(rst_content, include_source_path):
    pattern = r"\.\. include:: /includes/(.*?\.rst)"
    updated_content = re.sub(
        pattern, f".. include:: {include_source_path}/\\1", rst_content
    )

    return updated_content


def nextsteps():
    out = """
Tables:
- Build the Docusaurus docs and search for ---+ in the build folder to fix broken tables.
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
        title = match.group(1).replace("`", "")

        if ":" in title:
            title = f'"{title}"'

        title = title.replace("®\\*", "®*")
        title = title.replace("\\'s", "'s")
        title = title.replace(
            "{#opensearch-backup}", ""
        )

        beta_line = ""
        if "|beta|" in title:
            title = title.replace(" |beta|", "")
            beta_line = "beta: true"
            yaml_front_matter = f"---\ntitle: {title}\n{beta_line}\n---\n"
        else:
            yaml_front_matter = f"---\ntitle: {title}\n---\n"

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
    # look for `somepath`{.interpreted-text role="doc"}
    pattern_link_no_title = r"`(((\.\.)|(\/)).*?)`{\.interpreted-text\s+role=\"doc\"}"
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
    pattern = r"`(.*?)\s*<(.*?)>`{\.interpreted-text\s+role=\"doc\"}"
    return re.sub(pattern, r"[\1](\2)", md_content)


def delete_folders_until_docs(abs_path):
    # Validate if the provided path is absolute
    if not os.path.isabs(abs_path):
        raise ValueError("The provided path must be an absolute path.")

    # Split the path into components
    abs_path, _ = os.path.splitext(abs_path)
    path_components = abs_path.split(os.path.sep)

    # Find the index of 'docs' in the path
    docs_index = path_components.index("docs") if "docs" in path_components else -1

    # Check if 'docs' is found in the path
    if docs_index != -1:
        # Join the path components starting from 'docs'
        path_after_docs = os.path.join(os.path.sep, *path_components[docs_index:])

        return path_after_docs
    else:
        # 'docs' not found in the path
        raise ValueError("The '/docs/' folder was not found in the provided path.")


def fix_refs(md_content, all_titles):
    # `anchor`{\.interpreted-...
    pattern = r"`([^<>`]+)`{\.interpreted-text\s+role=\"ref\"}"

    def replace(match):
        anchor = match.group(1)

        # Loop through all_titles dictionary to find the matching key
        for file_path, subdictionary in all_titles.items():
            if anchor in subdictionary:
                # Replace the match with the formatted link
                return f"[{subdictionary[anchor]}]({delete_folders_until_docs(file_path)}#{anchor})"

        # If no match is found, return the original match
        # print(f"⚠️  Couldn't resolve ref. {anchor}")
        return match.group(0)

    # Use re.sub() with the custom replace function
    result = re.sub(pattern, replace, md_content)

    return result


def fix_anchor_links_same_page(md_content, all_titles, md_file_path):
    pattern = r"`([^<>`]+?)`{\.interpreted-text\s+role=\"ref\"}"
    titles = all_titles[md_file_path]

    def replace_match(match):
        anchor = match.group(1)
        title = titles.get(anchor)
        if title is not None:
            return f"[{title}](#{anchor})"
        else:
            # Return the original match if not found in titles dictionary
            return match.group(0)

    # Use re.sub to replace the matches with the dictionary values
    updated_content = re.sub(pattern, replace_match, md_content)
    return updated_content


def fix_refs_name(md_content, all_titles):
    # `name <anchor>`{\.interpreted-...
    pattern = r"`([^<>`]+)\s?<(.*?)>`{\.interpreted-text\s+role=\"ref\"}"

    def replace(match):
        name = match.group(1)
        anchor = match.group(2)

        # Loop through all_titles dictionary to find the matching key
        for file_path, subdictionary in all_titles.items():
            if anchor in subdictionary:
                # Replace the match with the formatted link
                link = delete_folders_until_docs(file_path) + "#" + anchor
                return f"[{name.strip()}]({link.strip()})"

        # If no match is found, return the original match
        # print(f"⚠️  Couldn't resolve ref. {name}: {anchor}")
        return match.group(0)

    # Use re.sub() with the custom replace function
    result = re.sub(pattern, replace, md_content)

    return result


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
    pattern = r":::topic\n\*\*(.*?)\*\*"
    matches = re.finditer(pattern, md_content, flags=re.DOTALL)

    updated_content = md_content
    for match in matches:
        matched_content = match.group(1)
        # Remove line breaks from matched content
        cleaned_content = matched_content.replace("\n", " ")
        # Build the replacement string
        replacement = f":::note[{cleaned_content}]"
        # Perform the substitution
        updated_content = re.sub(
            re.escape(match.group(0)), replacement, updated_content
        )

    updated_content = re.sub(r"(:::note\[.*\]\n)\n", r"\1", updated_content)
    return updated_content


def cleanup_md_docs_files(md_folder_path, destination_repo_path):
    print("\n🧹 Cleaning up MD files...")
    all_titles = {}
    for root, dirs, files in os.walk(md_folder_path):
        for file in files:
            if file.endswith(".md"):
                md_file_path = os.path.join(root, file)

                with open(md_file_path, "r", encoding="utf-8") as md_file:
                    md_content = md_file.read()
                    md_content = update_title(md_content)
                    all_titles[md_file_path] = extract_titles_with_anchors(md_content)
                    md_content = fix_admonitions(md_content)
                    md_content = fix_full_links(md_content)
                    md_content = fix_standalone_links(md_content)
                    md_content = fix_literal_includes(md_content)
                    md_content = process_seealso_blocks(md_content)
                    md_content = process_dropdowns(md_content)
                    md_content = process_topic_blocks(md_content)
                    md_content = comment_out_mermaid(md_content)
                    md_content = fix_codeblock_title(md_content)
                    md_content = process_grids(md_content)

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
                    md_content = fix_anchor_links_same_page(
                        md_content, all_titles, md_file_path
                    )
                    md_content = fix_no_name_links(md_content, destination_repo_path)
                    md_content = fix_refs(md_content, all_titles)
                    md_content = fix_refs_name(md_content, all_titles)
                    md_content = replace_anchors_in_content(md_content)
                    md_content = process_custom_markup(md_content)
                with open(md_file_path, "w", encoding="utf-8") as md_file:
                    md_file.write(md_content)


def fix_grids(md_folder_path):
    # only fix grids on landiing pages.
    pages = [
        "tools.md",
        "get-started.md",
        "integrations.md",
        "products/cassandra.md",
        "products/clickhouse.md",
        "products/dragonfly.md",
        "products/flink.md",
        "products/grafana.md",
        "products/influxdb.md",
        "products/kafka.md",
        "products/m3db.md",
        "products/mysql.md",
        "products/opensearch.md",
        "products/postgres.md",
        "products/redis.md",
        "products/cassandra/reference.md",
        "products/cassandra/howto/list-get-started.md",
        "products/clickhouse/concepts.md",
        "products/clickhouse/list-overview.md",
        "products/clickhouse/reference.md",
        "products/clickhouse/list-connect-to-service.md",
        "products/clickhouse/howto/list-get-started.md",
        "products/clickhouse/howto/list-integrations.md",
    ]
    # join path with md_folder_path
    for p in pages:
        try:
            with open(p, "r", encoding="utf-8") as md_file:
                md_content = md_file.read()
                md_content = process_grids(md_content)
            with open(p, "w", encoding="utf-8") as md_file:
                md_file.write(md_content)
        except FileNotFoundError:
            print(f"File not found: {p}")


def process_grids(md_content):
    # deletes grid instructions from the content
    grid_declaration = r"^::: ?grid\b.*:::"
    fix = r"import DocCardList from '@theme/DocCardList';\n\n<DocCardList />"
    content_final = re.sub(
        grid_declaration, fix, md_content, flags=re.MULTILINE | re.DOTALL
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
    md_content = md_content.replace("](sales@aiven.io) ", "](mailto:sales@aiven.io)")
    md_content = md_content.replace("::: {#Terminology", ":::Terminology")
    md_content = re.sub(
        r"{\.interpreted-text\s*?role=\"bdg-secondary\"}", "", md_content
    )

    md_content = re.sub(
        r"\n:::\s?tableofcontents\n:::\n", r"", md_content, flags=re.MULTILINE
    )
    md_content = re.sub(r"<(https://.*)>", r"[\1](\1)", md_content, flags=re.MULTILINE)

    return md_content


def fix_specific_files(repo_path):
    service_memory_capped = os.path.join(
        repo_path, "static/includes/services-memory-capped.md"
    )

    with open(service_memory_capped, "r", encoding="utf-8") as md_file:
        md_content = md_file.read()
        md_content = re.sub(r"^(\#+)", "#\1", md_content, flags=re.MULTILINE)
    with open(service_memory_capped, "w", encoding="utf-8") as md_file:
        md_file.write(md_content)

    service_memory_limits = os.path.join(
        repo_path, "docs/platform/concepts/service-memory-limits.md"
    )
    with open(service_memory_limits, 'a', encoding='utf-8') as file:
        import_statement = """
import Cap from '@site/static/includes/services-memory-capped.md'

<Cap/>
        """
        file.write(import_statement)


def replace_anchors_in_content(md_content):
    pattern = r"`(.*?)\s?<(.*)>`{\.interpreted-text\s*role=\"ref\"}"

    anchors_mapping = {
        "avn-service-logs": "/docs/tools/cli/service#avn-service-logs",
        "avn-service-metrics": "/docs/tools/cli/service#avn-service-metrics",
        "avn-cloud-list": "/docs/tools/cli/cloud#avn-cloud-list",
        "avn-service-cli": "/docs/tools/cli/service#avn-service-cli",
        "avn-service-database-create": "/docs/tools/cli/service/database#avn-service-database-create",
        "zookeeper": "#zookeeper",
        "avn-user-access-token-create": "/docs/tools/cli/user/user-access-token",
        "avn-service-user-create": "/docs/tools/cli/service/user#avn-service-user-create",
        "replicated-database-engine": "/docs/products/clickhouse/concepts/service-architecture#replicated-database-engine",
        "replicated-table-engine": "/docs/products/clickhouse/concepts/service-architecture#replicated-table-engine",
        "manage-roles-and-permissions": "/docs/products/clickhouse/howto/manage-users-roles#manage-roles-and-permissions",
        "networking-with-vpc-peering": "/docs/platform/concepts/cloud-security#networking-with-vpc-peering",
        "continuous-migration": "/docs/products/mysql/howto/migrate-db-to-aiven-via-console#about-migrating-via-console",
        "mysqldump-migration": "/docs/products/mysql/howto/migrate-db-to-aiven-via-console",
        "set-service-contacts": "/docs/platform/howto/technical-emails#set-service-contacts",
        "set-project-contacts": "/docs/platform/howto/technical-emails#set-project-contacts",
        "enable-prometheus": "/docs/platform/howto/integrations/prometheus-metrics#enable-prometheus",
        "remote-storage-overview": "/docs/products/kafka/howto/tiered-storage-overview-page#remote-storage-overview",
        "opensearch-backup": "/docs/products/opensearch/concepts/backups",
        "reference": "#reference",
        "stop-migration-mysql": "#stop-migration-mysql",
    }

    def replace_match(match):
        name = match.group(1)
        anchor = match.group(2)

        if anchor in anchors_mapping:
            replacement = f"[{name}]({anchors_mapping[anchor]})"
            return replacement
        else:
            # Return the original match if anchor is not in anchors_mapping
            print(f"{anchor} not found in mapping.")
            return match.group(0)

    updated_content = re.sub(pattern, replace_match, md_content)
    return updated_content


def process_dropdowns(md_content):
    pattern = r"(\s+)^(\s*):::dropdown\s*$(.*?)\n\n(.*?)^\s*:::\s*$"

    # Define the replacement pattern
    replacement = r"\1\2<details><summary>\3\n\2</summary>\n\n\4\n\2</details>\n"

    # Perform the replacement with re.MULTILINE and re.DOTALL flags
    result = re.sub(pattern, replacement, md_content, flags=re.MULTILINE | re.DOTALL)
    return result


def copy_folder_contents(source_path, destination_path):
    print(f"📸 Copying {source_path} into {destination_path}...")
    try:
        os.makedirs(destination_path, exist_ok=True)
        shutil.copytree(source_path, destination_path, dirs_exist_ok=True)
    except Exception as e:
        print(f"An error occurred: {e}")


def fix_codeblock_title(md_content):
    pattern = r"```\s?{\.(.*?) caption=\"(.*)\"}"
    replacement = r'```\1 title="\2"'
    result = re.sub(pattern, replacement, md_content, flags=re.MULTILINE)
    return result


def extract_titles_with_anchors(md_content):
    title_pattern = r"#+ (.+?) \{#(.+?)\}"
    title_matches = re.findall(title_pattern, md_content)
    titles_and_anchors = {anchor: title for title, anchor in title_matches}
    return titles_and_anchors


def comment_out_mermaid(md_content):
    pattern = r"(:::mermaid.*?:::)"
    updated_content = re.sub(pattern, r"<!--\n\1\n-->", md_content, flags=re.DOTALL)

    return updated_content

def delete_lines(md_folder_path):
    for file in os.listdir(md_folder_path):
        if file.endswith(".md"):
            md_file_path = os.path.join(md_folder_path, file)

            with open(md_file_path, "r", encoding="utf-8") as md_file:
                md_content = md_file.read()
                md_content = re.sub(r"^--------*\n", "", md_content, flags=re.MULTILINE)

            # write the changes
            with open(md_file_path, "w", encoding="utf-8") as md_file:
                md_file.write(md_content)
                # print(f"Wrote {md_file_path}")

def convert_pmtable_to_html(table_content):
    table_html = "<table>\n"
    headers = "  <thead>\n    <tr><th>Parameter</th><th>Information</th></tr>\n  </thead>"
    table_html += headers
    table_html += "\n  <tbody>\n"
    rows = table_content.strip().split('\n')

    for row in rows:
        columns = row.split('  ')
        columns = [col.strip() for col in columns if col.strip()]  # Remove empty strings
        if columns:
            table_html += "    <tr>\n"
            for col in columns:
                table_html += f"      <td>{col}</td>\n"
            table_html += "    </tr>\n"
    table_html += "  </tbody>\n"
    table_html += "</table>\n"

    return table_html

def convert_markup_to_html(md_content):
    table_pattern = re.compile(r"  Parameter\s+Information\s*[-]+\s*.*?\n(.*?)(?=\n\n|$)", re.DOTALL)

    def replace_table(match):
        table_content = match.group(1)
        return convert_pmtable_to_html(table_content)

    html_content = re.sub(table_pattern, replace_table, md_content)
    return html_content

# TODO
# check docs/products/kafka/howto/prevent-full-disks.md
# convert variables
# process ::: {#.*?}
# process [Integrated service]{.title-ref}.

if __name__ == "__main__":
    main()
