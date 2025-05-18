#!/bin/bash
# Simple helper to store Mistral API key in .env.
set -e

read -p "Enter your Mistral API key: " MISTRAL_API_KEY

cat > .env <<EOL
MISTRAL_API_KEY=$MISTRAL_API_KEY
EOL

echo "Mistral API key saved to .env"

echo "Setup complete. Load the key with 'export \$(cat .env | xargs)'"

