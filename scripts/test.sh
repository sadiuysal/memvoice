#!/bin/bash

# MemVoice Test Runner Script
# This script runs all tests for the project

set -e

echo "🧪 Running MemVoice Test Suite..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Parse command line arguments
BACKEND_ONLY=false
FRONTEND_ONLY=false
COVERAGE=false
E2E=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --backend)
            BACKEND_ONLY=true
            shift
            ;;
        --frontend)
            FRONTEND_ONLY=true
            shift
            ;;
        --coverage)
            COVERAGE=true
            shift
            ;;
        --e2e)
            E2E=true
            shift
            ;;
        --help)
            echo "Usage: $0 [options]"
            echo "Options:"
            echo "  --backend     Run only backend tests"
            echo "  --frontend    Run only frontend tests"
            echo "  --coverage    Run tests with coverage report"
            echo "  --e2e         Run end-to-end tests"
            echo "  --help        Show this help message"
            exit 0
            ;;
        *)
            print_error "Unknown option: $1"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

# Ensure services are running
print_info "Checking if services are running..."
if ! docker-compose ps | grep -q "Up"; then
    print_warning "Services not running. Starting them..."
    docker-compose up -d
    sleep 10
fi

# Backend tests
if [[ "$FRONTEND_ONLY" == "false" ]]; then
    print_info "Running backend tests..."
    
    if [[ "$COVERAGE" == "true" ]]; then
        print_info "Running backend tests with coverage..."
        docker-compose exec backend pytest --cov=src --cov-report=html --cov-report=term-missing
        print_status "Backend coverage report generated in backend/htmlcov/"
    else
        docker-compose exec backend pytest -v
    fi
    
    print_status "Backend tests completed"
fi

# Frontend tests
if [[ "$BACKEND_ONLY" == "false" ]]; then
    print_info "Running frontend tests..."
    
    if [[ "$COVERAGE" == "true" ]]; then
        print_info "Running frontend tests with coverage..."
        docker-compose exec frontend npm run test:coverage
        print_status "Frontend coverage report generated in frontend/coverage/"
    else
        docker-compose exec frontend npm test -- --watchAll=false
    fi
    
    print_status "Frontend tests completed"
fi

# End-to-end tests
if [[ "$E2E" == "true" ]]; then
    print_info "Running end-to-end tests..."
    
    # Wait for services to be fully ready
    sleep 5
    
    # Run E2E tests
    docker-compose exec frontend npm run test:e2e
    
    print_status "End-to-end tests completed"
fi

# Code quality checks
if [[ "$BACKEND_ONLY" == "false" && "$FRONTEND_ONLY" == "false" ]]; then
    print_info "Running code quality checks..."
    
    # Backend linting
    print_info "Checking backend code quality..."
    docker-compose exec backend black --check .
    docker-compose exec backend isort --check-only .
    docker-compose exec backend flake8 .
    docker-compose exec backend mypy src/
    docker-compose exec backend bandit -r . -x tests/
    
    # Frontend linting
    print_info "Checking frontend code quality..."
    docker-compose exec frontend npm run lint
    docker-compose exec frontend npm run type-check
    docker-compose exec frontend npm run format:check
    
    print_status "Code quality checks passed"
fi

echo ""
print_status "All tests completed successfully! 🎉"

# Summary
echo ""
echo "📊 Test Summary:"
if [[ "$BACKEND_ONLY" == "false" ]]; then
    echo "✅ Backend tests: PASSED"
fi
if [[ "$FRONTEND_ONLY" == "false" ]]; then
    echo "✅ Frontend tests: PASSED"
fi
if [[ "$E2E" == "true" ]]; then
    echo "✅ E2E tests: PASSED"
fi
if [[ "$COVERAGE" == "true" ]]; then
    echo "📈 Coverage reports generated"
fi
echo ""