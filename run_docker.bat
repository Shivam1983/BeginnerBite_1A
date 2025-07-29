@echo off
REM Windows batch script to build and run the Docker container

REM Build Docker image
echo Building Docker image...
docker build -t pdf-analyzer .

REM Run model training
echo Running model training...
docker run --rm ^
  -v "%cd%\input_pdfs:/app/input_pdfs" ^
  -v "%cd%\models:/app/models" ^
  pdf-analyzer python analyze_pdf.py --mode train input_pdfs models

REM Run PDF analysis
echo Running PDF analysis...
docker run --rm ^
  -v "%cd%\input_pdfs:/app/input_pdfs" ^
  -v "%cd%\models:/app/models" ^
  -v "%cd%\output:/app/output" ^
  pdf-analyzer python analyze_pdf.py --mode analyze input_pdfs output

echo Done! Results are in the output directory.
