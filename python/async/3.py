import socket
import asyncio
import uuid
from typing import Dict, Optional, Tuple
from fastapi import FastAPI, HTTPException
import uvicorn
from pydantic import BaseModel

# TCP Client for socket communication
class TCPClient:
    def __init__(self, host: str = "localhost", port: int = 9000):
        self.host = host
        self.port = port
        self.reader: Optional[asyncio.StreamReader] = None
        self.writer: Optional[asyncio.StreamWriter] = None
        self.pending_requests: Dict[bytes, asyncio.Future] = {}
        self.connected = False
        
    async def connect(self):
        if self.connected:
            return
            
        try:
            self.reader, self.writer = await asyncio.open_connection(
                self.host, self.port
            )
            self.connected = True
            
            # Start listening for responses
            asyncio.create_task(self._listen_for_responses())
        except (ConnectionRefusedError, OSError) as e:
            raise ConnectionError(f"Failed to connect to {self.host}:{self.port} - {str(e)}")
        
    async def _listen_for_responses(self):
        try:
            while self.connected:
                # Read message ID (first byte)
                msg_id = await self.reader.readexactly(1)
                if not msg_id:
                    continue
                    
                # Read data until "END"
                data = b""
                while True:
                    chunk = await self.reader.readline()
                    if chunk.strip() == b"END":
                        break
                    data += chunk
                
                # Resolve the future if we have a pending request with this ID
                if msg_id in self.pending_requests:
                    future = self.pending_requests.pop(msg_id)
                    future.set_result(data.decode().strip())
                    
        except (ConnectionResetError, asyncio.IncompleteReadError, ConnectionError):
            self.connected = False
            # Cancel all pending requests
            for future in self.pending_requests.values():
                if not future.done():
                    future.set_exception(ConnectionError("Connection lost"))
            
    async def send_message(self, message: str, timeout: float = 10.0) -> str:
        if not self.connected:
            await self.connect()
            
        # Create a unique message ID (1 byte)
        msg_id = bytes([len(self.pending_requests) % 256])
        
        # Create a future to wait for the response
        future = asyncio.Future()
        self.pending_requests[msg_id] = future
        
        # Send the message: ID + message + END
        self.writer.write(msg_id)
        self.writer.write(message.encode())
        self.writer.write(b"\nEND\n")
        await self.writer.drain()
        
        try:
            # Wait for the response with timeout
            return await asyncio.wait_for(future, timeout)
        except asyncio.TimeoutError:
            self.pending_requests.pop(msg_id, None)
            raise TimeoutError(f"Request timed out after {timeout} seconds")
        
    async def close(self):
        if self.writer:
            self.writer.close()
            await self.writer.wait_closed()
        self.connected = False
        
        # Cancel all pending requests
        for future in self.pending_requests.values():
            if not future.done():
                future.set_exception(ConnectionError("Connection closed"))
        self.pending_requests.clear()

# FastAPI Application
app = FastAPI(title="Socket Message Proxy API")

# TCP Client singleton
tcp_client = TCPClient()

# Request model
class MessageRequest(BaseModel):
    message: str
    timeout: float = 10.0

# Response model
class MessageResponse(BaseModel):
    response: str

@app.post("/send-message", response_model=MessageResponse)
async def send_message(request: MessageRequest):
    try:
        response = await tcp_client.send_message(request.message, request.timeout)
        return MessageResponse(response=response)
    except TimeoutError:
        raise HTTPException(status_code=504, detail="Request to socket server timed out")
    except ConnectionError as e:
        raise HTTPException(status_code=503, detail=str(e))

@app.on_event("startup")
async def startup_event():
    try:
        await tcp_client.connect()
    except ConnectionError:
        # We'll retry connection when the first request comes in
        pass

@app.on_event("shutdown")
async def shutdown_event():
    await tcp_client.close()

# Run the server
if __name__ == "__main__":
    uvicorn.run("3:app", host="0.0.0.0", port=8000, reload=True)