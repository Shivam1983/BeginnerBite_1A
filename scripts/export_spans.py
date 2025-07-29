# import os, csv, fitz

# out_csv = "data/annotations_template.csv"
# pdf_folder = "data/input_pdfs"

# with open(out_csv, "w", newline="", encoding="utf-8") as f:
#     w = csv.writer(f)
#     w.writerow(["pdf_file","page","text","font_size","x0","y0","flags","label"])
#     for fname in os.listdir(pdf_folder):
#         if not fname.lower().endswith(".pdf"): continue
#         doc = fitz.open(os.path.join(pdf_folder, fname))
#         for p in doc:
#             for block in p.get_text("dict")["blocks"]:
#                 for line in block.get("lines", []):
#                     for span in line["spans"]:
#                         txt = span["text"].strip()
#                         if not txt: continue
#                         w.writerow([
#                             fname, p.number+1, txt,
#                             round(span["size"],1),
#                             round(span["bbox"][0],1),
#                             round(span["bbox"][1],1),
#                             span["flags"], ""
#                         ])
# print("Template CSV →", out_csv)





"""
Export all spans from PDF files to create an annotation template.

This script extracts text spans from PDF files and creates a CSV template
that can be manually annotated to train the heading detection model.
"""

import os
import csv
import fitz  # PyMuPDF
import sys

# Add the project root to Python path to allow imports from pdf_analyzer
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pdf_analyzer.config.paths import DATA_DIR, PDF_INPUT_DIR, TEMPLATE_PATH

def main():
    """Extract spans from PDFs and create an annotation template CSV."""
    # Ensure output directory exists
    os.makedirs(os.path.dirname(TEMPLATE_PATH), exist_ok=True)
    
    print(f"Creating annotation template from PDFs in {PDF_INPUT_DIR}")
    print(f"Output will be saved to {TEMPLATE_PATH}")
    
    with open(TEMPLATE_PATH, "w", newline="", encoding="utf-8") as f:
        # Create CSV writer and write header
        writer = csv.writer(f)
        writer.writerow(["pdf_file", "page", "text", "font_size", "x0", "y0", "flags", "label"])
        
        # Process each PDF file
        for filename in os.listdir(PDF_INPUT_DIR):
            if not filename.lower().endswith(".pdf"):
                continue
                
            pdf_path = os.path.join(PDF_INPUT_DIR, filename)
            doc = fitz.open(pdf_path)
            
            # Process each page
            for page in doc:
                page_num = page.number + 1
                
                # Process each text block
                for block in page.get_text("dict")["blocks"]:
                    for line in block.get("lines", []):
                        for span in line["spans"]:
                            text = span["text"].strip()
                            if not text:
                                continue
                                
                            # Write span data to CSV
                            writer.writerow([
                                filename,
                                page_num,
                                text,
                                round(span["size"], 1),
                                round(span["bbox"][0], 1),
                                round(span["bbox"][1], 1),
                                span["flags"],
                                ""  # Empty label column to be filled manually
                            ])
    
    print(f"Template CSV created: {TEMPLATE_PATH}")
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


