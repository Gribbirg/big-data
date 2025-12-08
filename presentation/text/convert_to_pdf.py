import markdown
from weasyprint import HTML, CSS
from pathlib import Path

md_file = Path('full_speech.md')
pdf_file = Path('full_speech.pdf')

with open(md_file, 'r', encoding='utf-8') as f:
    md_content = f.read()

html_content = markdown.markdown(md_content)

html_template = f'''<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>KNIME Analytics Platform — Полный текст выступления</title>
    <style>
        @page {{
            size: A4;
            margin: 2cm;
        }}
        body {{
            font-family: "DejaVu Sans", Arial, sans-serif;
            font-size: 12pt;
            line-height: 1.6;
            color: #333;
        }}
        h1 {{
            font-size: 20pt;
            margin-top: 1em;
            margin-bottom: 0.5em;
            color: #2c3e50;
        }}
        h2 {{
            font-size: 16pt;
            margin-top: 1em;
            margin-bottom: 0.5em;
            color: #34495e;
        }}
        h3 {{
            font-size: 14pt;
            margin-top: 0.8em;
            margin-bottom: 0.4em;
            color: #555;
        }}
        p {{
            margin-bottom: 0.8em;
        }}
        hr {{
            border: none;
            border-top: 1px solid #ccc;
            margin: 1.5em 0;
        }}
    </style>
</head>
<body>
{html_content}
</body>
</html>'''

HTML(string=html_template).write_pdf(pdf_file)
print(f'✓ PDF created: {pdf_file}')
