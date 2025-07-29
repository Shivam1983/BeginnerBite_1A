"""
Export lines from PDF files to create an annotation template.

This script extracts lines of text from PDF files (combining spans within a line)
and creates a CSV template that can be manually annotated to train the heading detection model.
"""

import os
import csv
import fitz  # PyMuPDF
import sys

# Add the project root to Python path to allow imports from pdf_analyzer
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pdf_analyzer.config.paths import DATA_DIR, PDF_INPUT_DIR, TEMPLATE_PATH

def main():
    """Extract lines from PDFs and create an annotation template CSV."""
    # Ensure output directory exists
    os.makedirs(os.path.dirname(TEMPLATE_PATH), exist_ok=True)
    
    print(f"Creating line-level annotation template from PDFs in {PDF_INPUT_DIR}")
    print(f"Output will be saved to {TEMPLATE_PATH}")
    
    with open(TEMPLATE_PATH, "w", newline="", encoding="utf-8") as f:
        # Create CSV writer and write header
        writer = csv.writer(f)
        writer.writerow(["pdf_file", "page", "text", "font_size", "x0", "y0", "flags", "label"])
        
        # Process each PDF file
        for filename in sorted(os.listdir(PDF_INPUT_DIR)):
            if not filename.lower().endswith(".pdf"):
                continue
                
            pdf_path = os.path.join(PDF_INPUT_DIR, filename)
            doc = fitz.open(pdf_path)
            
            # Process each page
            for page in doc:
                page_num = page.number + 1
                
                # Process each text block
                for block in page.get_text("dict")["blocks"]:
                    # Each block is a group of lines
                    for line in block.get("lines", []):
                        spans = line["spans"]
                        if not spans:
                            continue
                            
                        # Join all spans' text into one line
                        text = " ".join(s["text"].strip() for s in spans).strip()
                        if not text:
                            continue
                            
                        # Use the first span's font_size, flags, and bbox as representative
                        rep_span = spans[0]
                        bbox = rep_span.get("bbox", [0, 0, 0, 0])
                        
                        # Write line data to CSV
                        writer.writerow([
                            filename,
                            page_num,
                            text,
                            round(rep_span["size"], 1),
                            round(bbox[0], 1),
                            round(bbox[1], 1),
                            rep_span["flags"],
                            ""  # Empty label column to be filled manually
                        ])
    
    print(f"Line-level template CSV created: {TEMPLATE_PATH}")
    print("Next steps:")
    print("1. Open the CSV file and manually annotate the 'label' column with:")
    print("   -1 for document title")
    print("    0 for regular body text")
    print("    1 for H1 headings")
    print("    2 for H2 headings")
    print("    3 for H3 headings")
    print("2. Save the annotated file as 'data/annotations.csv'")
    print("3. Run 'python analyze_pdf.py --mode train input_pdfs models/'")

if __name__ == "__main__":
    main()
