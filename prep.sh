#!/bin/bash

# Function to calculate the checksum of requirements.txt
calculate_checksum() {
    if [ -f "requirements.txt" ]; then
        md5 -q requirements.txt
    else
        echo ""
    fi
}

# Check if the virtual environment exists
if [ ! -d ".venv" ]; then
    echo "Virtual environment not found. Creating it..."
    python -m venv .venv
fi

# Activate the virtual environment
source .venv/bin/activate

# Check if requirements.txt has changed
CHECKSUM_FILE=".venv/requirements_checksum.txt"
CURRENT_CHECKSUM=$(calculate_checksum)

if [ ! -f "$CHECKSUM_FILE" ] || [ "$CURRENT_CHECKSUM" != "$(cat $CHECKSUM_FILE)" ]; then
    if [ -f "requirements.txt" ]; then
        echo "requirements.txt has changed or is being installed for the first time. Installing dependencies..."
        pip install -r requirements.txt
        echo "$CURRENT_CHECKSUM" > $CHECKSUM_FILE
    else
        echo "No requirements.txt found. Skipping dependency installation."
    fi
else
    echo "requirements.txt has not changed. Skipping dependency installation."
fi

# Deactivate the virtual environment
deactivate