import re


def convert_normal_pmtable_to_html(table_content):
    table_html = "<table>\n"
    headers = "  <thead>\n    <tr><th>Parameter</th><th>Information</th></tr>\n  </thead>"
    table_html += headers
    table_html += "\n  <tbody>\n"
    rows = table_content.split('\n')

    for row in rows:
        row = row[1:-1] # remove first and last char (|)
        if not "---" in row and len(row)>1:
          columns = row.split('|')
          if columns:
              table_html += "    <tr>\n"
              for col in columns:
                  table_html += f"      <td>{col.strip()}</td>\n"
              table_html += "    </tr>\n"
    table_html += "  </tbody>\n"
    table_html += "</table>\n"

    return table_html

def convert_pm2_to_html(md_content):

    regex = r"\+\-.*?$\n\| ?Parameter.+?Information.*?\n\+\=.*?\n(.*?)\+\-+?\+\-+\+\n\n"

    def replace_table(match):
        table_content = match.group(1)
        return convert_normal_pmtable_to_html(table_content)

    html_content= re.sub(regex, replace_table, md_content, 0, re.DOTALL | re.MULTILINE)

    return html_content

content = """
test

+------------------------------+--------------------------------------+
| Parameter                    | Information                          |
+==============================+======================================+
| `service_name`               | The name of the service              |
+------------------------------+--------------------------------------+
| `service_name`               | The name of the service              |
+------------------------------+--------------------------------------+

test

+-----------+-------------+
| Parameter | Information |
+===========+=============+
| `yes`     | a           |
+-----------+-------------+
| `no`      | b           |
+-----------+-------------+

test
"""

print(convert_pm2_to_html(content))