import os
import re
from pathlib import Path

def extract_slide_content(md_file):
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()

    text_on_slide_match = re.search(r'## Текст на слайде\s*\n(.*?)(?=##|$)', content, re.DOTALL)
    if text_on_slide_match:
        slide_text = text_on_slide_match.group(1).strip()
    else:
        slide_text = ""

    title_match = re.search(r'# (.+)', content)
    title = title_match.group(1) if title_match else "Слайд"

    return title, slide_text

def markdown_to_html(md_text):
    html = md_text

    html = re.sub(r'\*\*\*(.+?)\*\*\*', r'<strong><em>\1</em></strong>', html)
    html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
    html = re.sub(r'\*(.+?)\*', r'<em>\1</em>', html)
    html = re.sub(r'`(.+?)`', r'<code>\1</code>', html)

    lines = html.split('\n')
    processed_lines = []
    in_list = False
    list_type = None

    for line in lines:
        line = line.strip()

        if not line:
            if in_list:
                processed_lines.append(f'</{list_type}>')
                in_list = False
                list_type = None
            processed_lines.append('')
            continue

        if line.startswith('- '):
            if not in_list:
                processed_lines.append('<ul>')
                in_list = True
                list_type = 'ul'
            processed_lines.append(f'<li>{line[2:]}</li>')
        elif re.match(r'^\d+\.\s', line):
            if not in_list:
                processed_lines.append('<ol>')
                in_list = True
                list_type = 'ol'
            processed_lines.append(f'<li>{re.sub(r"^\d+\.\s", "", line)}</li>')
        else:
            if in_list:
                processed_lines.append(f'</{list_type}>')
                in_list = False
                list_type = None

            if line.startswith('###'):
                processed_lines.append(f'<h3>{line[3:].strip()}</h3>')
            elif line.startswith('##'):
                processed_lines.append(f'<h2>{line[2:].strip()}</h2>')
            elif line.startswith('#'):
                processed_lines.append(f'<h1>{line[1:].strip()}</h1>')
            elif line == '---':
                processed_lines.append('<hr>')
            else:
                processed_lines.append(f'<p>{line}</p>')

    if in_list:
        processed_lines.append(f'</{list_type}>')

    return '\n'.join(processed_lines)

def generate_html_slide(slide_number, title, content, is_title_slide=False):
    html_content = markdown_to_html(content)

    slide_class = "slide title-slide" if is_title_slide else "slide"

    html = f'''<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <link rel="stylesheet" href="../styles.css">
</head>
<body>
    <div class="{slide_class}">
        <div class="content">
{html_content}
        </div>
    </div>
</body>
</html>'''

    return html

def main():
    slides_dir = Path('../presentation/slides')
    html_dir = Path('html')
    html_dir.mkdir(exist_ok=True)

    md_files = sorted(slides_dir.glob('*.md'))

    for md_file in md_files:
        slide_number = md_file.stem.split('_')[0]
        title, content = extract_slide_content(md_file)

        is_title = '01_title' in md_file.name

        html_content = generate_html_slide(slide_number, title, content, is_title)

        html_file = html_dir / f'{md_file.stem}.html'
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)

        print(f'Generated: {html_file.name}')

if __name__ == '__main__':
    main()
