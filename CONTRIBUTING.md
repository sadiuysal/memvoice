# Contributing to MemVoice

Thank you for your interest in contributing to MemVoice! This document provides guidelines and information for contributors.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Project Structure](#project-structure)
- [Coding Standards](#coding-standards)
- [Testing Guidelines](#testing-guidelines)
- [Pull Request Process](#pull-request-process)
- [Issue Guidelines](#issue-guidelines)
- [Release Process](#release-process)

## 📜 Code of Conduct

This project adheres to a code of conduct. By participating, you are expected to uphold this code. Please report unacceptable behavior to the project maintainers.

### Our Standards

- Using welcoming and inclusive language
- Being respectful of differing viewpoints and experiences
- Gracefully accepting constructive criticism
- Focusing on what is best for the community
- Showing empathy towards other community members

## 🚀 Getting Started

### Prerequisites

- Node.js 18+ and npm
- Python 3.11+
- Git
- Docker (optional, for local development)

### Local Development Setup

1. **Fork and clone the repository**
   ```bash
   git clone https://github.com/your-username/memvoice.git
   cd memvoice
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys and configuration
   ```

3. **Install dependencies**
   ```bash
   # Backend
   cd backend
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   pip install -r requirements-dev.txt

   # Frontend
   cd ../frontend
   npm install
   ```

4. **Start development servers**
   ```bash
   # Terminal 1: Backend
   cd backend && uvicorn src.main:app --reload

   # Terminal 2: Frontend
   cd frontend && npm run dev
   ```

## 🔄 Development Workflow

### Branching Strategy

We use a Git flow-based branching strategy:

- `main` - Production-ready code
- `develop` - Integration branch for features
- `feature/*` - Feature development branches
- `bugfix/*` - Bug fix branches
- `hotfix/*` - Production hotfixes

### Creating a New Feature

1. **Create a new branch from develop**
   ```bash
   git checkout develop
   git pull origin develop
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Write tests for new functionality
   - Follow coding standards
   - Update documentation as needed

3. **Test your changes**
   ```bash
   # Run all tests
   npm run test:all

   # Run specific tests
   cd backend && pytest
   cd frontend && npm test
   ```

4. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: add new feature description"
   ```

5. **Push and create a Pull Request**
   ```bash
   git push origin feature/your-feature-name
   ```

### Commit Message Convention

We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

**Types:**
- `feat`: A new feature
- `fix`: A bug fix
- `docs`: Documentation only changes
- `style`: Changes that do not affect the meaning of the code
- `refactor`: A code change that neither fixes a bug nor adds a feature
- `perf`: A code change that improves performance
- `test`: Adding missing tests or correcting existing tests
- `build`: Changes that affect the build system or external dependencies
- `ci`: Changes to our CI configuration files and scripts

**Examples:**
```
feat(voice): add real-time voice processing
fix(memory): resolve token optimization bug
docs(api): update authentication documentation
test(frontend): add voice interface unit tests
```

## 🏗️ Project Structure

```
memvoice/
├── backend/                    # FastAPI backend service
│   ├── src/
│   │   ├── api/               # API routes and endpoints
│   │   ├── core/              # Core application logic
│   │   ├── models/            # Database models
│   │   ├── services/          # Business logic services
│   │   ├── utils/             # Utility functions
│   │   └── main.py           # Application entry point
│   ├── tests/                 # Backend tests
│   ├── alembic/              # Database migrations
│   ├── requirements.txt       # Production dependencies
│   ├── requirements-dev.txt   # Development dependencies
│   └── Dockerfile
├── frontend/                   # Next.js frontend application
│   ├── src/
│   │   ├── app/              # Next.js app directory
│   │   ├── components/       # React components
│   │   ├── hooks/            # Custom React hooks
│   │   ├── lib/              # Utility libraries
│   │   ├── store/            # State management
│   │   └── types/            # TypeScript type definitions
│   ├── public/               # Static assets
│   ├── tests/                # Frontend tests
│   └── package.json
├── docs/                      # Documentation
├── scripts/                   # Utility scripts
└── .github/                   # GitHub workflows and templates
```

## 🎨 Coding Standards

### Python (Backend)

We use the following tools for code quality:

- **Black** for code formatting
- **isort** for import sorting
- **flake8** for linting
- **mypy** for type checking
- **bandit** for security analysis

**Configuration files:**
- `pyproject.toml` - Black and isort configuration
- `.flake8` - Flake8 configuration
- `mypy.ini` - MyPy configuration

**Run quality checks:**
```bash
cd backend
black .
isort .
flake8 .
mypy .
bandit -r . -x tests/
```

### TypeScript/JavaScript (Frontend)

We use the following tools:

- **ESLint** for linting
- **Prettier** for code formatting
- **TypeScript** for type checking

**Run quality checks:**
```bash
cd frontend
npm run lint
npm run lint:fix
npm run type-check
```

### Code Style Guidelines

**General:**
- Use descriptive variable and function names
- Write self-documenting code with clear comments
- Keep functions small and focused on a single responsibility
- Use type hints in Python and TypeScript interfaces

**Python:**
- Follow PEP 8 style guide
- Use type hints for all function signatures
- Use docstrings for classes and functions
- Prefer composition over inheritance

**TypeScript/React:**
- Use functional components with hooks
- Prefer named exports over default exports
- Use TypeScript interfaces for props and state
- Follow React best practices and patterns

## 🧪 Testing Guidelines

### Testing Strategy

We follow a testing pyramid approach:

1. **Unit Tests (70%)** - Test individual functions and components
2. **Integration Tests (20%)** - Test component interactions
3. **End-to-End Tests (10%)** - Test complete user workflows

### Backend Testing

**Framework:** pytest

**Structure:**
```
tests/
├── unit/                 # Unit tests
├── integration/          # Integration tests
├── fixtures/            # Test fixtures
└── conftest.py          # Pytest configuration
```

**Running tests:**
```bash
cd backend
pytest                          # Run all tests
pytest tests/unit/             # Run unit tests only
pytest --cov=src              # Run with coverage
pytest -k "test_memory"        # Run specific tests
```

**Writing tests:**
```python
import pytest
from src.services.memory import MemoryService

class TestMemoryService:
    def test_add_memory(self):
        # Arrange
        service = MemoryService()
        content = "Test memory content"
        
        # Act
        result = service.add_memory(content)
        
        # Assert
        assert result.success is True
        assert result.memory_id is not None
```

### Frontend Testing

**Frameworks:** Jest, React Testing Library, Playwright

**Structure:**
```
tests/
├── unit/                 # Unit tests
├── integration/          # Integration tests
├── e2e/                 # End-to-end tests
└── __mocks__/           # Mocks and fixtures
```

**Running tests:**
```bash
cd frontend
npm test                        # Run all tests
npm run test:watch            # Run in watch mode
npm run test:coverage         # Run with coverage
npm run test:e2e              # Run E2E tests
```

**Writing tests:**
```typescript
import { render, screen } from '@testing-library/react';
import { VoiceInterface } from '@/components/VoiceInterface';

describe('VoiceInterface', () => {
  it('should render record button', () => {
    render(<VoiceInterface />);
    const recordButton = screen.getByRole('button', { name: /record/i });
    expect(recordButton).toBeInTheDocument();
  });
});
```

### Test Coverage Requirements

- **Minimum coverage:** 80% for all new code
- **Critical components:** 90%+ coverage required
- **Unit tests:** Must cover all public methods and functions
- **Integration tests:** Must cover API endpoints and component interactions

## 🔄 Pull Request Process

### Before Submitting

1. **Create an issue** first (unless it's a trivial change)
2. **Follow the branching strategy**
3. **Write tests** for new functionality
4. **Update documentation** as needed
5. **Run all tests** and ensure they pass
6. **Check code quality** tools pass

### PR Description Template

When creating a pull request, use our template which includes:

- **Description** of changes
- **Type of change** (feature, bugfix, etc.)
- **Testing** completed
- **Screenshots** (if applicable)
- **Checklist** of requirements

### Review Process

1. **Automated checks** must pass (CI/CD)
2. **Code review** by maintainers
3. **Testing verification** on review environment
4. **Approval** required before merge

### Merge Requirements

- [ ] All automated checks pass
- [ ] Code review approved
- [ ] Tests added for new functionality
- [ ] Documentation updated
- [ ] No merge conflicts

## 📝 Issue Guidelines

### Issue Types

We use the following issue types:

- **🐛 Bug Report** - Report a bug
- **✨ Feature Request** - Request a new feature
- **📋 Task** - Development task
- **🎯 Epic** - Large feature or initiative
- **📚 Documentation** - Documentation improvements

### Issue Labels

**Priority:**
- `priority/critical` - System down, security issues
- `priority/high` - Important features, major bugs
- `priority/medium` - Standard features and bugs
- `priority/low` - Nice-to-have improvements

**Type:**
- `type/bug` - Bug reports
- `type/feature` - New features
- `type/enhancement` - Improvements to existing features
- `type/documentation` - Documentation updates
- `type/maintenance` - Code maintenance and refactoring

**Component:**
- `component/frontend` - Frontend-related issues
- `component/backend` - Backend-related issues
- `component/voice-processing` - Voice processing pipeline
- `component/memory-management` - Memory management system
- `component/infrastructure` - Infrastructure and deployment

### Writing Good Issues

**For Bug Reports:**
- Provide clear steps to reproduce
- Include expected vs actual behavior
- Add screenshots or error messages
- Specify environment details

**For Feature Requests:**
- Describe the problem you're solving
- Explain the proposed solution
- Consider alternative approaches
- Define acceptance criteria

## 🚀 Release Process

### Version Numbering

We follow [Semantic Versioning](https://semver.org/):

- **MAJOR** version for incompatible API changes
- **MINOR** version for backwards-compatible functionality
- **PATCH** version for backwards-compatible bug fixes

### Release Workflow

1. **Feature freeze** on develop branch
2. **Create release branch** (`release/vX.Y.Z`)
3. **Final testing** and bug fixes
4. **Update version numbers** and changelog
5. **Merge to main** and tag release
6. **Deploy to production**
7. **Merge back to develop**

### Changelog

We maintain a changelog following [Keep a Changelog](https://keepachangelog.com/) format:

```markdown
## [1.2.0] - 2024-01-15

### Added
- New voice persona customization feature
- Real-time performance monitoring

### Changed
- Improved memory optimization algorithm
- Updated API response format

### Fixed
- Voice processing latency issues
- Memory leak in vector storage

### Security
- Updated dependencies with security patches
```

## 🆘 Getting Help

If you need help:

1. **Check the documentation** in the `/docs` directory
2. **Search existing issues** for similar problems
3. **Create a new issue** with detailed information
4. **Join our discussions** for general questions

## 📞 Contact

- **Issues**: [GitHub Issues](https://github.com/username/memvoice/issues)
- **Discussions**: [GitHub Discussions](https://github.com/username/memvoice/discussions)
- **Email**: contact@memvoice.dev

---

Thank you for contributing to MemVoice! 🎉 