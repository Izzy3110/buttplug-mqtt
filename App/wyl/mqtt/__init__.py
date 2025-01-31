import json
import os
import time

from aiomqtt import Client
from dotenv import load_dotenv

from control_panel.app.extensions.socketio import socketio

load_dotenv('.env')


MQTT_HOST = os.getenv('MQTT_BROKER', "127.0.0.1")
MQTT_USER = os.getenv('MQTT_USER', "")
MQTT_PASS = os.getenv('MQTT_PASSWORD', "")
MQTT_TOPIC = os.getenv('MQTT_TOPIC', "plug/hush")

from wyl import logger


async def subscribe_async(mqtt_client, mqtt_topic=None, queue=None, debug=True):
    """
    Subscribes to the MQTT topic and processes incoming messages.
    Args:
        mqtt_client: The MQTT client instance.

    Listens for messages on the configured MQTT topic, decodes the JSON payload,
    and enqueues vibration commands for processing.
    :param queue:
    :param mqtt_topic:
    :param mqtt_client:
    :param debug:
    """

    await mqtt_client.subscribe(mqtt_topic)
    async for message in mqtt_client.messages:
        if debug:
            print(f"Received: {message.payload.decode()}")
        try:
            json_: dict = json.loads(message.payload.decode('utf-8'))
            is_set_cmd = False
            is_axis_cmd = False

            duration = .1

            if "cmd" in json_.keys():
                is_set_cmd = True
                if json_.get('cmd') == "axis":
                    is_axis_cmd = True
            else:
                try:
                    duration = float(json_.get('duration'))
                except TypeError:
                    is_set_cmd = True
                    pass
            strength = float(json_.get('strength'))
            if not is_axis_cmd:
                # print("OK" if is_set_cmd else "NOT A SET-CMD")
                if not is_set_cmd:
                    print(f"cmd:yes a:no  s:{strength}")
                    await queue.put(json.dumps({"duration": duration, "strength": strength, "t": time.time()}))
                else:
                    print(f"cmd:no  a:no  s:{strength}")
                    await queue.put(json.dumps({"duration": "-1", "strength": strength, "t": time.time()}))
            else:
                # print("axis cmd")
                print(f"cmd:yes a:yes s:{strength}")
                strength /= 1000
                socketio.emit("mouse_move_point", {
                    "value": strength,
                    "duration": "-1"
                })
                await queue.put(json.dumps({"duration": "-1", "strength": strength, "t": time.time()}))
        except json.decoder.JSONDecodeError as de:
            print(de)
            print(f"m: {message.payload.decode('utf-8')}")


async def on_subscribe(client, userdata, mid, granted_qos):
    """Callback function when a subscription is successful."""
    logger.debug(f"Subscription successful. Message ID: {mid}, QoS: {granted_qos}")


async def on_message(client, userdata, msg):
    logger.debug(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")


async def publish_async_set(strength=.3,  topic=MQTT_TOPIC):
    print(f"mqtt-strength: {strength}")
    async with Client(MQTT_HOST, username=MQTT_USER, password=MQTT_PASS) as client:
        await client.publish(topic, payload=json.dumps({"cmd": "set", "strength": strength}).encode(), qos=2)


async def publish_async_axis_set(strength_axis=.3,  topic=MQTT_TOPIC):
    print(f"mqtt-strength: {strength_axis}")
    async with Client(MQTT_HOST, username=MQTT_USER, password=MQTT_PASS) as client:
        await client.publish(topic, payload=json.dumps({"cmd": "axis", "strength": strength_axis}).encode(), qos=2)
