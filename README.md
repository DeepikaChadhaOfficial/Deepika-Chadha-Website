# EPS Proxy Service

A FastAPI-based proxy service for the EPS tracking API.

## Project Structure

```
eps-proxy/
├── main.py                          # Application entry point
├── requirements.txt                 # Python dependencies
├── .env.example                     # Environment variables template
├── .env                            # Your environment variables (not in git)
└── app/
    ├── __init__.py
    ├── core/                       # Core configuration
    │   ├── __init__.py
    │   ├── config.py              # Settings management
    │   └── logging_config.py      # Logging setup
    ├── middleware/                 # Middleware components
    │   ├── __init__.py
    │   ├── cors.py                # CORS configuration
    │   └── error_handler.py       # Global error handling
    ├── api/                        # API layer
    │   ├── __init__.py
    │   └── routes/
    │       ├── __init__.py
    │       └── tracking.py        # Tracking endpoints
    └── services/                   # Business logic
        ├── __init__.py
        └── eps_service.py         # EPS API integration
```

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your actual credentials
   ```

3. **Run the application:**
   ```bash
   uvicorn main:app --reload
   ```

   Or for production:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```

## API Endpoints

### Health Check
- `GET /` - Basic health check
- `GET /health` - Detailed health check

### Tracking
- `GET /track/{awb}` - Get tracking information for an AWB number

**Example:**
```bash
curl http://localhost:8000/track/AWB123456789
```

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| TOKEN | EPS API token | Yes |
| USER_ID | EPS user ID | Yes |
| PASSWORD | EPS password | Yes |
| LOG_LEVEL | Logging level (INFO, DEBUG, etc.) | No |
| REQUEST_TIMEOUT | API request timeout in seconds | No |

## Features

- ✅ Clean, modular architecture
- ✅ Separation of concerns (routes, services, config)
- ✅ Type hints throughout
- ✅ Comprehensive error handling
- ✅ CORS support
- ✅ Environment-based configuration
- ✅ Health check endpoints
- ✅ Structured logging

## Development

To add a new endpoint:

1. Create a new route in `app/api/routes/`
2. Add business logic in `app/services/`
3. Register the router in `main.py`

## License

Proprietary
