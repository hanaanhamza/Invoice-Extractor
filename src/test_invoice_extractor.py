import unittest
from invoice_extractor import search_value
from nlp_extractor import clean_value, extract_fields

class TestInvoiceExtractor(unittest.TestCase):
    """Simple unit tests for invoice extraction functions"""
    
    def test_search_value_found(self):
        """Test when pattern is found in text"""
        text = "Order ID: 12345 Customer: John Doe"
        result = search_value(r"\bOrder ID[:\s]*([\d]+)", text)
        self.assertEqual(result, "12345")
    
    def test_search_value_not_found(self):
        """Test when pattern is not found in text"""
        text = "Customer: John Doe"
        result = search_value(r"\bOrder ID[:\s]*([\d]+)", text)
        self.assertIsNone(result)
    
    def test_clean_value_removes_newlines(self):
        """Test that clean_value removes newlines"""
        dirty_text = "John\nDoe"
        cleaned = clean_value(dirty_text)
        self.assertEqual(cleaned, "John Doe")
    
    def test_extract_fields_finds_email(self):
        """Test that extract_fields finds email addresses"""
        text = "Contact us at john@example.com for more info"
        result = extract_fields(text)
        self.assertIn("john@example.com", result["emails"])
    
    def test_extract_fields_finds_phone(self):
        """Test that extract_fields finds phone numbers"""
        text = "Call us at 555-123-4567"
        result = extract_fields(text)
        self.assertTrue(len(result["phones"]) > 0)

if __name__ == '__main__':
    print("Running simple unit tests...")
    unittest.main(verbosity=2)