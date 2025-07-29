# # """
# # Entry point script for PDF Analyzer.
# # """

# # import sys
# # import os
# # from pdf_analyzer.cli.commands import main


# # # Add the project root to Python path
# # sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# # print("Python Path:", sys.path)
# # print("Current Directory:", os.getcwd())

# # try:
# #     from pdf_analyzer.cli.commands import main
# #     print("Successfully imported main from pdf_analyzer.cli.commands")
# # except ImportError as e:
# #     print(f"Import Error: {e}")
# #     print("Files in current directory:", os.listdir("."))
# #     print("Files in pdf_analyzer:", os.listdir("pdf_analyzer"))
# #     print("Files in pdf_analyzer/cli:", os.listdir("pdf_analyzer/cli"))

# # if __name__ == "__main__":
# #     print("Starting PDF Analyzer...")
# #     try:
# #         main()
# #     except NameError:
# #         # If main is not defined, try running it a different way
# #         import click
# #         from pdf_analyzer.core.headings import process_documents
        
# #         print("Using alternative method to run...")
# #         input_dir = "input_pdfs"
# #         output_dir = "output"
# #         print(f"Processing PDFs from '{input_dir}' and saving outlines to '{output_dir}'...")
# #         process_documents(input_dir, output_dir)


# # # if __name__ == "__main__":
# # #     main()

# """
# Entry point script for PDF Analyzer.
# """

# import sys
# import os

# # 1) Make sure the project root is on sys.path before any imports
# root = os.path.abspath(os.path.dirname(__file__))
# sys.path.insert(0, root)

# print("Python Path:", sys.path)
# print("Current Directory:", os.getcwd())

# # 2) Try to import the click‑based CLI main()
# try:
#     from pdf_analyzer.cli.commands import main
#     print("✔️  Successfully imported main from pdf_analyzer.cli.commands")
# except ImportError as e:
#     print(f"❌ Import Error: {e}")
#     print("Files in cwd:", os.listdir("."))
#     print("Files in pdf_analyzer:", os.listdir("pdf_analyzer"))
#     print("Files in pdf_analyzer/cli:", os.listdir("pdf_analyzer/cli"))

#     # Fallback: wire up a simple process_documents entrypoint
#     def main():
#         from pdf_analyzer.core.headings import process_documents
#         input_dir = "input_pdfs"
#         output_dir = "output"
#         print(f"Using fallback: processing {input_dir} → {output_dir}")
#         process_documents(input_dir, output_dir)

# # 3) Single entrypoint guard
# if __name__ == "__main__":
#     print("Starting PDF Analyzer…")
#     main()



#!/usr/bin/env python3
import sys
import os
import argparse
# Ensure our package is on the path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from pdf_analyzer.core.headings import process_documents

def main():
    parser = argparse.ArgumentParser(
        description="PDF Analyzer: extract outlines from a folder of PDFs"
    )
    parser.add_argument(
    "input_dir",
    nargs='?',
    default="data/input_pdfs",
    help="Directory containing PDF files (default: data/input_pdfs/)"
    )
    parser.add_argument(
        "output_dir",
        nargs='?',
        default="output",
        help="Directory to write JSON outlines (default: output/)"
    )
    args = parser.parse_args()

    print(f"📂  Reading PDFs from: {args.input_dir!r}")
    print(f"💾  Writing outlines to: {args.output_dir!r}")
    process_documents(args.input_dir, args.output_dir)

if __name__ == "__main__":
    main()
