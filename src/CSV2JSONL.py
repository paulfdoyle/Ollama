import pandas as pd
import json
import os
import sys

# Function to convert CSV to JSONL
def convert_csv_to_jsonl(csv_file_path):
    encodings = ['utf-8-sig', 'latin1', 'cp1252']
    df = None
    
    for encoding in encodings:
        try:
            # Load CSV file into DataFrame with proper encoding to handle BOM
            df = pd.read_csv(csv_file_path, encoding=encoding)
            print(f"CSV file loaded successfully with encoding: {encoding}")
            break
        except Exception as e:
            print(f"Error reading CSV file with encoding {encoding}: {e}")
    
    if df is None:
        print("Failed to read CSV file with all attempted encodings.")
        sys.exit(1)
    
    # Generate JSONL file path in the current directory
    jsonl_file_name = os.path.splitext(os.path.basename(csv_file_path))[0] + '.jsonl'
    jsonl_file_path = os.path.join(os.getcwd(), jsonl_file_name)
    
    try:
        # Open JSONL file for writing
        with open(jsonl_file_path, 'w', encoding='utf-8') as jsonl_file:
            # Iterate over each row in DataFrame
            for _, row in df.iterrows():
                # Convert row to dictionary and write to JSONL
                json_record = row.to_dict()
                jsonl_file.write(json.dumps(json_record) + '\n')
        print(f"JSONL file created successfully at: {jsonl_file_path}")
    except Exception as e:
        print(f"Error writing JSONL file: {e}")
        sys.exit(1)

# Main function to handle command line arguments
def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <csv_file_path>")
        sys.exit(1)
    
    csv_file_path = sys.argv[1]
    convert_csv_to_jsonl(csv_file_path)

if __name__ == "__main__":
    main()

