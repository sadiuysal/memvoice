# 🛠️ Local Development Guide

This guide shows you how to run all CI checks locally before pushing code to ensure your changes pass the CI pipeline.

## Quick Start

```bash
# 1. Auto-fix common issues
make format

# 2. Run all CI checks
make ci

# 3. If all checks pass, commit and push!
git add .
git commit -m "Your commit message"
git push
```

## Available Commands

### Development Commands

```bash
# Install dependencies
make install

# Start development server
make dev

# Run tests only
make test
```

### Code Quality Commands

```bash
# Auto-fix formatting and imports
make format

# Run linting checks only
make lint

# Run type checking only
make check

# Run all CI checks locally
make ci
```

### Utility Commands

```bash
# Clean temporary files
make clean

# Show help
make help
```

## Detailed Workflow

### 1. Before Making Changes

```bash
# Ensure dependencies are up to date
make install

# Start development server
make dev
```

### 2. After Making Changes

```bash
# Auto-fix formatting issues
make format

# Run full CI check suite
make ci
```

### 3. If CI Checks Fail

#### Formatting Issues
```bash
# Auto-fix with black and isort
make format
```

#### Test Failures
```bash
# Run tests in verbose mode to see details
make test
```

#### Type Checking Issues
```bash
# Run mypy to see type errors
make check
```

#### Linting Issues
```bash
# Run linting to see specific issues
make lint
```

### 4. Manual Commands (if needed)

```bash
# Individual tools
black .                    # Format code
isort .                    # Sort imports
flake8 .                   # Lint code
mypy --config-file mypy.ini src/  # Type check
pytest                     # Run tests
bandit -r .               # Security check
```

## Setting Up Pre-commit Hooks (Optional)

Pre-commit hooks automatically run checks before each commit:

```bash
# Install pre-commit
pip install pre-commit

# Install the hooks
pre-commit install

# Run hooks on all files
pre-commit run --all-files
```

Once installed, the hooks will run automatically on `git commit`.

## CI Pipeline Checks

The following checks run in CI and can be verified locally:

1. **Code Formatting** - Black ensures consistent code style
2. **Import Sorting** - isort organizes imports
3. **Linting** - flake8 catches common issues
4. **Type Checking** - mypy verifies type annotations
5. **Security** - bandit scans for security issues
6. **Tests** - pytest runs the test suite
7. **Import Test** - Verifies the module can be imported

## Troubleshooting

### Common Issues

1. **Port Already in Use**
   ```bash
   # Kill processes on port 8001
   lsof -ti:8001 | xargs kill -9
   ```

2. **Database Issues**
   ```bash
   # Clean up test database
   rm -f test.db
   ```

3. **Cache Issues**
   ```bash
   # Clean all caches
   make clean
   ```

### Environment Setup

1. **Create Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On macOS/Linux
   # or
   venv\Scripts\activate     # On Windows
   ```

2. **Install Dependencies**
   ```bash
   make install
   ```

3. **Environment Variables**
   ```bash
   # Copy example environment file
   cp .env.example .env
   
   # Edit .env with your settings
   nano .env
   ```

## Best Practices

1. **Always run `make ci` before pushing**
2. **Use `make format` to auto-fix common issues**
3. **Run tests after making changes: `make test`**
4. **Check individual tools if CI fails**
5. **Keep commits small and focused**
6. **Write descriptive commit messages**

## File Structure

```
backend/
├── scripts/
│   ├── run_ci_checks.sh     # Full CI check suite
│   └── fix_formatting.sh   # Auto-fix script
├── Makefile                 # Development commands
├── .pre-commit-config.yaml  # Pre-commit hooks
└── LOCAL_DEVELOPMENT.md     # This guide
```

## Configuration Files

- `pytest.ini` - Test configuration
- `mypy.ini` - Type checking configuration
- `.flake8` - Linting configuration
- `pyproject.toml` - Black configuration (if present)
- `.pre-commit-config.yaml` - Pre-commit hooks

## Getting Help

If you're still having issues:

1. Check the error messages carefully
2. Run individual commands to isolate the problem
3. Clean up temporary files: `make clean`
4. Ensure your virtual environment is activated
5. Check that all dependencies are installed: `make install`

Happy coding! 🚀 