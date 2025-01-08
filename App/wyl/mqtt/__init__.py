import json
import time

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
            json_ = json.loads(message.payload.decode('utf-8'))
            duration = float(json_.get('duration'))
            strength = float(json_.get('strength'))
            await queue.put(json.dumps({"duration": duration, "strength": strength, "t": time.time()}))
        except json.decoder.JSONDecodeError as de:
            print(de)
            print(f"m: {message.payload.decode('utf-8')}")


async def on_subscribe(client, userdata, mid, granted_qos):
    """Callback function when a subscription is successful."""
    logger.debug(f"Subscription successful. Message ID: {mid}, QoS: {granted_qos}")


async def on_message(client, userdata, msg):
    logger.debug(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
