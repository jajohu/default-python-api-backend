# Orbital Witness Usage API

An API service to retrieve service usage over a billing period.

<!-- ## Demo
![Demo](demo.gif) -->

## Setup

### Prerequisites
- [Docker](https://docs.docker.com/engine/install/)
- [Docker Compose](https://docs.docker.com/compose/install/)
- Make (alternatively, you can run the underlying commands from the Makefile)

### Local Development

1. Build the image with development dependencies:
```bash
make build
```

2. Start the service:
```bash
make up
```
The API will be available at http://localhost:8000

### Development Commands
Run tests:
```bash
make test
```

Run linter:
```bash
make lint
```

Format code:
```bash
make format
```

Run all checks (format, lint, test):
```bash
make check
```

## API Endpoints
### GET /usage
Returns the usage data for the current billing period.
Example request:
```bash
curl http://localhost:8000/usage
```

## API Documentation
Once the service is running, view the API documentation at:
* Swagger UI: http://localhost:8000/docs
* ReDoc: http://localhost:8000/redoc

### Production Build
To build with production dependencies only:
```bash
docker build .
```


