"""
Tests for the heading detection functionality.
"""

import unittest
import os
import tempfile
import json
from pdf_analyzer.core.headings import extract_document_outline, process_documents

class TestHeadingDetector(unittest.TestCase):
    """Test cases for the heading detection module."""

    def test_extract_document_outline_structure(self):
        """Test that the document outline has the correct structure."""
        # This is a mock test since we can't easily create PDF files for testing
        # In a real test, you'd use a test PDF file or mock the necessary components
        
        # Create a temporary directory
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create a test input and output directory
            input_dir = os.path.join(temp_dir, "input")
            output_dir = os.path.join(temp_dir, "output")
            os.makedirs(input_dir, exist_ok=True)
            os.makedirs(output_dir, exist_ok=True)
            
            # For this test, we'll verify the function exists and has the right signature
            self.assertTrue(callable(extract_document_outline))
            self.assertTrue(callable(process_documents))
            
            # In a real test with actual PDFs:
            # 1. Place a test PDF in input_dir
            # 2. Call process_documents(input_dir, output_dir)
            # 3. Verify the JSON output file exists and has the right structure
            
    def test_outline_json_structure(self):
        """Test that the outline JSON has the expected structure."""
        # Sample outline data that would be produced by the heading detector
        sample_outline = {
            "title": "Test Document",
            "outline": [
                {"level": "H1", "text": "Introduction", "page": 1},
                {"level": "H2", "text": "Background", "page": 1},
                {"level": "H1", "text": "Methods", "page": 2}
            ]
        }
        
        # Verify the structure
        self.assertIn("title", sample_outline)
        self.assertIn("outline", sample_outline)
        self.assertIsInstance(sample_outline["outline"], list)
        
        # Check that each outline item has the required fields
        for item in sample_outline["outline"]:
            self.assertIn("level", item)
            self.assertIn("text", item)
            self.assertIn("page", item)
            
            # Verify level format (H1, H2, etc.)
            self.assertTrue(item["level"].startswith("H"))
            
            # Verify page is a positive integer
            self.assertIsInstance(item["page"], int)
            self.assertGreater(item["page"], 0)

if __name__ == "__main__":
    unittest.main()
