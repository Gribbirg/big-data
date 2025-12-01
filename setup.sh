#!/bin/bash

# Setup script for big-data project
# Works on macOS and Linux

echo "Setting up big-data project..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install required packages
echo "Installing dependencies..."
pip install pandas scikit-learn jupyter matplotlib seaborn numpy scipy plotly umap-learn statsmodels xgboost

echo "Setup complete!"
echo ""
echo "To activate the virtual environment manually, run:"
echo "source .venv/bin/activate"
echo ""
echo "To start Jupyter notebook, run:"
echo "jupyter notebook"