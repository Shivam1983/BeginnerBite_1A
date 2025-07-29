"""
File I/O helper functions.
"""

import os
import json
import pandas as pd
from pdf_analyzer.config.paths import ANNOTATIONS_PATH

def write_json(data, filepath):
    """
    Write data to a JSON file.
    
    Args:
        data (dict): The data to write
        filepath (str): Path to the output JSON file
    """
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    # Write to file with proper formatting
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def read_annotations():
    """
    Read the annotations CSV file with labeled heading data.
    
    Returns:
        pandas.DataFrame: DataFrame containing labeled spans
    """
    if not os.path.exists(ANNOTATIONS_PATH):
        print(f"Error: {ANNOTATIONS_PATH} not found.")
        print("Please ensure you have generated the template using scripts/export_spans.py")
        print("and then manually labeled it and saved as data/annotations.csv.")
        raise FileNotFoundError(f"Annotations file not found: {ANNOTATIONS_PATH}")

    # Read and validate the CSV
    df = pd.read_csv(ANNOTATIONS_PATH)
    
    # Ensure required columns exist
    required_cols = ["text", "font_size", "flags", "label"]
    missing = [col for col in required_cols if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns in annotations file: {', '.join(missing)}")
    
    # Ensure label column is integer type for consistency
    df["label"] = df["label"].astype(int)
    
    return df
