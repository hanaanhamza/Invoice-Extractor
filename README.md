# Invoice Data Extraction System

A Python-based system for extracting structured data from PDF invoices.

## Features

- **PDF Processing**: Extracts text and tabular data from PDF invoices
- **Multi-method Extraction**: Combines regex patterns with NLP for robust data extraction
- **REST API**: Flask-based API for file upload and processing
- **CLI Interface**: Command-line tool for batch processing
- **JSON Output**: Structured data output with proper Unicode support

## Requirements

- Python 3.7+
- Required packages (install via `pip install -r requirements.txt`):
  - Flask
  - pdfplumber
  - spacy
  - spacy model: `python -m spacy download en_core_web_md`

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd Invoice-Extractor
```

2. Install dependencies:
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_md
```

## Usage

### CLI Usage

Process all PDF files in a folder:

```bash
python run_cli_extraction.py --input /path/to/input/folder --output /path/to/output/folder
```

**Example:**
```bash
python run_cli_extraction.py --input ./sample_invoices --output ./extracted_data
```

### REST API Usage

1. Start the API server:
```bash
python invoice_api_server.py
```

2. Upload a PDF file:
```bash
curl -X POST -F "file=@invoice.pdf" http://localhost:5000/parse
```

**Example with curl:**
```bash
curl -X POST -F "file=@sample_invoice.pdf" http://localhost:5000/parse -o output.json
```

**Example with Python requests:**
```python
import requests

with open('invoice.pdf', 'rb') as f:
    response = requests.post('http://localhost:5000/parse', files={'file': f})
    data = response.json()
    print(data)
```

## Output Format

The system extracts data into the following JSON structure:

```json
{
  "invoice_meta": {
    "order_id": "12345",
    "customer_id": "CUST001",
    "order_date": "2024-01-15",
    "total_price": "299.99"
  },
  "customer_details": {
    "contact_name": "John Doe",
    "phone": "+1-555-123-4567",
    "city": "New York"
  },
  "items": [
    {
      "product_id": "P001",
      "product_name": "Widget A",
      "quantity": "2",
      "unit_price": "10.00"
    }
  ],
  "nlp_metadata": {
    "dates": ["2024-01-15"],
    "people": ["John Doe"],
    "locations": ["New York"],
    "emails": ["john.doe@example.com"],
    "phones": ["+1-555-123-4567"]
  }
}
```
## Core Components
1. **`invoice_extractor.py`**: Main extraction logic

2. **`nlp_extractor.py`**: NLP-based field extraction

3. **`invoice_api_server.py`**: Flask REST API

4. **`run_cli_extraction.py`**: Command-line interface



## Testing

Run the unit tests:

```bash
python test_invoice_extractor.py
```


