import asyncio
import aiohttp
import sys

async def test_api():
    async with aiohttp.ClientSession() as session:
        try:
            # Send a message through the FastAPI endpoint
            message = "Hello, World!" if len(sys.argv) < 2 else sys.argv[1]
            print(f"Sending message: {message}")
            
            async with session.post(
                "http://localhost:8000/send-message",
                json={"message": message}
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    print(f"Response from server: {result['response']}")
                else:
                    error = await response.text()
                    print(f"Error: {response.status} - {error}")
                    
        except aiohttp.ClientError as e:
            print(f"Client error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

if __name__ == "__main__":
    asyncio.run(test_api())
