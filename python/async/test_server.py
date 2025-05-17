import asyncio
import socket

# Simple TCP Server to test our FastAPI service
async def handle_client(reader, writer):
    print("Client connected")
    
    while True:
        try:
            # Read message ID (first byte)
            msg_id = await reader.readexactly(1)
            if not msg_id:
                continue
                
            # Read data until "END"
            data = b""
            while True:
                chunk = await reader.readline()
                if not chunk:
                    break
                if chunk.strip() == b"END":
                    break
                data += chunk
                
            if not data:
                continue
                
            message = data.decode().strip()
            print(f"Received message: {message}")
            
            # Send response with same ID
            response = f"Processed: {message}"
            writer.write(msg_id)
            writer.write(response.encode())
            writer.write(b"\nEND\n")
            await writer.drain()
            
        except (ConnectionResetError, asyncio.IncompleteReadError):
            break
    
    writer.close()
    await writer.wait_closed()
    print("Client disconnected")

async def main():
    server = await asyncio.start_server(
        handle_client, '127.0.0.1', 9000
    )
    
    addr = server.sockets[0].getsockname()
    print(f'Serving on {addr}')
    
    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Server stopped")