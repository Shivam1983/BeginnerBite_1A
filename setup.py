from setuptools import setup, find_packages

setup(
    name="pdf_analyzer",
    version="1.0.0",
    description="Extract document outlines and headings from PDF files",
    author="Adobe Hackathon Team",
    packages=find_packages(),
    install_requires=[
        "PyMuPDF",
        "sentence-transformers",
        "rank_bm25",
        "click",
        "scikit-learn",
        "pandas",
        "joblib",
    ],
    entry_points={
        "console_scripts": [
            "pdf-analyzer=pdf_analyzer.cli.commands:main",
        ],
    },
    python_requires=">=3.8",
)
