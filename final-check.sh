#!/bin/bash

echo "🔧 Starting final project health check..."

# Activate venv
echo "📦 Activating virtual environment..."
source venv/Scripts/activate

# Pull latest changes
echo "⬇️ Fetching and pulling latest changes from GitHub..."
git fetch
git pull origin main

# Run Flake8
echo "🧹 Running Flake8 linting..."
flake8

# Run Black (check mode first)
echo "🎨 Checking code formatting with Black..."
black --line-length 88 --check .

# Auto-fix with Black & autopep8
echo "🛠 Auto-fixing code formatting..."
black --line-length 88 .
autopep8 --in-place --recursive --max-line-length 88 .

# Re-run Flake8 after fixing
echo "🔁 Re-running Flake8 after auto-fix..."
flake8 || echo "⚠️ Some warnings remain (non-critical)."

# Stage and commit changes
echo "📥 Staging all changes..."
git add .

echo "✍️ Committing changes..."
git commit -m 'Final health check: Auto-format, lint fixes, and sync'

# Push to GitHub
echo "🚀 Pushing to remote repository..."
git push origin main

echo "✅ Final project health check complete and pushed!"
#!/bin/bash
set -e

echo "🔧 Starting final project health check..."

# 1️⃣ Activate virtual environment
if [ -d "venv" ]; then
  echo "📦 Activating virtual environment..."
  source venv/Scripts/activate
else
  echo "⚠️ Virtual environment not found. Exiting."
  exit 1
fi

# 2️⃣ Pull latest changes
echo "⬇️ Fetching and pulling latest changes from GitHub..."
git fetch
git pull origin main

# 3️⃣ Run Flake8 linting
echo "🧹 Running Flake8 linting..."
flake8 || echo "⚠️ Flake8 found issues!"

# 4️⃣ Run Black check
echo "🎨 Checking code formatting with Black..."
black --check .

# 5️⃣ Run pre-commit hooks
echo "🔄 Running pre-commit hooks..."
pre-commit run --all-files || echo "⚠️ Pre-commit found issues!"

# 6️⃣ Show git status
echo "📂 Displaying Git status..."
git status

echo "✅ Final check complete!"

