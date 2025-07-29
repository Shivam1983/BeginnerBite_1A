"""
Model training for heading detection.
"""

import os
import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

from pdf_analyzer.core.analysis import extract_features
from pdf_analyzer.utils.io_helpers import read_annotations
from pdf_analyzer.config.paths import MODEL_DIR, MODEL_PATH

def train_model():
    """
    Train and save a heading detection model using the labeled annotations.
    
    Returns:
        tuple: The trained model and the median body font size
    """
    print("Loading annotations data...")
    df = read_annotations()
    
    # Calculate median font size for body text (label 0)
    median_body = df[df.label == 0]["font_size"].median()
    print(f"Median body font size: {median_body}")
    
    # Convert DataFrame to list of dicts for feature extraction
    spans = df.to_dict("records")
    
    # Extract features and get labels
    X = extract_features(spans, median_body)
    y = df["label"].values
    
    # Split into training and validation sets
    X_train, X_val, y_train, y_val = train_test_split(
        X, y, stratify=y, test_size=0.2, random_state=42)
    
    print(f"Training with {X_train.shape[0]} samples, validating with {X_val.shape[0]} samples")
    
    # Train a Decision Tree model
    print("Training model...")
    clf = DecisionTreeClassifier(random_state=42)
    clf.fit(X_train, y_train)
    
    # Evaluate the model
    val_preds = clf.predict(X_val)
    print("\nModel Performance:")
    print(classification_report(y_val, val_preds, digits=3))
    
    # Save the model and median body font size
    os.makedirs(MODEL_DIR, exist_ok=True)
    
    model_data = {
        "model": clf,
        "median_body": float(median_body)
    }
    
    joblib.dump(model_data, MODEL_PATH)
    print(f"Model saved to {MODEL_PATH}")
    
    return clf, median_body
