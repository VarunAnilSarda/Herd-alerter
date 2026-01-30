from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import asyncio
from kafka import KafkaConsumer

app = FastAPI()

# Allow frontend origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

clients = []

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)
    try:
        while True:
            await asyncio.sleep(1)
    except:
        clients.remove(websocket)

async def kafka_listener():
    consumer = KafkaConsumer(
        "test-topic",
        bootstrap_servers=["localhost:9092"],
        auto_offset_reset="earliest",
        group_id="dashboard",
        value_deserializer=lambda x: x.decode("utf-8")
    )
    for message in consumer:
        for client in clients:
            await client.send_text(message.value)

if __name__ == "__main__":
    import uvicorn
    loop = asyncio.get_event_loop()
    loop.create_task(kafka_listener())
    uvicorn.run(app, host="0.0.0.0", port=8000)
