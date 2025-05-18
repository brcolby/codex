#!/bin/bash
# Simple helper to install OpenAI python package and store API key in .env.
set -e

if ! python3 -c "import openai" >/dev/null 2>&1; then
    echo "Installing openai package..."
    pip install openai
fi

read -p "Enter your OpenAI API key: " OPENAI_API_KEY

cat > .env <<EOL
OPENAI_API_KEY=$OPENAI_API_KEY
EOL

echo "OpenAI API key saved to .env"

echo "Setup complete. Load the key with 'export \$(cat .env | xargs)'"

