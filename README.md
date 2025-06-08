# MemVoice: Memory-Optimized Voice Agent Pipeline

[![CI/CD](https://github.com/username/memvoice/workflows/CI/badge.svg)](https://github.com/username/memvoice/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com)

A memory-optimized voice agent service that transforms websites and document sets into interactive voice assistants. MemVoice uses advanced memory management techniques to provide efficient, natural voice interactions with minimal token usage.

## 🚀 Quick Start

### Prerequisites

- Node.js 18+ and npm
- Python 3.11+
- Docker (optional, for local development)
- API keys for:
  - OpenAI (Whisper, GPT)
  - ElevenLabs or similar TTS service
  - Pinecone (vector database)
  - Zep (memory management)

### Local Development Setup

#### 🚀 Quick Start (One Command)

```bash
# Clone the repository
git clone https://github.com/sadiuysal/memvoice.git
cd memvoice

# One-command setup with Docker
./scripts/setup.sh
```

This will automatically:
- Set up environment variables from template
- Build and start all Docker services
- Run database migrations
- Install dependencies
- Start development servers with hot reload

#### 📱 Access the Application

After setup completes, access the services at:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000  
- **API Documentation**: http://localhost:8000/docs
- **Database**: PostgreSQL on localhost:5432
- **Cache**: Redis on localhost:6379

#### 🔧 Manual Setup (Alternative)

If you prefer manual setup:

1. **Environment Setup**
   ```bash
   cp env.template .env
   # Edit .env with your API keys
   ```

2. **Start Services**
   ```bash
   # Use docker compose (v2) or docker-compose (v1)
   docker compose up -d
   # OR
   docker-compose up -d
   ```

3. **Run Tests**
   ```bash
   ./scripts/test.sh  # Run all tests
   ```

## 🏗️ Architecture

MemVoice consists of several integrated components:

- **Memory Management**: Zep-powered memory system with token optimization
- **Voice Processing**: Whisper STT + ElevenLabs TTS pipeline
- **Content Processing**: Website scraping and vectorization
- **Frontend**: Next.js React application
- **Backend**: FastAPI Python service

```mermaid
graph TB
    A[User Voice Input] --> B[Speech-to-Text]
    B --> C[Memory-Enhanced LLM]
    C --> D[Text-to-Speech]
    D --> E[User Voice Output]
    
    C <--> F[Memory Management]
    F <--> G[Vector Database]
    C <--> H[Content Retrieval]
    H --> I[Website Content]
```

## 📋 Features

### Current (MVP)
- ✅ Voice-to-voice interaction with websites
- ✅ Memory-optimized token usage (70% reduction)
- ✅ Real-time voice processing
- ✅ Website content extraction and vectorization
- ✅ Simple management dashboard

### Planned (Phase 2)
- 🔄 Multi-language support
- 🔄 Voice persona customization
- 🔄 Advanced analytics
- 🔄 API access for developers
- 🔄 Team collaboration features

## 🛠️ Development

### Tech Stack

**Backend:**
- Python 3.11+ with FastAPI
- Zep for memory management
- Pinecone for vector storage
- OpenAI Whisper for STT
- ElevenLabs for TTS

**Frontend:**
- Next.js 14 with TypeScript
- Tailwind CSS for styling
- React Hook Form for forms
- SWR for data fetching

**Infrastructure:**
- Vercel for frontend hosting
- Railway for backend deployment
- GitHub Actions for CI/CD

### Project Structure

```
memvoice/
├── backend/            # FastAPI backend application
│   ├── src/           # Python source code
│   ├── tests/         # Backend tests (pytest)
│   ├── scripts/       # Database scripts and utilities
│   └── Dockerfile.dev # Backend development container
├── frontend/          # Next.js frontend application
│   ├── src/           # TypeScript/React source code
│   ├── src/app/       # Next.js App Router pages
│   └── Dockerfile.dev # Frontend development container
├── scripts/           # Development automation scripts
│   ├── setup.sh       # One-command environment setup
│   └── test.sh        # Comprehensive test runner
├── .github/           # GitHub Actions workflows
├── docs/              # Project documentation
├── docker-compose.yml # Service orchestration
├── env.template       # Environment variables template
└── README.md          # Project overview
```

### Development Scripts

- **`./scripts/setup.sh`** - Complete environment setup with Docker
- **`./scripts/test.sh`** - Run all tests with coverage
- **`docker compose up -d`** - Start all services
- **`docker compose logs -f [service]`** - View service logs

### Contributing

See [DEVELOPMENT_SETUP.md](DEVELOPMENT_SETUP.md) for detailed development setup and workflow information.

## 🧪 Testing

```bash
# Run all tests with coverage
./scripts/test.sh

# Backend tests only
cd backend && PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 pytest -p pytest_cov --cov=src

# Frontend tests only
cd frontend && npm test

# Code quality checks
cd backend && black . && isort . && flake8 . && mypy --config-file mypy.ini src/
cd frontend && npm run lint && npm run format
```

### Test Coverage

The project includes comprehensive testing:
- **Backend**: pytest with coverage reporting
- **Frontend**: Jest with React Testing Library
- **Code Quality**: Black, isort, flake8, mypy, ESLint, Prettier
- **Security**: Bandit security analysis
- **CI/CD**: Automated testing on all pull requests

## 📚 Documentation

- [Development Setup Guide](DEVELOPMENT_SETUP.md) - Complete development environment setup
- [API Documentation](http://localhost:8000/docs) - Interactive API docs (when running locally)
- [GitHub Project Board](https://github.com/sadiuysal/memvoice/projects) - Project management and progress tracking
- [GitHub Issues](https://github.com/sadiuysal/memvoice/issues) - Feature requests and bug reports

## 🚀 Deployment

### Development Status

The development environment is complete and ready for use. Production deployment configuration is included in the CI/CD pipeline:

- **Frontend**: Configured for Vercel deployment
- **Backend**: Configured for Railway deployment  
- **Database**: PostgreSQL with Docker for development
- **CI/CD**: GitHub Actions with automated testing and deployment

Current focus is on MVP development before production deployment.

### Environment Variables

Copy the template and configure your environment:

```bash
cp env.template .env
```

Key variables to configure (see `env.template` for complete list):

```env
# Development (auto-configured by setup.sh)
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/memvoice
REDIS_URL=redis://localhost:6379
NEXT_PUBLIC_API_URL=http://localhost:8000

# Production API Keys (add when needed)
OPENAI_API_KEY=your_openai_key
ELEVENLABS_API_KEY=your_elevenlabs_key
PINECONE_API_KEY=your_pinecone_key
ZEP_API_KEY=your_zep_key
```

## 📊 Monitoring

- **Error Tracking**: Sentry integration
- **Performance**: Built-in monitoring
- **Uptime**: External monitoring service
- **Analytics**: Custom usage tracking

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Setup for Contributors

1. Fork the repository
2. Create a feature branch
3. Make your changes with tests
4. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Documentation**: Check our [docs](docs/) directory
- **Issues**: Open a [GitHub issue](https://github.com/username/memvoice/issues)
- **Discussions**: Join our [GitHub discussions](https://github.com/username/memvoice/discussions)

## 🗺️ Roadmap

### Phase 1: Foundation (Completed ✅)
- [x] **Development Environment Setup** - Docker, CI/CD, testing infrastructure
- [x] **Project Structure** - Backend (FastAPI), Frontend (Next.js), Database (PostgreSQL)
- [x] **Code Quality Tools** - Automated formatting, linting, security scanning
- [x] **Testing Framework** - pytest, Jest, coverage reporting

### Phase 2: Core Infrastructure (In Progress 🔄)
- [ ] **Backend API Foundation** - FastAPI endpoints, database models
- [ ] **Memory Management System** - Zep integration, token optimization  
- [ ] **Frontend Core** - React components, routing, state management
- [ ] **Voice Processing Pipeline** - Whisper STT, TTS integration

### Phase 2: Enhancement (Months 5-8)
- [ ] Multi-language support
- [ ] Advanced analytics
- [ ] Voice customization
- [ ] API access

### Phase 3: Scale (Months 9-12)
- [ ] Enterprise features
- [ ] Advanced integrations
- [ ] Team collaboration
- [ ] White-label solutions

## 📈 Metrics

Current MVP metrics targets:
- Voice processing latency: < 2 seconds
- Memory efficiency: 70% token reduction
- Uptime: 99.5%
- Customer satisfaction: NPS > 50

---

**Built with ❤️ by the MemVoice team** 