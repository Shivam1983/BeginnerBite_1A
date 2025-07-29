# """
# Heading detection and outline extraction.
# """

# import os
# import joblib
# import warnings
# import pickle

# from pdf_analyzer.core.document import parse_document
# from pdf_analyzer.core.analysis import extract_features
# from pdf_analyzer.utils.io_helpers import write_json
# from pdf_analyzer.config.paths import MODEL_PATH

# # Load the trained model with error handling
# try:
#     # Suppress scikit-learn version warnings
#     with warnings.catch_warnings():
#         warnings.simplefilter("ignore")
#         _data = joblib.load(MODEL_PATH)
#         _clf, _median_body = _data["model"], _data["median_body"]
# except (ImportError, ModuleNotFoundError, pickle.UnpicklingError) as e:
#     print(f"Error loading model: {e}")
#     print("Running model training to generate a compatible model...")
#     from pdf_analyzer.model.trainer import train_model
#     train_model()
#     _data = joblib.load(MODEL_PATH)
#     _clf, _median_body = _data["model"], _data["median_body"]

# def extract_document_outline(pdf_path):
#     """
#     Extract headings and structure from a single PDF document.
    
#     Args:
#         pdf_path (str): Path to the PDF file
        
#     Returns:
#         dict: Document outline with title and structured headings
#     """
#     # Declare globals at the beginning of the function
#     global _clf, _median_body
    
#     # Parse the document to extract spans
#     spans = parse_document(pdf_path)
    
#     # Extract features for classification
#     features = extract_features(spans, _median_body)
    
#     # Predict heading levels with error handling
#     try:
#         predictions = _clf.predict(features)
#     except (AttributeError, TypeError) as e:
#         print(f"Error with model compatibility: {e}")
#         print("Training a new model to ensure compatibility...")
#         from pdf_analyzer.model.trainer import train_model
#         train_model()
#         # Reload the model
#         _data = joblib.load(MODEL_PATH)
#         _clf, _median_body = _data["model"], _data["median_body"]
#         predictions = _clf.predict(features)
    
#     # Create outline structure
#     outline = [
#         {"level": f"H{p}", "text": s["text"], "page": s["page"]}
#         for s, p in zip(spans, predictions) if p > 0
#     ]
    
#     # Extract document title (level -1) or use filename as fallback
#     title = next((s["text"] for s, p in zip(spans, predictions) if p == -1), 
#                  os.path.basename(pdf_path))
    
#     return {"title": title, "outline": outline}

# def process_documents(input_dir, output_dir):
#     """
#     Process multiple PDF documents and generate outlines.
    
#     Args:
#         input_dir (str): Directory containing PDF files
#         output_dir (str): Directory where JSON outlines will be saved
#     """
#     os.makedirs(output_dir, exist_ok=True)
    
#     # Process each PDF file
#     for filename in os.listdir(input_dir):
#         if filename.lower().endswith(".pdf"):
#             # Path to input PDF
#             pdf_path = os.path.join(input_dir, filename)
            
#             # Output JSON path (replace .pdf with .json)
#             json_path = os.path.join(output_dir, filename[:-4] + ".json")
            
#             # Extract outline
#             outline = extract_document_outline(pdf_path)
            
#             # Save to JSON
#             write_json(outline, json_path)
            
#             print(f"Processed: {filename}")

#     print(f"All documents processed. Outlines saved to {output_dir}")
"""
Heading detection, outline extraction, and language identification.
"""

import os
import joblib
import warnings
import pickle
import langid

from pdf_analyzer.core.document import parse_document
from pdf_analyzer.core.analysis import extract_features
from pdf_analyzer.utils.io_helpers import write_json
from pdf_analyzer.config.paths import MODEL_PATH

# Load the trained model with error handling
try:
    # Suppress scikit‑learn version warnings
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        _data = joblib.load(MODEL_PATH)
        _clf, _median_body = _data["model"], _data["median_body"]
except (ImportError, ModuleNotFoundError, pickle.UnpicklingError) as e:
    print(f"Error loading model: {e}")
    print("Running model training to generate a compatible model...")
    from pdf_analyzer.model.trainer import train_model
    train_model()
    _data = joblib.load(MODEL_PATH)
    _clf, _median_body = _data["model"], _data["median_body"]


def extract_document_outline(pdf_path):
    """
    Extract headings, structure, and language from a single PDF document.
    
    Args:
        pdf_path (str): Path to the PDF file
        
    Returns:
        dict: {
            "title":   document title,
            "lang":    document‑level language code,
            "lang_confidence": document‑level confidence,
            "outline": [
                {
                    "level": "H1"…"H4",
                    "text":  span text,
                    "page":  page number,
                    "lang":  span’s language code,
                    "lang_confidence": span’s confidence
                }, …
            ]
        }
    """
    global _clf, _median_body

    # Parse the document to extract spans
    spans = parse_document(pdf_path)

    # Detect overall document language
    full_text = " ".join(s["text"] for s in spans)
    doc_lang, doc_conf = langid.classify(full_text)

    # Extract features for heading‑level classification
    features = extract_features(spans, _median_body)

    # Predict heading levels with error handling
    try:
        predictions = _clf.predict(features)
    except (AttributeError, TypeError) as e:
        print(f"Error with model compatibility: {e}")
        print("Training a new model to ensure compatibility...")
        from pdf_analyzer.model.trainer import train_model
        train_model()
        _data = joblib.load(MODEL_PATH)
        _clf, _median_body = _data["model"], _data["median_body"]
        predictions = _clf.predict(features)

    # Build the outline, attaching per‑span language detection
    outline = []
    for span, lvl in zip(spans, predictions):
        if lvl > 0:
            span_lang, span_conf = langid.classify(span["text"])
            outline.append({
                "level": f"H{lvl}",
                "text": span["text"],
                "page": span["page"],
                "lang": span_lang,
                "lang_confidence": span_conf
            })

    # Extract document title (level -1) or fallback to filename
    title = next(
        (s["text"] for s, lvl in zip(spans, predictions) if lvl == -1),
        os.path.basename(pdf_path)
    )

    return {
        "title": title,
        "lang": doc_lang,
        "lang_confidence": doc_conf,
        "outline": outline
    }


def process_documents(input_dir, output_dir):
    """
    Process multiple PDFs, generate outlines with language IDs, and save as JSON.
    
    Args:
        input_dir (str): Directory containing PDF files
        output_dir (str): Directory where JSON outlines will be saved
    """
    os.makedirs(output_dir, exist_ok=True)

    for filename in os.listdir(input_dir):
        if filename.lower().endswith(".pdf"):
            pdf_path = os.path.join(input_dir, filename)
            json_path = os.path.join(output_dir, filename[:-4] + ".json")

            outline = extract_document_outline(pdf_path)
            write_json(outline, json_path)
            print(f"Processed: {filename}")

    print(f"All documents processed. Outlines saved to {output_dir}")
