#!/bin/bash

# MemVoice Development Environment Setup Script
# This script sets up the complete development environment

set -e  # Exit on any error

echo "🚀 Starting MemVoice Development Environment Setup..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    print_error "Docker is not installed. Please install Docker and try again."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    print_error "Docker Compose is not installed. Please install Docker Compose and try again."
    exit 1
fi

print_status "Docker and Docker Compose are installed"

# Check if .env file exists
if [ ! -f .env ]; then
    print_warning ".env file not found. Creating from template..."
    cp env.template .env
    print_warning "Please edit .env file with your API keys before continuing"
    echo ""
    echo "Required API keys:"
    echo "- OPENAI_API_KEY (for Whisper STT and GPT)"
    echo "- ELEVENLABS_API_KEY (for TTS)"
    echo "- PINECONE_API_KEY (for vector database)"
    echo "- ZEP_API_KEY (for memory management)"
    echo ""
    read -p "Press Enter after editing .env file..."
fi

print_status ".env file exists"

# Create necessary directories
mkdir -p backend/src
mkdir -p backend/tests
mkdir -p frontend/src
mkdir -p frontend/tests
mkdir -p logs
mkdir -p data

print_status "Created project directories"

# Stop any existing containers
echo "🔄 Stopping any existing containers..."
docker-compose down --remove-orphans

# Build and start services
echo "🏗️  Building and starting services..."
docker-compose build --no-cache
docker-compose up -d

# Wait for services to be healthy
echo "⏳ Waiting for services to be ready..."
sleep 10

# Check service health
echo "🔍 Checking service health..."

# Check PostgreSQL
if docker-compose exec postgres pg_isready -U memvoice_user -d memvoice; then
    print_status "PostgreSQL is ready"
else
    print_error "PostgreSQL failed to start"
    exit 1
fi

# Check Redis
if docker-compose exec redis redis-cli ping | grep -q PONG; then
    print_status "Redis is ready"
else
    print_error "Redis failed to start"
    exit 1
fi

# Install pre-commit hooks
echo "🔧 Setting up pre-commit hooks..."
if command -v pre-commit &> /dev/null; then
    pre-commit install
    print_status "Pre-commit hooks installed"
else
    print_warning "pre-commit not found. Install with: pip install pre-commit"
fi

# Setup complete
echo ""
echo "🎉 MemVoice development environment setup complete!"
echo ""
echo "Services running:"
echo "- Frontend: http://localhost:3000"
echo "- Backend API: http://localhost:8000"
echo "- API Documentation: http://localhost:8000/docs"
echo "- PostgreSQL: localhost:5432"
echo "- Redis: localhost:6379"
echo ""
echo "Useful commands:"
echo "- View logs: docker-compose logs -f [service]"
echo "- Stop services: docker-compose down"
echo "- Restart services: docker-compose restart [service]"
echo "- Run tests: ./scripts/test.sh"
echo ""
echo "Happy coding! 🚀"