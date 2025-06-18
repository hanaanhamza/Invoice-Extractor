import os
import json
import argparse
from invoice_extractor import extract_invoice_data  # Fixed import

def process_folder(input_folder, output_folder):
    os.makedirs(output_folder, exist_ok=True)

    for file in os.listdir(input_folder):
        if file.lower().endswith(".pdf"):
            input_path = os.path.join(input_folder, file)
            output_path = os.path.join(output_folder, file.replace(".pdf", ".json"))

            data = extract_invoice_data(input_path)
            with open(output_path, "w", encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)  # Key changes here
            print(f"Saved: {output_path}")
        else:
            print(f"Error: Unsupported file type")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    process_folder(args.input, args.output)