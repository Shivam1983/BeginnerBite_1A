"""
Text analysis for heading detection.
"""

import re
import numpy as np

def extract_features(spans, median_body_size):
    """
    Extract features from text spans for heading classification.
    
    Args:
        spans (list): List of span dictionaries with text properties
        median_body_size (float): Median font size of body text
        
    Returns:
        numpy.ndarray: Feature matrix for classification
    """
    rows = []
    for span in spans:
        text = span["text"]
        font_size = span["font_size"]
        flags = span["flags"]
        
        # Calculate features
        rows.append([
            font_size,                                    # Absolute font size
            int(bool(flags & 2)),                         # Bold flag (1 if bold, 0 otherwise)
            len(text.split()),                            # Word count
            sum(1 for c in text if c.isupper()) / max(len(text), 1),  # Percentage of uppercase
            bool(re.match(r"^\d+\.\d+", text)),           # Starts with numbering pattern
            font_size / median_body_size if median_body_size else 1    # Relative font size
        ])
    
    return np.array(rows)
