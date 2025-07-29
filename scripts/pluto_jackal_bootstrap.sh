#!/bin/bash
echo "🚀 Bootstrapping Pluto-Jackal environment..."

cd "$(dirname "$0")/.."

echo "📦 Installing Python environment..."
python -m venv venv
source venv/Scripts/activate || source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt || echo "⚠️ No requirements.txt found, skipping..."

if [ -f "package.json" ]; then
    echo "📦 Installing Node modules..."
    npm install
else
    echo "⚠️ No package.json found, skipping Node setup..."
fi

if [ -z "$GITHUB_PAT" ]; then
    echo "🔑 Please enter your GitHub PAT:"
    read -r GITHUB_PAT
    export GITHUB_PAT=$GITHUB_PAT
fi
git config --global credential.helper store

echo "🤖 Setting up AI runtime..."
pip install litellm openai
npm install -g @modelcontextprotocol/cli

mkdir -p runtime/logs runtime/agents

echo "✅ Pluto-Jackal bootstrap complete!"
echo "Next: run 'pluto-jackal init --agents founding' to initialize AI agents."
