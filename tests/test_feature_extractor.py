"""
Tests for the feature extraction functionality.
"""

import unittest
import numpy as np
from pdf_analyzer.core.analysis import extract_features

class TestFeatureExtractor(unittest.TestCase):
    """Test cases for the feature extraction module."""

    def test_extract_features_basic(self):
        """Test basic feature extraction from spans."""
        # Sample test data
        spans = [
            {
                "text": "Sample Heading",
                "font_size": 14.0,
                "flags": 2,  # Bold
                "page": 1
            },
            {
                "text": "Regular paragraph text with more words.",
                "font_size": 10.0,
                "flags": 0,
                "page": 1
            },
            {
                "text": "1.2 Numbered Heading",
                "font_size": 12.0,
                "flags": 0,
                "page": 1
            }
        ]
        
        # Median body font size for relative sizing
        median_body_size = 10.0
        
        # Extract features
        features = extract_features(spans, median_body_size)
        
        # Assert expectations
        self.assertIsInstance(features, np.ndarray)
        self.assertEqual(features.shape, (3, 6))  # 3 spans, 6 features each
        
        # Check feature for bold heading
        self.assertEqual(features[0][0], 14.0)  # Font size
        self.assertEqual(features[0][1], 1)     # Bold flag
        
        # Check feature for numbered heading
        self.assertTrue(features[2][4])  # Should detect numbering pattern
        
        # Check relative size calculations
        self.assertEqual(features[0][5], 14.0/10.0)  # Heading relative size
        self.assertEqual(features[1][5], 10.0/10.0)  # Body relative size

if __name__ == "__main__":
    unittest.main()
