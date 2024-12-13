#!/bin/bash

# Set up virtual environment
VENV_DIR="venv"

echo "Checking if virtual environment exists..."
if [ ! -d "$VENV_DIR" ]; then
    echo "Virtual environment not found. Creating..."
    python3 -m venv $VENV_DIR
else
    echo "Virtual environment already exists."
fi

# Activate the virtual environment
echo "Activating virtual environment..."
source $VENV_DIR/bin/activate

# Install requirements
echo "Installing dependencies from requirements.txt..."
pip install --upgrade pip
pip install -r requirements.txt

# Run the main Python script
echo "Running the Python script..."
python main.py

# here's how to start
# sh ./setup_and_run.sh
