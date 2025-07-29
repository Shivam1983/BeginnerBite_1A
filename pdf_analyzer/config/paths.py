"""
Paths configuration for the PDF Analyzer.
"""

import os

# Get absolute path for the base project directory
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))

# Data paths
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
ANNOTATIONS_PATH = os.path.join(DATA_DIR, "annotations.csv")
TEMPLATE_PATH = os.path.join(DATA_DIR, "annotations_template.csv")

# Input PDF path (moved to root level)
PDF_INPUT_DIR = os.path.join(PROJECT_ROOT, "input_pdfs")

# Model paths
MODEL_DIR = os.path.join(PROJECT_ROOT, "models")
MODEL_PATH = os.path.join(MODEL_DIR, "heading_model.joblib")

# Output paths
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "output")

# Output paths
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "output")
