# main.py

from fastapi import FastAPI, Request
from azure.eventhub import EventHubProducerClient, EventData
from dotenv import load_dotenv
import os
import json

# ✅ Load secrets from .env file
load_dotenv()

# ✅ Read from environment variables
EVENTHUB_CONNECTION_STR = os.getenv("EVENTHUB_CONNECTION_STR")
EVENTHUB_NAME = os.getenv("EVENTHUB_NAME")

# ✅ Create FastAPI app
app = FastAPI()

# ✅ Define POST endpoint to receive GTM event data
@app.post("/send-data")
async def send_data(request: Request):
    # Get the data sent from GTM
    event_data = await request.json()
    print("Received:", event_data)

    # Create Event Hub client
    producer = EventHubProducerClient.from_connection_string(
        conn_str=EVENTHUB_CONNECTION_STR,
        eventhub_name=EVENTHUB_NAME
    )

    # Create a batch and add event data to it
    event_batch = await producer.create_batch()
    event_batch.add(EventData(json.dumps(event_data)))

    # Send batch to Event Hubs
    await producer.send_batch(event_batch)
    await producer.close()

    return {"status": "sent"}


