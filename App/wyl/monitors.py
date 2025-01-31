import asyncio
import pygame
from wyl.mqtt import publish_async_axis_set

current_axis_value = 0
strength = 0.25  # Adjust this value to control smoothness (0.01 = very smooth, 1 = aggressive)


class ControllerMonitor:
    current_axis_value = 0
    strength = 0.25  # Adjust this value to control smoothness (0.01 = very smooth, 1 = aggressive)

    def __init__(self):
        pass

    def set_current_axis_strength(self, value):
        self.strength = value

    def set_current_axis_value(self, value):
        self.current_axis_value = value

    async def increase_current_axis_value(self, value):
        if self.current_axis_value == 0:
            self.current_axis_value = 0.5  # Set an initial value if it's zero

        if self.current_axis_value <= 1000:
            current_axis_value_ = self.current_axis_value
            current_axis_value_ += (
                                               self.current_axis_value * self.strength) * value  # Increment by a percentage of the current value
            if current_axis_value_ > 1000:
                self.current_axis_value = 1000
            else:
                self.current_axis_value = current_axis_value_
        elif self.current_axis_value > 1000:
            self.current_axis_value = 1000

        await publish_async_axis_set(strength_axis=self.current_axis_value)

    async def decrease_current_axis_value(self, value):
        if self.current_axis_value > 0:
            if self.current_axis_value <= 0.01:
                self.current_axis_value = 0

            current_axis_value_ = self.current_axis_value
            current_axis_value_ -= current_axis_value_ * (
                        self.strength * abs(value))  # Decrement by a percentage of the current value
            current_axis_value_ = max(0, current_axis_value_)  # Ensure it doesn't go below 0

            if current_axis_value_ < 0:
                self.current_axis_value = 0
            else:
                self.current_axis_value = current_axis_value_

        if self.current_axis_value < 0:
            self.current_axis_value = 0

        await publish_async_axis_set(strength_axis=self.current_axis_value)


async def increase_current_axis_value(value):
    global current_axis_value
    if current_axis_value == 0:
        current_axis_value = 0.5  # Set an initial value if it's zero

    if current_axis_value <= 1000:
        current_axis_value_ = current_axis_value
        current_axis_value_ += (current_axis_value * strength) * value  # Increment by a percentage of the current value
        if current_axis_value_ > 1000:
            current_axis_value = 1000
        else:
            current_axis_value = current_axis_value_
    elif current_axis_value > 1000:
        current_axis_value = 1000

    await publish_async_axis_set(strength_axis=current_axis_value)


async def decrease_current_axis_value(value):
    global current_axis_value
    if current_axis_value > 0:
        if current_axis_value <= 0.01:
            current_axis_value = 0

        current_axis_value_ = current_axis_value
        current_axis_value_ -= current_axis_value_ * (strength * abs(value))  # Decrement by a percentage of the current value
        current_axis_value_ = max(0, current_axis_value_)  # Ensure it doesn't go below 0

        if current_axis_value_ < 0:
            current_axis_value = 0
        else:
            current_axis_value = current_axis_value_

    if current_axis_value < 0:
        current_axis_value = 0

    await publish_async_axis_set(strength_axis=current_axis_value)

monitor_running = True


async def monitor_controller(joystick, poll_interval=0.05, inverted_set=False):
    global monitor_running
    global current_axis_value
    # Store previous states to detect changes
    previous_dpad = (0, 0)
    previous_axis = {}
    controller_monitor = ControllerMonitor()
    try:
        while monitor_running:
            try:
                pygame.event.pump()  # Process event queue
            except pygame.error as e:
                print(f"pygame error: {e.args}")
                pass


            try:
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
                if inverted_set:
                    controller_monitor.set_current_axis_value(inverted_value)

                    if inverted_value > 0.15:
                        print(inverted_value)
                        await controller_monitor.increase_current_axis_value(inverted_value)
                        print(f"Increasing: {current_axis_value:.2f}")

                    elif inverted_value < -0.35:
                        print(inverted_value)
                        await controller_monitor.decrease_current_axis_value(inverted_value)
                        print(f"Decreasing: {current_axis_value:.2f}")

                    """
                    if inverted_value > 0.15:
                        await decrease_current_axis_value(inverted_value)
                        print(f"Decreasing: {current_axis_value:.2f}")
                    elif inverted_value < -0.15:
                        await increase_current_axis_value(inverted_value)
                        print(f"Increasing: {current_axis_value:.2f}")
                    """
                else:
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
            except pygame.error as perr:
                if "not initialized" in perr.args[0]:
                    pass
                    await asyncio.sleep(3)

    except asyncio.CancelledError:
        print("Controller monitoring stopped.")
        monitor_running = False
    finally:
        pygame.quit()
        monitor_running = False
