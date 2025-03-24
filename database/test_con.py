import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv

load_dotenv()

async def ping_server():
    # Get the MongoDB URI from environment variables
    uri = os.getenv('uri')
    print(uri)
    if not uri:
        print("Error: MongoDB URI not found in environment variables")
        return

    # Set the Stable API version when creating a new client
    client = AsyncIOMotorClient(uri, server_api=ServerApi('1'))

    # Send a ping to confirm a successful connection
    try:
        await client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(f"Failed to connect to MongoDB: {str(e)}")
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(ping_server())