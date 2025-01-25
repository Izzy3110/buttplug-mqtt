import json
import sys

import pygame
import asyncio
from dotenv import load_dotenv
from aiomqtt import Client
import os

if sys.platform.lower() == "win32" or os.name.lower() == "nt":
    from asyncio import set_event_loop_policy, WindowsSelectorEventLoopPolicy
    set_event_loop_policy(WindowsSelectorEventLoopPolicy())

load_dotenv('.env')

MQTT_HOST = os.getenv('MQTT_BROKER', "127.0.0.1")
MQTT_USER = os.getenv('MQTT_USER', "")
MQTT_PASS = os.getenv('MQTT_PASSWORD', "")
MQTT_TOPIC = os.getenv('MQTT_TOPIC', "plug/hush")

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


async def publish_async_set(strength_axis=.3,  topic=MQTT_TOPIC):
    print(f"mqtt-strength: {strength_axis}")
    async with Client(MQTT_HOST, username=MQTT_USER, password=MQTT_PASS) as client:
        await client.publish(topic, payload=json.dumps({"cmd": "axis", "strength": strength_axis}).encode(), qos=2)


async def increase_current_axis_value(value):
    global current_axis_value
    if current_axis_value == 0:
        current_axis_value = 0.5  # Set an initial value if it's zero

    if current_axis_value <= 1000:
        current_axis_value_ = current_axis_value
        current_axis_value_ += current_axis_value * value  # Increment by a percentage of the current value
        if current_axis_value_ > 1000:
            current_axis_value = 1000
        else:
            current_axis_value = current_axis_value_
    elif current_axis_value > 1000:
        current_axis_value = 1000

    await publish_async_set(strength_axis=current_axis_value)


async def decrease_current_axis_value(value):
    global current_axis_value
    if current_axis_value > 0:
        if current_axis_value <= 0.01:
            current_axis_value = 0

        current_axis_value_ = current_axis_value
        current_axis_value_ -= current_axis_value_ * abs(value)  # Decrement by a percentage of the current value
        current_axis_value_ = max(0, current_axis_value_)  # Ensure it doesn't go below 0

        if current_axis_value_ < 0:
            current_axis_value = 0
        else:
            current_axis_value = current_axis_value_

    if current_axis_value < 0:
        current_axis_value = 0

    await publish_async_set(strength_axis=current_axis_value)

current_axis_value = 0


async def monitor_controller(poll_interval=0.05):
    # Store previous states to detect changes
    previous_dpad = (0, 0)
    previous_axis = {}

    try:
        while True:
            pygame.event.pump()  # Process event queue

            # Get D-pad values
            dpad = joystick.get_hat(0)
            if dpad != previous_dpad:
                print(f"D-pad changed: X: {dpad[0]}, Y: {dpad[1]}")
                previous_dpad = dpad

            # Get axis values
            # for i in range(joystick.get_numaxes()):
            axis_value = joystick.get_axis(3)
            # Invert the value as per your original code
            inverted_value = -1 * axis_value

            if inverted_value > 0.15:
                await increase_current_axis_value(inverted_value)
                print(f"Increasing: {current_axis_value:.2f}")
            elif inverted_value < -0.15:
                await decrease_current_axis_value(inverted_value)
                print(f"Decreasing: {current_axis_value:.2f}")

            if 3 not in previous_axis or abs(inverted_value - previous_axis[3]) > 0.01:  # Significant change
                # print(f"Axis {3} changed: {inverted_value:.2f}")

                previous_axis[3] = inverted_value

            # Wait before polling again
            await asyncio.sleep(poll_interval)
    except asyncio.CancelledError:
        print("Controller monitoring stopped.")
    finally:
        pygame.quit()


# Run the asyncio event loop
async def main():
    task = asyncio.create_task(monitor_controller())
    try:
        await task
    except KeyboardInterrupt:
        task.cancel()
        await task

asyncio.run(main())
