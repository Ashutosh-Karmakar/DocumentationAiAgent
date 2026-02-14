# Documentation AI Agent

This project provides an API service for an AI agent designed to help with documentation updates.

## Setup

1.  Clone the repository.
2.  Install dependencies: `npm install` (for the Node.js part) and `pip install -r requirements.txt` (for the Python part).
3.  Set up necessary environment variables (e.g., `GEMINI_API_KEY`).

## Run

To start the Node.js server:
`npm start`

To run the Python agent (usually triggered by some event, or manually for testing):
`python doc-update-agent/src/main.py`

## Endpoints

| Endpoint      | Method | Description                               |
| :------------ | :----- | :---------------------------------------- |
| `/api/health` | GET    | Checks the health of the API service.     |
| `/api/info`   | GET    | Provides information about the API service. |
| `/api/echo`   | POST   | Echoes the request body.                  |

## Examples

### GET /api/info

```bash
curl http://localhost:3000/api/info
```

**Response:**
```json
{
  "name": "Documentation AI Agent",
  "version": "1.0.0",
  "description": "API service for documentation AI agent",
  "endpoints": ["/api/health", "/api/info", "/api/echo"]
}
```

### POST /api/echo

```bash
curl -X POST -H "Content-Type: application/json" -d '{"message": "hello", "data": 123}' http://localhost:3000/api/echo
```

**Response:**
```json
{
  "echoed": {
    "message": "hello",
    "data": 123
  },
  "receivedAt": "YYYY-MM-DDTHH:MM:SS.sssZ"
}
```
