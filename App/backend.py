import asyncio
import json
import os
import buttplug
import sys
from asyncio import Queue
from aiomqtt import Client
from dotenv import load_dotenv
from wyl.buttplug import client_setup, vibrate
from wyl.mqtt import subscribe_async
from wyl import logger

load_dotenv('.env')

MQTT_HOST = os.getenv('MQTT_BROKER', "5.230.42.8")
MQTT_USER = os.getenv('MQTT_USER', "")
MQTT_PASS = os.getenv('MQTT_PASSWORD', "")
MQTT_TOPIC = os.getenv('MQTT_TOPIC', "plug/hush")

INTIFACE_ENGINE_CLIENT_NAME = os.getenv('INTIFACE_ENGINE_CLIENT_NAME', "Python-App")
INTIFACE_ENGINE_WS_URL = os.getenv('INTIFACE_ENGINE_WS_URL', "ws://localhost:15345")

client = buttplug.client.Client(INTIFACE_ENGINE_CLIENT_NAME)
connector = buttplug.connectors.WebsocketConnector(INTIFACE_ENGINE_WS_URL)

if sys.platform.lower() == "win32" or os.name.lower() == "nt":
    from asyncio import set_event_loop_policy, WindowsSelectorEventLoopPolicy

    set_event_loop_policy(WindowsSelectorEventLoopPolicy())

queue = Queue()

q_processing = False
buttplug_client = None
async_debug = True
silenced = True


async def process_q(q: asyncio.Queue):
    """
    Processes the items in the queue by sending vibration commands to connected devices.

    Args:
        q (asyncio.Queue): The queue containing vibration command items.
    """
    global q_processing, buttplug_client

    q_processing = True

    try:
        if q.qsize() > 0:
            if buttplug_client is not None:
                if buttplug_client.connected:
                    if len(buttplug_client.devices) > 0:
                        while q.qsize() > 0:
                            item = await q.get()

                            json_ = json.loads(item)
                            duration = float(json_.get('duration'))
                            strength = float(json_.get('strength'))

                            await vibrate(
                                buttplug_client=buttplug_client,
                                duration=duration, strength=strength
                            )
                    else:
                        logger.debug(f"{q.qsize()} items in q")

                        await buttplug_client.start_scanning()
                        await asyncio.sleep(3)
                        try:
                            await buttplug_client.stop_scanning()

                        except TypeError as e:
                            logger.error(e.args)
                        except buttplug.errors.client.DisconnectedError as e:
                            logger.error(f"buttplug.errors.client.DisconnectedError: {e.message}")

                        print(buttplug_client.devices)

                else:
                    logger.debug("waiting for client")
                    try:
                        await buttplug_client.connect(connector=connector)
                    except buttplug.errors.client.ServerNotFoundError as e:
                        logger.error(f"buttplug.errors.client.ServerNotFoundError: {e.message}")

            else:
                try:
                    buttplug_client = await client_setup(buttplug_client=client, connector=connector)
                except Exception as e:
                    print(str(e))

    finally:
        q_processing = False


async def monitor_queue():
    """
    Monitors the queue and starts `process_q` when not already processing.

    Continuously checks if there are items in the queue and ensures the processing
    function `process_q` is initiated if not already running.
    """
    global q_processing
    while True:
        if not q_processing and not queue.empty():
            asyncio.create_task(process_q(queue))
        await asyncio.sleep(0.1)  # Adjust polling interval as needed


async def main():
    """
    Initializes the MQTT client, starts the subscription and queue monitoring
    tasks, and manages application shutdown.
    """

    async with Client(MQTT_HOST, username=MQTT_USER, password=MQTT_PASS) as mqtt_client:
        logger.debug("starting tasks...")
        logger.debug("  subscribe_async")
        logger.debug("  monitor_queue")
        logger.debug("")

        tasks = [
            asyncio.create_task(subscribe_async(mqtt_client, mqtt_topic=MQTT_TOPIC, queue=queue)),
            asyncio.create_task(monitor_queue())
        ]

        try:
            await asyncio.gather(*tasks)
        except asyncio.CancelledError:
            logger.debug("Shutting down...")


if __name__ == "__main__":
    config = {
        "program": "Buttplug MQTT Bridge",
        "version": "0.1"
    }

    logger.debug(f"Program: {config.get('program')}")
    logger.debug(f"Version: {config.get('version')}")
    logger.debug(f"Debug: {'On' if async_debug else 'Off'}")
    logger.debug("")

    asyncio.run(main(), debug=async_debug)
