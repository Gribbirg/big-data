import os
import subprocess
from pathlib import Path
from PyPDF2 import PdfMerger

def html_to_pdf(html_file, pdf_file):
    cmd = [
        'python', '-m', 'weasyprint',
        str(html_file),
        str(pdf_file)
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(f'✓ Created: {pdf_file.name}')
        return True
    except subprocess.CalledProcessError as e:
        print(f'✗ Error creating {pdf_file.name}:')
        print(e.stderr)
        return False

def merge_pdfs(pdf_files, output_file):
    merger = PdfMerger()

    for pdf_file in pdf_files:
        if pdf_file.exists():
            merger.append(str(pdf_file))
            print(f'Added: {pdf_file.name}')
        else:
            print(f'Warning: {pdf_file.name} not found')

    merger.write(str(output_file))
    merger.close()
    print(f'\n✓ Final presentation saved: {output_file}')

def main():
    html_dir = Path('html')
    pdf_dir = Path('pdf')
    pdf_dir.mkdir(exist_ok=True)

    html_files = sorted(html_dir.glob('*.html'))

    print('Converting HTML to PDF...\n')
    pdf_files = []

    for html_file in html_files:
        pdf_file = pdf_dir / f'{html_file.stem}.pdf'
        if html_to_pdf(html_file, pdf_file):
            pdf_files.append(pdf_file)

    print(f'\nConverted {len(pdf_files)} slides to PDF\n')

    print('Merging PDFs...\n')
    output_file = Path('KNIME_Presentation.pdf')
    merge_pdfs(pdf_files, output_file)

    print(f'\n✓ Done! Total pages: {len(pdf_files)}')

if __name__ == '__main__':
    main()
