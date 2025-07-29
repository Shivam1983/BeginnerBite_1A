#!/bin/bash

# Build Docker image
echo "Building Docker image..."
docker build -t pdf-analyzer .

# Run model training
echo "Running model training..."
docker run --rm \
  -v "$(pwd)/input_pdfs:/app/input_pdfs" \
  -v "$(pwd)/models:/app/models" \
  pdf-analyzer python analyze_pdf.py --mode train input_pdfs models

# Run PDF analysis
echo "Running PDF analysis..."
docker run --rm \
  -v "$(pwd)/input_pdfs:/app/input_pdfs" \
  -v "$(pwd)/models:/app/models" \
  -v "$(pwd)/output:/app/output" \
  pdf-analyzer python analyze_pdf.py --mode analyze input_pdfs output

echo "Done! Results are in the output directory."
