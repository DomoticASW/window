from enum import Enum
import time

class InvalidOperationError(Exception):
    """Exception raised for invalid operations on the washing machine."""
    pass

class WindowPosition(str, Enum):
    CLOSED = "Closed"
    TILTED = "Tilted"
    OPEN = "Open"

class WindowState(str, Enum):
    IDLE = "Idle"
    MOVING = "Moving"

class SmartWindow:
    def __init__(self, id: str, name: str):
        self.id = id
        self.name = name
        self.angle = 0.0  # degrees, 0 = closed, 90 = fully open
        self.state = WindowState.IDLE
        self.position = WindowPosition.CLOSED

    def _simulate_motion(self, target_angle, duration):
        if self.state == WindowState.MOVING:
            raise InvalidOperationError("The window is already moving.")
        self.state = WindowState.MOVING
        
        steps = 10
        step_duration = duration / steps
        angle_step = (target_angle - self.angle) / steps
        
        for _ in range(steps):
            self.angle += angle_step
            time.sleep(step_duration)
        
        self.angle = target_angle  # Ensure exact target at the end
        self.state = WindowState.IDLE

    def open(self):
        if self.position == WindowPosition.OPEN:
            raise InvalidOperationError("The window is already open.")
        self._simulate_motion(90.0, 3)
        self.position = WindowPosition.OPEN

    def tilt(self, angle: float):
        if self.position == WindowPosition.TILTED and self.angle == angle:
            raise InvalidOperationError("The window is already tilted.")
        self._simulate_motion(angle, 2)
        self.position = WindowPosition.TILTED

    def close(self):
        if self.position == WindowPosition.CLOSED:
            raise InvalidOperationError("The window is already closed.")
        self._simulate_motion(0.0, 3)
        self.position = WindowPosition.CLOSED

    def status(self):
        status_string = f"Angle: {self.angle:.1f}° | State: {self.state.value}"
        print(status_string)
        return status_string
