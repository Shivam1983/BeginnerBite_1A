"""
This script resolves compatibility issues with the model and then runs the PDF processing.
"""
import os
import sys
import warnings

# Suppress warnings
warnings.filterwarnings("ignore")

def main():
    # First train a new model with the current scikit-learn version
    print("Step 1: Training a new model to ensure compatibility...")
    os.system("python analyze_pdf.py --mode train input_pdfs models")
    
    # Then process the PDFs
    print("\nStep 2: Processing PDFs with the newly trained model...")
    os.system("python analyze_pdf.py --mode analyze input_pdfs output")
    
    print("\nDone!")

if __name__ == "__main__":
    main()
