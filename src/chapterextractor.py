import pdfplumber
import re
import os

def extract_chapters_from_pdf(pdf_path, output_dir):
    # Ensure output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Load the PDF
    with pdfplumber.open(pdf_path) as pdf:
        full_text = ""
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                full_text += page_text + "\n"

    # Split the text into chapters based on headings
    chapters = re.split(r'\n\d+\.\s+[A-Z][^\n]+', full_text)
    headings = re.findall(r'\n(\d+\.\s+[A-Z][^\n]+)', full_text)

    # Save each chapter to a separate text file
    for idx, chapter in enumerate(chapters[1:], start=1):
        # Clean the chapter title to create a valid filename
        title = headings[idx - 1].strip().replace(" ", "_").replace(".", "").replace("/", "-")
        filename = f'Chapter_{idx}_{title}.txt'
        file_path = os.path.join(output_dir, filename)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(chapter.strip())
        print(f'Saved: {file_path}')

# Example usage
if __name__ == '__main__':
    pdf_file = './Industry Work Placement Handbook August 2023.pdf'  # Replace with your PDF file path
    output_directory = './'  # Directory to save chapter files
    extract_chapters_from_pdf(pdf_file, output_directory)

