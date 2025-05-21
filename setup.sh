#!/bin/bash

echo "Starting setup script..."

# Check if virtual environment exists
if [ -d ".venv" ]; then
    echo "Virtual environment found. Activating..."
else
    echo "Virtual environment not found. Creating..."
    python3 -m venv .venv
fi

# Ensure virtual environment was created successfully
if [ ! -d ".venv" ]; then
    echo "Failed to create virtual environment."
    exit 1
fi

# Activate virtual environment based on OS
if [[ "$OSTYPE" == "darwin"* || "$OSTYPE" == "linux-gnu"* ]]; then
    source .venv/bin/activate
elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    source .venv/Scripts/activate
else
    echo "Unsupported OS for activation."
    exit 1
fi

if [ $? -ne 0 ]; then
    echo "Failed to activate virtual environment."
    exit 1
fi

echo "Virtual environment activated."

# Update pip, setuptools, and wheel
echo "Updating pip..."
pip install --upgrade pip setuptools wheel

# Install required packages
echo "Installing required packages..."
pip install -r requirements.txt 2>&1
sleep 3
echo "Setup complete!"
