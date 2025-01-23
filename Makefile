.PHONY: build up down test lint format clean

# Docker commands
build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down

# Development commands
test:
	docker-compose exec api python -m pytest

lint:
	docker-compose exec api python -m pylint app/

format:
	docker-compose exec api python -m black .

# Run all checks
check: format lint test

# Help command
help:
	@echo "Available commands:"
	@echo "  make build    - Build Docker images"
	@echo "  make up       - Start Docker containers in detached mode"
	@echo "  make down     - Stop Docker containers"
	@echo "  make test     - Run tests using pytest"
	@echo "  make lint     - Run pylint"
	@echo "  make format   - Run black formatter"
	@echo "  make check    - Run formatter, linter, and tests"