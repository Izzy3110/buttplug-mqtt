import asyncio
import json
import os
import sys
from aiomqtt import Client
from dotenv import load_dotenv

load_dotenv('.env')

MQTT_HOST = os.getenv('MQTT_BROKER')
MQTT_USER = os.getenv('MQTT_USER')
MQTT_PASS = os.getenv('MQTT_PASSWORD')
MQTT_TOPIC = os.getenv('MQTT_TOPIC')

if sys.platform.lower() == "win32" or os.name.lower() == "nt":
    from asyncio import set_event_loop_policy, WindowsSelectorEventLoopPolicy
    set_event_loop_policy(WindowsSelectorEventLoopPolicy())


async def publish_async(duration: float = 2, strength=.3,  topic=MQTT_TOPIC):
    async with Client(MQTT_HOST, username=MQTT_USER, password=MQTT_PASS) as client:
        await client.publish(topic, payload=json.dumps({"duration": duration, "strength": strength}).encode(), qos=2)


async def subscribe_async(client):
    await client.subscribe(os.getenv('MQTT_TOPIC'))
    async for message in client.messages:
        print(f"Received: {message.payload.decode('utf-8')}")


if __name__ == "__main__":
    # asyncio.run(publish_async(strength=.06))
    asyncio.run(publish_async(duration=.1, strength=.7))
    # asyncio.run(publish_async(duration=3, strength=.01))
