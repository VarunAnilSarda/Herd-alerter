import asyncio
import websockets
import json
import random
from datetime import datetime, timedelta

fields = ["North Field", "South Field", "East Field", "West Field"]
alert_types = ["Movement", "Behavior", "Fence Breach", "Missing"]
health_statuses = ["Good", "Warning", "Critical"]

def generate_event():
    return {
        "timestamp": (datetime.now() - timedelta(minutes=random.randint(0, 120))).strftime("%H:%M:%S"),
        "field": random.choice(fields),
        "alert_type": random.choice(alert_types),
        "cow_id": random.randint(100, 120),
        "health_status": random.choice(health_statuses)
    }

async def send_events(websocket, path):
    while True:
        event = generate_event()
        await websocket.send(json.dumps(event))
        await asyncio.sleep(2)  # send every 2 seconds

async def main():
    async with websockets.serve(send_events, "localhost", 6789):
        print("WebSocket server running on ws://localhost:6789")
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())
