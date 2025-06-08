# MemVoice Development Setup Guide

This guide walks you through setting up the complete MemVoice development environment. The setup includes Docker containers for all services, development tools, and testing frameworks.

## 🚀 Quick Start

### Prerequisites

- **Docker** 20.10+ and **Docker Compose** 2.0+
- **Git** for version control
- **Node.js** 18+ (for local development without Docker)
- **Python** 3.11+ (for local development without Docker)

### One-Command Setup

```bash
# Clone and setup everything
git clone https://github.com/sadiuysal/memvoice.git
cd memvoice
./scripts/setup.sh
```

The setup script will:
1. ✅ Check prerequisites
2. ✅ Create `.env` from template
3. ✅ Build Docker containers
4. ✅ Start all services
5. ✅ Initialize database
6. ✅ Install pre-commit hooks
7. ✅ Verify service health

## 📋 Manual Setup (Step by Step)

### 1. Clone Repository

```bash
git clone https://github.com/sadiuysal/memvoice.git
cd memvoice
```

### 2. Environment Configuration

Copy the environment template and edit with your API keys:

```bash
cp env.template .env
```

**Required API Keys:**
- `OPENAI_API_KEY` - For Whisper STT and GPT models
- `ELEVENLABS_API_KEY` - For text-to-speech generation
- `PINECONE_API_KEY` - For vector database storage
- `ZEP_API_KEY` - For memory management

### 3. Start Services

```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Check service status
docker-compose ps
```

### 4. Verify Setup

After services start, verify everything is working:

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **PostgreSQL**: localhost:5432 (user: `memvoice_user`, db: `memvoice`)
- **Redis**: localhost:6379

## 🏗️ Architecture Overview

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend API   │    │   PostgreSQL    │
│   (Next.js)     │◄──►│   (FastAPI)     │◄──►│   Database      │
│   Port: 3000    │    │   Port: 8000    │    │   Port: 5432    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │     Redis       │
                       │   Cache/Queue   │
                       │   Port: 6379    │
                       └─────────────────┘
```

## 🛠️ Development Workflow

### Daily Development

```bash
# Start services
docker-compose up -d

# View logs for specific service
docker-compose logs -f backend
docker-compose logs -f frontend

# Run tests
./scripts/test.sh

# Stop services
docker-compose down
```

### Code Quality

The project uses automated code quality tools:

**Python (Backend):**
- **Black** - Code formatting
- **isort** - Import sorting
- **flake8** - Linting
- **mypy** - Type checking
- **bandit** - Security analysis

**TypeScript/JavaScript (Frontend):**
- **ESLint** - Linting
- **Prettier** - Code formatting
- **TypeScript** - Type checking

### Pre-commit Hooks

Pre-commit hooks run automatically on every commit:

```bash
# Install hooks (done by setup script)
pre-commit install

# Run manually
pre-commit run --all-files
```

## 🧪 Testing

### Run All Tests

```bash
./scripts/test.sh
```

### Specific Test Types

```bash
# Backend only
./scripts/test.sh --backend

# Frontend only
./scripts/test.sh --frontend

# With coverage
./scripts/test.sh --coverage

# End-to-end tests
./scripts/test.sh --e2e
```

### Manual Testing

```bash
# Backend tests
docker-compose exec backend pytest

# Frontend tests
docker-compose exec frontend npm test

# Type checking
docker-compose exec backend mypy src/
docker-compose exec frontend npm run type-check
```

## 📂 Project Structure

```
memvoice/
├── backend/                 # FastAPI backend
│   ├── src/                # Source code
│   ├── tests/              # Backend tests
│   ├── Dockerfile.dev      # Development Docker config
│   └── requirements*.txt   # Python dependencies
├── frontend/               # Next.js frontend
│   ├── src/                # Source code
│   ├── tests/              # Frontend tests
│   ├── Dockerfile.dev      # Development Docker config
│   └── package.json        # Node.js dependencies
├── scripts/                # Development scripts
│   ├── setup.sh            # Environment setup
│   └── test.sh             # Test runner
├── docs/                   # Project documentation
├── docker-compose.yml      # Docker services configuration
├── env.template            # Environment variables template
└── .pre-commit-config.yaml # Code quality configuration
```

## 🔧 Troubleshooting

### Common Issues

**Services won't start:**
```bash
# Check Docker daemon
docker info

# View detailed logs
docker-compose logs

# Rebuild containers
docker-compose build --no-cache
docker-compose up -d
```

**Port conflicts:**
```bash
# Check what's using ports
lsof -i :3000  # Frontend
lsof -i :8000  # Backend
lsof -i :5432  # PostgreSQL
lsof -i :6379  # Redis

# Kill conflicting processes
kill -9 <PID>
```

**Database connection issues:**
```bash
# Check PostgreSQL health
docker-compose exec postgres pg_isready -U memvoice_user -d memvoice

# Reset database
docker-compose down -v
docker-compose up -d
```

**Permission issues:**
```bash
# Fix script permissions
chmod +x scripts/*.sh

# Fix Docker permissions (Linux)
sudo usermod -aG docker $USER
# Log out and back in
```

### Environment Variables Issues

**Missing API keys:**
1. Copy `env.template` to `.env`
2. Add your actual API keys
3. Restart services: `docker-compose restart`

**Database connection:**
```bash
# Test connection
docker-compose exec postgres psql -U memvoice_user -d memvoice -c "SELECT version();"
```

### Development Tips

**Hot Reload Not Working:**
- Ensure volumes are properly mounted in `docker-compose.yml`
- Check file watching limits (Linux): `echo fs.inotify.max_user_watches=524288 | sudo tee -a /etc/sysctl.conf`

**Slow Performance:**
- Allocate more memory to Docker
- Use Docker BuildKit: `export DOCKER_BUILDKIT=1`
- Enable file sharing optimization in Docker settings

## 📚 Additional Resources

### Documentation
- [API Documentation](http://localhost:8000/docs) (when running)
- [Project Overview](docs/memvoice.wiki/Project-Overview.md)
- [Technical Architecture](docs/memvoice.wiki/Architecture.md)
- [Contribution Guide](docs/memvoice.wiki/Contribution-Guide.md)

### Development Commands

```bash
# Database operations
docker-compose exec postgres psql -U memvoice_user -d memvoice

# Backend shell
docker-compose exec backend bash

# Frontend shell
docker-compose exec frontend sh

# View container resources
docker stats

# Clean up unused resources
docker system prune -a
```

### VS Code Setup

Recommended VS Code extensions:
- Python (Microsoft)
- Pylance
- ES7+ React/Redux/React-Native snippets
- Prettier - Code formatter
- ESLint
- Docker
- Thunder Client (API testing)

## 🚀 Next Steps

After setup is complete:

1. **Explore the API**: Visit http://localhost:8000/docs
2. **Run tests**: `./scripts/test.sh`
3. **Check code quality**: `pre-commit run --all-files`
4. **Start developing**: Create a feature branch and start coding!

For implementation guidance, see:
- [Development Plan](docs/memvoice.wiki/Development-Plan.md)
- [Project Management](docs/memvoice.wiki/Project-Management.md)
- [FAQ & Troubleshooting](docs/memvoice.wiki/FAQ-Troubleshooting.md)

---

**Need help?** Open an issue or check the [FAQ](docs/memvoice.wiki/FAQ-Troubleshooting.md)!