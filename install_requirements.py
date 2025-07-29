"""
Script to install required packages for the PDF Analyzer.
"""

import subprocess
import sys

def install_packages():
    """Install required packages."""
    packages = [
        "PyMuPDF",
        "click",
        "scikit-learn",
        "pandas",
        "joblib",
        "numpy",
    ]
    
    print("Installing required packages...")
    
    for package in packages:
        print(f"Installing {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    
    print("All packages installed successfully!")

if __name__ == "__main__":
    install_packages()
