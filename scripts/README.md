# Script Update Instructions

The scripts in the `scripts` directory have been updated to work with the new `pdf_analyzer` package structure. Here's how to use them:

## Using the Updated Scripts

1. **Export Spans Script** (`export_spans.py`)

   - This script extracts individual text spans from PDF files
   - Run: `python scripts/export_spans.py`
   - Output: `data/annotations_template.csv`

2. **Export Lines Script** (`export_lines_new.py`)
   - This script extracts whole lines from PDF files (by combining spans)
   - Run: `python scripts/export_lines_new.py`
   - Output: `data/annotations_template.csv`

## Annotation Process

After running either script:

1. Open the generated CSV file and manually annotate the 'label' column:

   - `-1` for document title
   - `0` for regular body text
   - `1` for H1 headings
   - `2` for H2 headings
   - `3` for H3 headings

2. Save the annotated file as `data/annotations.csv`

3. Train the model using the annotated data:

   ```
   python analyze_pdf.py --mode train data/input_pdfs models/
   ```

4. Run the extraction on your PDFs:
   ```
   python analyze_pdf.py --mode analyze data/input_pdfs output/
   ```

## Notes

- Both scripts now use the centralized path configuration from `pdf_analyzer.config.paths`
- The scripts add the project root to the Python path to enable imports from the package
