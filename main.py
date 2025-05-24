from fastapi import FastAPI, Request
from azure.eventhub import EventHubProducerClient, EventData
import json
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

EVENTHUB_CONNECTION_STR=os.getenv("EVENTHUB_CONNECTION_STR")
EVENTHUB_NAME=os.getenv("EVENTHUB_NAME")


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

    event_batch = producer.create_batch()
    event_batch.add(EventData(json.dumps(event_data)))
    producer.send_batch(event_batch)
    producer.close()

    return {"message": "Event sent successfully"}



