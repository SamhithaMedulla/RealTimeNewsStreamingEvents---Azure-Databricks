from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from azure.eventhub.aio import EventHubProducerClient
from azure.eventhub import EventData
import json
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# CORS middleware config

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],  # <-- explicitly allow your frontend origin
    allow_credentials=True,
    allow_methods=["*"],   # allow POST, GET, OPTIONS, etc
    allow_headers=["*"],   # allow all headers
)


EVENTHUB_CONNECTION_STR = os.getenv("EVENTHUB_CONNECTION_STR")
EVENTHUB_NAME = os.getenv("EVENTHUB_NAME")

@app.get("/")
def read_root():
    return {"message": "FastAPI is running!"}

@app.post("/send-data")
async def send_data(request: Request):
    event_data = await request.json()

    producer = EventHubProducerClient.from_connection_string(
        conn_str=EVENTHUB_CONNECTION_STR,
        eventhub_name=EVENTHUB_NAME
    )

    async with producer:
        event_batch = await producer.create_batch()
        event_batch.add(EventData(json.dumps(event_data)))
        await producer.send_batch(event_batch)

    print("✅ Sent to Event Hub:", json.dumps(event_data))
    return {"message": "Event sent successfully"}
