"""
PDF document parsing functionality.
"""

import fitz  # PyMuPDF

def parse_document(pdf_path):
    """
    Extract text spans with their properties from a PDF document.
    
    Args:
        pdf_path (str): Path to the PDF file
        
    Returns:
        list: List of span dictionaries with text and formatting information
    """
    spans = []
    doc = fitz.open(pdf_path)
    
    for page in doc:
        page_num = page.number + 1
        for block in page.get_text("dict")["blocks"]:
            for line in block.get("lines", []):
                for span in line["spans"]:
                    text = span["text"].strip()
                    if not text:
                        continue
                        
                    spans.append({
                        "pdf_file": pdf_path,
                        "page": page_num,
                        "text": text,
                        "font_size": span["size"],
                        "x0": span["bbox"][0],
                        "y0": span["bbox"][1],
                        "flags": span["flags"]
                    })
    
    return spans
