"""
Command-line interface for PDF Analyzer.
"""

import click
from pdf_analyzer.core.headings import process_documents
from pdf_analyzer.model.trainer import train_model

# Define path types for click validation
INPUT_PATH_TYPE = click.Path(exists=True, file_okay=False, dir_okay=True)
OUTPUT_PATH_TYPE = click.Path(file_okay=False, dir_okay=True)

@click.command()
@click.option(
    "--mode", 
    type=click.Choice(["train", "analyze"]),
    required=True,
    help="Operation mode: 'train' to train model, 'analyze' to extract PDF outlines"
)
@click.argument("input_dir", type=INPUT_PATH_TYPE)
@click.argument("output_dir", type=OUTPUT_PATH_TYPE)
def main(mode, input_dir, output_dir):
    """
    PDF Analyzer - Extract document outlines and headings from PDF files.
    
    INPUT_DIR: Directory containing PDF files
    OUTPUT_DIR: Directory where results will be saved
    """
    if mode == "train":
        print("Starting model training...")
        train_model()
        print("Model training completed.")
    else:  # mode == "analyze"
        print(f"Processing PDFs from '{input_dir}' and saving outlines to '{output_dir}'...")
        process_documents(input_dir, output_dir)
        print("PDF processing completed. Outlines generated.")

if __name__ == "__main__":
    main()
