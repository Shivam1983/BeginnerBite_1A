
````markdown
# PDF Analyzer

PDF Analyzer automatically extracts document outlines and heading structure from PDF files. It provides a simple CLI and Docker setup so you can train a model on your own annotated PDFs and generate JSON outlines.

---

## Directory Structure

```text
Adobe_hackathon2025/
├── analyze_pdf.py
├── run_project.py
├── install_requirements.py
├── setup.py
├── run_docker.bat
├── run_docker.sh
├── Dockerfile
├── docker-compose.yml
├── .gitignore
├── .dockerignore
├── DOCKER.md
├── DOCKER_COMMANDS.md
├── DOCKER_INSTALL.md
├── README.md
├── NEW_README.md
├── pip.conf
├── requirements.txt
├── requirements-minimal.txt
├── test_imports.py
├── input_pdfs/
├── pdf_analyzer/
│   ├── __init__.py
│   ├── __main__.py
│   ├── cli/
│   ├── config/
│   ├── core/
│   ├── model/
│   └── utils/
├── scripts/
├── src/
└── tests/
````

---

## Installation

```bash
pip install -r requirements.txt
```

---

## Usage

1. **Prepare Training Data (optional)**

   ```bash
   python scripts/export_spans.py    # or export_lines_new.py
   # Fill in labels in data/annotations_template.csv
   mv data/annotations_template.csv data/annotations.csv
   ```

2. **Train the Model**

   ```bash
   python analyze_pdf.py --mode train input_pdfs models/
   ```

3. **Extract Outlines**

   ```bash
   python analyze_pdf.py --mode analyze input_pdfs output/
   ```

---

## Docker Support

### Build Image

```bash
docker build -t pdf-analyzer .
```

### Train

```bash
docker run --rm \
  -v "$(pwd)/input_pdfs:/app/input_pdfs" \
  -v "$(pwd)/models:/app/models" \
  pdf-analyzer \
  python analyze_pdf.py --mode train input_pdfs models/
```

### Analyze

```bash
docker run --rm \
  -v "$(pwd)/input_pdfs:/app/input_pdfs" \
  -v "$(pwd)/models:/app/models" \
  -v "$(pwd)/output:/app/output" \
  pdf-analyzer \
  python analyze_pdf.py --mode analyze input_pdfs output/
```

### Convenience Scripts

* **Windows**: `run_docker.bat`
* **Linux/macOS**:

  ```bash
  chmod +x run_docker.sh
  ./run_docker.sh
  ```

Refer to [DOCKER\_COMMANDS.md](DOCKER_COMMANDS.md) for more options.

---

## Project Components

* **Document Parser**
  Reads PDFs via PyMuPDF and extracts text spans with font metadata.

* **Feature Extractor**
  Converts spans into numeric features (font size, bold flag, word count, uppercase ratio, numbering pattern, relative size).

* **Model Trainer**
  Trains a Decision Tree on annotated data; saves `models/heading_model.joblib`.

* **Heading Detector**
  Loads the model and predicts heading levels to build a JSON outline.

Unit tests for parser, extractor and detector live in the `tests/` directory.

---

## Running Tests

```bash
pytest -v
```

