import asyncio
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


async def on_subscribe(client, userdata, mid, granted_qos):
    """Callback function when a subscription is successful."""
    print(f"Subscription successful. Message ID: {mid}, QoS: {granted_qos}")


async def subscribe_async():
    async with Client(MQTT_HOST, username=MQTT_USER, password=MQTT_PASS) as client:
        client.on_subscribe = on_subscribe
        print(f"Topic: {MQTT_TOPIC}")
        await client.subscribe(MQTT_TOPIC, qos=1)
        async for message in client.messages:
            print(f"Received: {message.payload.decode()}")


if __name__ == "__main__":
    try:
        asyncio.run(subscribe_async())
    except KeyboardInterrupt:
        print("Interrupted with CTRL+C ... exiting... ")
        sys.exit(0)
