#!/bin/bash

# Quick Fix Script
# Automatically fixes common formatting and linting issues

echo "🛠️  Auto-fixing code formatting and imports..."

# Fix import sorting first
echo "📦 Fixing import sorting with isort..."
isort .

# Then fix code formatting
echo "📝 Fixing code formatting with Black..."
black .

echo "✅ Auto-fixes completed!"
echo ""
echo "Next steps:"
echo "  1. Review the changes made"
echo "  2. Run './scripts/run_ci_checks.sh' to verify all checks pass"
echo "  3. Commit your changes" 