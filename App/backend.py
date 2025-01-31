import asyncio
import json
import os
import threading
import aiomqtt.exceptions
import buttplug
import sys
from asyncio import Queue
import pygame
from aiomqtt import Client
from dotenv import load_dotenv
from flask_socketio import emit, Namespace

from wyl.monitors import monitor_controller
from wyl.buttplug import client_setup, vibrate, vibrate_set
from wyl.mqtt import subscribe_async, publish_async_set
from wyl import logger

from control_panel.control_panel import app, socketio

load_dotenv('.env')

# Initialize pygame
pygame.init()
pygame.joystick.init()

# Check for connected joysticks
joystick_count = pygame.joystick.get_count()
if joystick_count == 0:
    print("No joystick connected!")
    exit()
else:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    print(f"Connected to: {joystick.get_name()}")

MQTT_HOST = os.getenv('MQTT_BROKER', "127.0.0.1")
MQTT_USER = os.getenv('MQTT_USER', "")
MQTT_PASS = os.getenv('MQTT_PASSWORD', "")
MQTT_TOPIC = os.getenv('MQTT_TOPIC', "plug/hush")

INTIFACE_ENGINE_CLIENT_NAME = os.getenv('INTIFACE_ENGINE_CLIENT_NAME', "Python-App")
INTIFACE_ENGINE_WS_URL = os.getenv('INTIFACE_ENGINE_WS_URL', "ws://localhost:12345")

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
mqtt_connected = False
current_axis_value = 0
inverted_set = True


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

                            json_: dict = json.loads(item)
                            # print("JSON")
                            # print(json_)
                            duration = float(json_.get('duration'))
                            strength = float(json_.get('strength'))
                            if json_.get('duration') != "-1":
                                print("default")
                                # print(json_)
                                await vibrate(
                                    buttplug_client=buttplug_client,
                                    duration=duration, strength=strength
                                )
                            else:
                                print("SET")
                                print(json_)

                                await vibrate_set(
                                    buttplug_client=buttplug_client,
                                    strength=strength
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
                    print(type(e))

    finally:
        q_processing = False


q_can_process = True


async def monitor_queue():
    """
    Monitors the queue and starts `process_q` when not already processing.

    Continuously checks if there are items in the queue and ensures the processing
    function `process_q` is initiated if not already running.
    """
    global q_processing, q_can_process
    try:
        while q_can_process:
            if not q_processing and not queue.empty():
                asyncio.create_task(process_q(queue))
            await asyncio.sleep(0.1)  # Adjust polling interval as needed
    except asyncio.CancelledError:
        q_can_process = False


async def main():
    global mqtt_connected, q_can_process
    """
    Initializes the MQTT client, starts the subscription and queue monitoring
    tasks, and manages application shutdown.
    """

    while not mqtt_connected:
        try:
            async with Client(MQTT_HOST, username=MQTT_USER, password=MQTT_PASS) as mqtt_client:
                logger.debug("starting tasks...")
                logger.debug("  subscribe_async")
                logger.debug("  monitor_queue")
                logger.debug("")

                tasks = [
                    asyncio.create_task(subscribe_async(mqtt_client, mqtt_topic=MQTT_TOPIC, queue=queue)),
                    asyncio.create_task(monitor_queue()),
                    asyncio.create_task(monitor_controller(joystick=joystick))
                ]
                mqtt_connected = True
                try:
                    await asyncio.gather(*tasks)
                except asyncio.CancelledError:
                    logger.debug("Shutting down...")
                    mqtt_connected = False
                    q_can_process = False
                    await asyncio.sleep(5)
        except aiomqtt.exceptions.MqttError as mqtt_error:
            mqtt_error_str = mqtt_error.args[0]
            logger.error(f"MQTT-Error: {mqtt_error_str}")
            mqtt_connected = False
            await asyncio.sleep(5)


class MyCustomNamespace(Namespace):
    last_data = None

    def on_connect(self):
        pass

    def on_system(self, data):
        if data.get("reconnected"):
            print("has reconnected")

    def on_disconnect(self, reason):
        pass

    def on_mouse_move_point(self, data):
        if self.should_process_data(data):
            self.last_data = data
            print(data)
            print(data.get('y%'))
            emit('mouse_coordinates', data, broadcast=True)
            self.process_last_data()

    def on_external_set(self, data):
        emit("my_set_event", data.get('value'), broadcast=True)

    def on_mouse_create_point(self, data):
        if self.should_process_data(data):
            self.last_data: dict = data

            print(self.last_data.get('y%'))
            emit('mouse_coordinates', data, broadcast=True)
            self.process_last_data()

    def should_process_data(self, data):
        """
        Function to filter out unwanted values.
        Assumption: The incorrect value (e.g., 0.83) always comes before the real one.
        """
        y_value = data.get('y%')
        print(f"should_process_data: {y_value}")
        # If y_value is None or invalid, return False
        if y_value is None:
            return False
        return True

    def process_last_data(self):
        print("processing...")
        loop = asyncio.new_event_loop()
        from asyncio import set_event_loop_policy, WindowsSelectorEventLoopPolicy
        set_event_loop_policy(WindowsSelectorEventLoopPolicy())
        loop.run_until_complete(publish_async_set(strength=(self.last_data.get('y%') / 100)))


def run_flask():
    socketio.on_namespace(MyCustomNamespace('/'))
    socketio.run(app, port=5005, allow_unsafe_werkzeug=True)


if __name__ == "__main__":
    config = {
        "program": "Buttplug MQTT Bridge",
        "version": "0.1"
    }

    logger.debug(f"Program: {config.get('program')}")
    logger.debug(f"Version: {config.get('version')}")
    logger.debug(f"Debug: {'On' if async_debug else 'Off'}")
    logger.debug("")

    # Start the Flask app in a separate thread
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()

    asyncio.run(main(), debug=async_debug)
