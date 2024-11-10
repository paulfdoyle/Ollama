import json
import PyPDF2
import sys
import os

# Function to extract text from a PDF file
def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page_num in range(len(reader.pages)):
            text += reader.pages[page_num].extract_text() + '\n'
    return text

# Function to convert PDF text to JSONL
def create_jsonl_from_pdf(pdf_path, jsonl_path):
    text = extract_text_from_pdf(pdf_path)
    lines = text.split('\n')
    
    if os.path.isdir(jsonl_path):
        jsonl_path = os.path.join(jsonl_path, os.path.basename(pdf_path).replace('.pdf', '.jsonl'))
    
    with open(jsonl_path, 'w', encoding='utf-8') as jsonl_file:
        for line in lines:
            if line.strip():  # Skip empty lines
                json_record = {"text": line.strip()}
                jsonl_file.write(json.dumps(json_record) + '\n')

# Main function to handle command line arguments
def main():
    if len(sys.argv) != 3:
        print("Usage: python script.py <pdf_path> <jsonl_path>")
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    jsonl_path = sys.argv[2]
    create_jsonl_from_pdf(pdf_path, jsonl_path)
    print(f"JSONL file created at: {jsonl_path}")

if __name__ == "__main__":
    main()

