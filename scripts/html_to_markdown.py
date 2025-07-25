import os
import glob
from markdownify import markdownify as md

def convert_html_to_markdown(html_content: str) -> str:
    return md(html_content, heading_style="ATX")

def convert_files_in_docs():
    html_files = glob.glob('Docs/**/*.html', recursive=True)
    for html_file in html_files:
        with open(html_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
        markdown_content = convert_html_to_markdown(html_content)
        md_file = os.path.splitext(html_file)[0] + '.md'
        with open(md_file, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        print(f"Converted {html_file} to {md_file}")

if __name__ == "__main__":
    convert_files_in_docs()
