#!/bin/bash
# Setup dependencies and submodules for macOS
set -e

# Initialize and update any git submodules
echo "Updating git submodules..."
git submodule update --init --recursive

# Ensure Homebrew is available for installing packages
if ! command -v brew >/dev/null 2>&1; then
  echo "Homebrew not found. Installing Homebrew..."
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi

# Ensure Python 3 is installed
if ! command -v python3 >/dev/null 2>&1; then
  echo "Python3 not found. Installing via Homebrew..."
  brew install python
fi

# Create a virtual environment for the project
python3 -m venv .venv
source .venv/bin/activate

# Upgrade pip and install Python dependencies
pip install --upgrade pip
pip install -r requirements.txt

echo "Setup complete. Activate the environment with 'source .venv/bin/activate'."
