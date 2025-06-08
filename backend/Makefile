.PHONY: help install test lint format fix check ci dev clean

# Default target
help:
	@echo "🛠️  MemVoice Backend Development Commands"
	@echo "========================================"
	@echo ""
	@echo "Development:"
	@echo "  make install     Install dependencies"
	@echo "  make dev         Start development server"
	@echo "  make test        Run tests"
	@echo ""
	@echo "Code Quality:"
	@echo "  make format      Auto-fix formatting and imports"
	@echo "  make lint        Run linting checks only"
	@echo "  make check       Run type checking"
	@echo "  make ci          Run all CI checks locally"
	@echo ""
	@echo "Utilities:"
	@echo "  make clean       Clean up temporary files"
	@echo "  make help        Show this help message"

# Install dependencies
install:
	python -m pip install --upgrade pip
	pip install -r requirements.txt
	pip install -r requirements-dev.txt

# Start development server
dev:
	@echo "🚀 Starting development server..."
	unset DATABASE_URL && unset TEST_DATABASE_URL && uvicorn src.main:app --host 0.0.0.0 --port 8001 --reload

# Run tests
test:
	@echo "🧪 Running tests..."
	TESTING=true PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 pytest -p pytest_cov --cov=src --cov-report=term-missing -v

# Auto-fix formatting
format:
	@echo "🛠️  Auto-fixing formatting..."
	./scripts/fix_formatting.sh

# Run linting only
lint:
	@echo "🔍 Running linting checks..."
	black --check .
	isort --check-only .
	flake8 .

# Run type checking
check:
	@echo "🔍 Running type checks..."
	mypy --config-file mypy.ini src/

# Run all CI checks
ci:
	@echo "🚀 Running full CI check suite..."
	./scripts/run_ci_checks.sh

# Clean temporary files
clean:
	@echo "🧹 Cleaning up..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type f -name ".coverage" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	rm -f bandit-report.json
	rm -f test.db
	@echo "✅ Cleanup completed" 