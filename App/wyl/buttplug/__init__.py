import asyncio
import logging
import time
from datetime import datetime

import buttplug
from buttplug.client import Actuator


async def client_setup(buttplug_client, connector) -> buttplug.client.client.Client|None:
    try:
        await buttplug_client.connect(connector)
        buttplug_client: buttplug.client.client.Client = buttplug_client
        if buttplug_client.connected:
            return buttplug_client
    except buttplug.connectors.websocket.ConnectorError as e:
        logging.error("Could not connect to server, exiting: {}".format(e.message))
    return


async def vibrate(buttplug_client, duration, strength=0.2, disconnect=False):
    # print("< vibrate")
    if buttplug_client is not None:
        start_ = datetime.now()
        start_t = time.time()
        no_devices = False
        if len(buttplug_client.devices) == 0:
            logging.error("no devices found")
            await buttplug_client.start_scanning()
            no_devices = True
        else:
            # print(f"strength: {strength}")
            last_actuator = None
            while (time.time() - start_t) < duration:
                # print((time.time() - start_t))
                for device_index, device_name in buttplug_client.devices.items():
                    device: buttplug.client.client.Device = buttplug_client.devices[device_index]
                    for actuator in device.actuators:
                        current_actuator: Actuator = actuator
                        await current_actuator.command(strength)
                        last_actuator = current_actuator
            if last_actuator is not None:
                await last_actuator.command(0)
            end_ = datetime.now()
            # print(start_.strftime("%d.%m.%Y %H:%M:%S"))
            # print(end_.strftime("%d.%m.%Y %H:%M:%S"))
            # print(end_ - start_)
            # print("done")
        if no_devices:
            await buttplug_client.stop_scanning()
            no_devices = False
        if disconnect:
            await buttplug_client.disconnect()
            logging.info("Disconnected, quitting")
            await asyncio.sleep(.0)
    else:
        logging.error("Client is None")
