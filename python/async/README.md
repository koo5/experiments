# FastAPI Socket Message Proxy

This project demonstrates a FastAPI service that forwards messages to a TCP socket server and returns the responses.

## Files

- `3.py`: Main FastAPI application with TCP client implementation
- `test_server.py`: A simple TCP server for testing
- `test_client.py`: A test client that sends requests to the FastAPI service

## How It Works

1. The FastAPI service exposes a POST endpoint at `/send-message`
2. When a message is received, it forwards it to a TCP socket server
3. Messages on the TCP socket are identified by an ID in the first byte, followed by the message, and ending with "END"
4. Responses from the TCP server follow the same format
5. The FastAPI service maintains a connection pool to the TCP server and handles request/response matching

## Usage

1. Start the TCP server:
```
python test_server.py
```

2. Start the FastAPI service:
```
python 3.py
```

3. Send a test message:
```
python test_client.py "Your message here"
```

## Requirements

- FastAPI
- Uvicorn
- Pydantic
- aiohttp (for test client)