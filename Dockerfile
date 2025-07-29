# # # Use Python 3.9 as base image
# # FROM python:3.9-slim AS builder

# # # Set working directory
# # WORKDIR /app

# # # Copy pip configuration
# # COPY pip.conf /etc/pip.conf

# # # Install system dependencies needed for PyMuPDF
# # RUN apt-get update && apt-get install -y \
# #     build-essential \
# #     libffi-dev \
# #     && rm -rf /var/lib/apt/lists/*

# # # Copy requirements file
# # # COPY requirements.txt .

# # COPY requirements.txt requirements_minimal.txt ./
# # RUN pip install --no-cache-dir -r requirements.txt
# # # # Install Python dependencies with increased timeout
# # RUN pip install --no-cache-dir -r requirements-minimal.txt

# # # Final stage
# # FROM python:3.9-slim

# # # Set working directory
# # WORKDIR /app

# # # Copy pip configuration
# # COPY pip.conf /etc/pip.conf

# # # Install system dependencies needed for PyMuPDF
# # RUN apt-get update && apt-get install -y \
# #     libffi-dev \
# #     && rm -rf /var/lib/apt/lists/*

# # # Copy installed packages from builder stage
# # COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
# # COPY --from=builder /usr/local/bin /usr/local/bin

# # # Copy project files
# # COPY input_pdfs/ /app/input_pdfs/
# # COPY data/ /app/data/
# # COPY pdf_analyzer/ /app/pdf_analyzer/
# # COPY analyze_pdf.py .
# # COPY setup.py .

# # # Create output and models directories
# # RUN mkdir -p /app/output /app/models

# # # Set environment variables
# # ENV PYTHONPATH=/app

# # # Default command - runs the analyzer in extraction mode
# # # Can be overridden at runtime
# # CMD ["python", "analyze_pdf.py", "--mode", "analyze", "input_pdfs", "output"]


# # ----------------------------
# # 1) Builder stage
# # ----------------------------
# FROM python:3.9-slim AS builder
# WORKDIR /app

# # copy your pip.conf (if you have a private index)
# COPY pip.conf /etc/pip.conf

# # install build tools for any native deps (e.g. PyMuPDF)
# RUN apt-get update && apt-get install -y \
#     build-essential \
#     libffi-dev \
#   && rm -rf /var/lib/apt/lists/*

# # copy both requirements files
# COPY requirements.txt requirements_minimal.txt ./

# # install everything in one go (underscore, not hyphen)
# RUN pip install --no-cache-dir --timeout=600 \
#       -r requirements.txt \
#       -r requirements_minimal.txt

# # ----------------------------
# # 2) Final stage
# # ----------------------------
# FROM python:3.9-slim
# WORKDIR /app

# COPY pip.conf /etc/pip.conf

# # only runtime deps needed
# RUN apt-get update && apt-get install -y \
#     libffi-dev \
#   && rm -rf /var/lib/apt/lists/*

# # bring in all the installed Python packages
# COPY --from=builder /usr/local/lib/python3.9/site‑packages /usr/local/lib/python3.9/site‑packages
# COPY --from=builder /usr/local/bin /usr/local/bin

# # copy your code
# COPY input_pdfs/ /app/input_pdfs/
# COPY data/        /app/data/
# COPY pdf_analyzer/ /app/pdf_analyzer/
# COPY analyze_pdf.py setup.py ./

# # create output and models dirs
# RUN mkdir -p /app/output /app/models

# ENV PYTHONPATH=/app

# # default command (can override at runtime)
# CMD ["python", "analyze_pdf.py", "--mode", "analyze", "input_pdfs", "output"]

# ----------------------------
# 1) Builder stage
# ----------------------------
FROM python:3.9-slim AS builder
WORKDIR /app

# copy pip config if you need it
COPY pip.conf /etc/pip.conf

# install build tools for native deps
RUN apt-get update && apt-get install -y \
    build-essential \
    libffi-dev \
  && rm -rf /var/lib/apt/lists/*

# copy requirements
COPY requirements.txt requirements_minimal.txt ./

# install everything (underscore filename)
RUN pip install --no-cache-dir --timeout=600 \
      -r requirements.txt \
      -r requirements_minimal.txt

# ----------------------------
# 2) Final stage
# ----------------------------
FROM python:3.9-slim
WORKDIR /app

COPY pip.conf /etc/pip.conf

RUN apt-get update && apt-get install -y \
    libffi-dev \
  && rm -rf /var/lib/apt/lists/*

# **Here** use ASCII "-" in "site-packages"
COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# copy your code and data
COPY input_pdfs/ /app/input_pdfs/
COPY data/        /app/data/
COPY pdf_analyzer/ /app/pdf_analyzer/
COPY analyze_pdf.py setup.py ./

# make sure output & models dirs exist
RUN mkdir -p /app/output /app/models
COPY models/        /app/models/

ENV PYTHONPATH=/app

# default entrypoint
CMD ["python", "analyze_pdf.py", "input_pdfs", "output"]
