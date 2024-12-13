#!/bin/bash

# Define variables
VENV_DIR="venv"
REQUIREMENTS_FILE="requirements.txt"
APP_FILE="App/app.py"

# Check if virtual environment exists
if [ ! -d "$VENV_DIR" ]; then
    echo "Virtual environment not found. Creating one..."
    python3 -m venv $VENV_DIR
else
    echo "Virtual environment already exists."
fi

# Activate virtual environment
echo "Activating virtual environment..."
source $VENV_DIR/bin/activate

# Install dependencies
if [ -f "$REQUIREMENTS_FILE" ]; then
    echo "Installing dependencies from $REQUIREMENTS_FILE..."
    pip install --upgrade pip
    pip install -r $REQUIREMENTS_FILE
else
    echo "$REQUIREMENTS_FILE not found. Skipping dependency installation."
fi

# Run the Python application
if [ -f "$APP_FILE" ]; then
    echo "Running the application..."
    python $APP_FILE
else
    echo "Application file $APP_FILE not found."
fi

# Deactivate virtual environment
deactivate
echo "Virtual environment deactivated."
