#!/bin/bash

# Local CI Checks Script
# This script runs all the same checks that run in CI/CD pipeline

set -e  # Exit on any error

echo "🚀 Running Local CI Checks for Backend"
echo "======================================="

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}📋 $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# Ensure we're in the backend directory
if [[ ! -f "requirements.txt" ]]; then
    echo "❌ Please run this script from the backend directory"
    exit 1
fi

# Check if virtual environment is activated
if [[ -z "$VIRTUAL_ENV" ]]; then
    print_warning "No virtual environment detected. Consider activating one."
fi

echo ""
print_status "Step 1: Installing/updating dependencies"
python -m pip install --upgrade pip > /dev/null
pip install -r requirements.txt > /dev/null
pip install -r requirements-dev.txt > /dev/null
print_success "Dependencies installed"

echo ""
print_status "Step 2: Code formatting with Black"
if black --check .; then
    print_success "Black formatting check passed"
else
    print_error "Black formatting check failed"
    echo "Run 'black .' to fix formatting issues"
    exit 1
fi

echo ""
print_status "Step 3: Import sorting with isort"
if isort --check-only .; then
    print_success "isort import sorting check passed"
else
    print_error "isort import sorting check failed"
    echo "Run 'isort .' to fix import sorting issues"
    exit 1
fi

echo ""
print_status "Step 4: Linting with flake8"
if flake8 .; then
    print_success "flake8 linting check passed"
else
    print_error "flake8 linting check failed"
    echo "Fix the linting issues shown above"
    exit 1
fi

echo ""
print_status "Step 5: Type checking with mypy"
if mypy --config-file mypy.ini src/; then
    print_success "mypy type checking passed"
else
    print_error "mypy type checking failed"
    echo "Fix the type errors shown above"
    exit 1
fi

echo ""
print_status "Step 6: Security check with bandit"
if bandit -r . -f json -o bandit-report.json; then
    print_success "bandit security check passed"
else
    print_warning "bandit security check found issues (not failing build)"
    echo "Check bandit-report.json for details"
fi

echo ""
print_status "Step 7: Running tests with pytest"
export TESTING=true
if PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 pytest -p pytest_cov --cov=src --cov-report=term-missing; then
    print_success "All tests passed"
else
    print_error "Tests failed"
    exit 1
fi

echo ""
print_status "Step 8: Test import functionality"
if python -c "import src.main; print('✅ Import test passed')"; then
    print_success "Module imports successfully"
else
    print_error "Module import failed"
    exit 1
fi

echo ""
echo "🎉 All CI checks passed! Your code is ready for CI/CD pipeline."
echo ""
echo "Next steps:"
echo "  - Commit your changes: git add . && git commit -m 'Your message'"
echo "  - Push to remote: git push"
echo "" 