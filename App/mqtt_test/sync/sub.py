# python 3.11
import os
import random
from dotenv import load_dotenv
import paho
from paho.mqtt import client as mqtt_client

load_dotenv('../../.env')

MQTT_HOST = os.getenv('MQTT_BROKER')
MQTT_USER = os.getenv('MQTT_USER')
MQTT_PASS = os.getenv('MQTT_PASSWORD')
MQTT_TOPIC = os.getenv('MQTT_TOPIC')
MQTT_PORT = int(os.getenv('MQTT_PORT', 1883))

client_id = f'subscribe-{random.randint(0, 100)}'


def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc, _):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(mqtt_client.CallbackAPIVersion.VERSION2, client_id=client_id, protocol=paho.mqtt.client.MQTTv5)
    # client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(MQTT_HOST, MQTT_PORT)
    return client


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

    def on_subscribe(mqttc, obj, mid, reason_code_list, flags):
        print("Subscribed: " + str(mid) + " " + str(reason_code_list[0]))
    client.subscribe(MQTT_TOPIC)
    client.on_message = on_message
    client.on_subscribe = on_subscribe


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    run()
