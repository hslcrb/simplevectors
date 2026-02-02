#!/bin/bash
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$PROJECT_DIR/venv"

if [ ! -d "$VENV_DIR" ]; then
    echo "Virtual environment not found. Please run installation first."
    exit 1
fi

source "$VENV_DIR/bin/activate"

# Add src to PYTHONPATH so imports work correctly
export PYTHONPATH="$PROJECT_DIR/src:$PYTHONPATH"

# Run the application
python3 "$PROJECT_DIR/src/main.py"
