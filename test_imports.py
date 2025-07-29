"""
Test script to verify imports are working correctly.
"""

import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

print("Verifying imports...")

# Test all the imports
try:
    print("Importing from pdf_analyzer.config.paths...")
    from pdf_analyzer.config.paths import PDF_INPUT_DIR, MODEL_PATH, OUTPUT_DIR
    print(f"PDF_INPUT_DIR = {PDF_INPUT_DIR}")
    print(f"MODEL_PATH = {MODEL_PATH}")
    print(f"OUTPUT_DIR = {OUTPUT_DIR}")
    
    print("\nImporting from pdf_analyzer.core.document...")
    from pdf_analyzer.core.document import parse_document
    print("parse_document function imported successfully")
    
    print("\nImporting from pdf_analyzer.core.analysis...")
    from pdf_analyzer.core.analysis import extract_features
    print("extract_features function imported successfully")
    
    print("\nImporting from pdf_analyzer.utils.io_helpers...")
    from pdf_analyzer.utils.io_helpers import write_json, read_annotations
    print("write_json and read_annotations functions imported successfully")
    
    print("\nImporting from pdf_analyzer.core.headings...")
    from pdf_analyzer.core.headings import extract_document_outline, process_documents
    print("extract_document_outline and process_documents functions imported successfully")
    
    print("\nImporting from pdf_analyzer.model.trainer...")
    from pdf_analyzer.model.trainer import train_model
    print("train_model function imported successfully")
    
    print("\nImporting from pdf_analyzer.cli.commands...")
    from pdf_analyzer.cli.commands import main
    print("main function imported successfully")
    
    print("\nAll imports verified successfully!")
    
except ImportError as e:
    print(f"Import Error: {e}")
    
except Exception as e:
    print(f"Error: {e}")

print("\nDone testing imports.")
