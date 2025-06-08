#!/bin/bash

# Quick CI Check - Shows just the results
echo "🚀 Quick CI Check Results:"
echo "========================="

# Run each check and show pass/fail
echo -n "📝 Formatting: "
if black --check . >/dev/null 2>&1; then
    echo "✅ PASS"
else
    echo "❌ FAIL"
fi

echo -n "📦 Imports: "
if isort --check-only . >/dev/null 2>&1; then
    echo "✅ PASS"
else
    echo "❌ FAIL"
fi

echo -n "🔍 Linting: "
if flake8 . >/dev/null 2>&1; then
    echo "✅ PASS"
else
    echo "❌ FAIL"
fi

echo -n "🔍 Types: "
if mypy --config-file mypy.ini src/ >/dev/null 2>&1; then
    echo "✅ PASS"
else
    echo "❌ FAIL"
fi

echo -n "🧪 Tests: "
if TESTING=true pytest -q >/dev/null 2>&1; then
    echo "✅ PASS"
else
    echo "❌ FAIL"
fi

echo ""
echo "💡 Run 'make format' to auto-fix formatting issues"
echo "💡 Run 'make ci' for detailed output" 