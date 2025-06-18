import pdfplumber
import re
from nlp_extractor import extract_fields

def extract_invoice_data(file_path):
    invoice_data = {
        "invoice_meta": {},
        "customer_details": {},
        "items": [],
        "nlp_metadata": {}
    }

    try:
        with pdfplumber.open(file_path) as pdf:
            full_text = ""
            for page in pdf.pages:
                text = page.extract_text() or ""
                full_text += text + "\n"

                table = page.extract_table()
                if table:
                    for row in table[1:]:
                        if len(row) >= 4 and all(row[:3]):
                            invoice_data["items"].append({
                                "product_id": row[0],
                                "product_name": row[1],
                                "quantity": row[2],
                                "unit_price": row[3]
                            })

        # Regex-based extraction
        invoice_data["invoice_meta"]["order_id"] = search_value(r"\bOrder ID[:\s]*([\d]+)", full_text)
        invoice_data["invoice_meta"]["customer_id"] = search_value(r"\bCustomer ID[:\s]*([\w]+)", full_text)
        invoice_data["invoice_meta"]["order_date"] = search_value(r"\bOrder Date[:\s]*([\d\-]+)", full_text)
        invoice_data["invoice_meta"]["total_price"] = search_value(r"\bTotalPrice[:\s]*([\d.]+)", full_text)

        # NLP fallback metadata
        nlp_results = extract_fields(full_text)
        invoice_data["nlp_metadata"] = nlp_results

        if not invoice_data["customer_details"].get("contact_name") and nlp_results["people"]:
            invoice_data["customer_details"]["contact_name"] = nlp_results["people"][0]
        if nlp_results["phones"]:
            invoice_data["customer_details"]["phone"] = nlp_results["phones"][0]
        if nlp_results["locations"]:
            invoice_data["customer_details"]["city"] = nlp_results["locations"][0]

    except Exception as e:
        print(f"[ERROR] Failed to extract invoice: {e}")

    return invoice_data

def process_file(file_path):
    """Main function called by API - wrapper around extract_invoice_data"""
    return extract_invoice_data(file_path)

def search_value(pattern, text):
    match = re.search(pattern, text, re.IGNORECASE)
    return match.group(1).strip() if match else None