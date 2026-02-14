# Documentation AI Agent API

This API service provides various endpoints for interacting with the Documentation AI Agent.

## Setup

To set up the project, follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone [repository_url]
    cd [repository_directory]
    ```
2.  **Install dependencies:**
    ```bash
    npm install
    ```

## How to Run

To run the API service, execute the following command:

```bash
npm start
```

The server will start on `http://localhost:3000`.

## Endpoints

The following endpoints are available:

| Endpoint      | Method | Description                                    | Example Response                                      |
| :------------ | :----- | :--------------------------------------------- | :---------------------------------------------------- |
| `/api/health` | `GET`  | Checks the health status of the API.           | `{"status": "ok"}`                                    |
| `/api/info`   | `GET`  | Provides information about the API service.    | `{"name": "Documentation AI Agent", "version": "1.0.0", "description": "API service for documentation AI agent", "endpoints": ["/api/health", "/api/info", "/api/echo", "/api/time"]}` |
| `/api/echo`   | `POST` | Echos back the JSON payload sent in the request body. | Request: `{"message": "hello"}` <br> Response: `{"received": {"message": "hello"}}` |
| `/api/time`   | `GET`  | Returns the current server time in ISO and epoch formats. | `{"iso": "2023-10-27T10:00:00.000Z", "epoch": 1678886400}` |