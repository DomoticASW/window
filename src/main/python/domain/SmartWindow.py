from enum import Enum
from threading import Thread
from pydantic import BaseModel
import time

class InvalidOperationError(Exception):
    """Invalid operations on the smart window."""
    pass

class InvalidAngleError(Exception):
    """Angle not provided or out of range."""
    pass

class WindowPosition(str, Enum):
    CLOSED = "Closed"
    TILTED = "Tilted"
    OPEN = "Open"

class WindowState(str, Enum):
    IDLE = "Idle"
    MOVING = "Moving"

class WindowStatus(BaseModel):
    angle: int
    state: WindowState
    position: WindowPosition
    model_config = {
        "frozen": True
    }

class SmartWindow:
    def __init__(self, id: str, name: str):
        self.id = id
        self.name = name
        self.angle = 0  # degrees, 0 = closed, 90 = fully open
        self.state = WindowState.IDLE
        self.position = WindowPosition.CLOSED

    def _run_tilt_motion(self, angle: int, position: WindowPosition):
        self._simulate_motion(angle, 10)
        self.position = position

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
        
        self.angle = int(target_angle)  # Ensure exact target at the end
        self.state = WindowState.IDLE

    def open(self):
        if self.position == WindowPosition.OPEN:
            raise InvalidOperationError("The window is already open.")
        Thread(target=self._run_tilt_motion, args=(90, WindowPosition.OPEN)).start()

    def tilt(self, angle: int):
        if angle is None or not (0 <= angle <= 90):
            raise InvalidAngleError("Angle must be between 0 and 90 degrees.")
        if angle == 0:
            self.close()
        elif angle == 90:
            self.open()
        else:
            if self.position == WindowPosition.TILTED and self.angle == angle:
                raise InvalidOperationError("The window is already tilted.")
            Thread(target=self._run_tilt_motion, args=(angle, WindowPosition.TILTED)).start()

    def close(self):
        if self.position == WindowPosition.CLOSED:
            raise InvalidOperationError("The window is already closed.")
        Thread(target=self._run_tilt_motion, args=(0, WindowPosition.CLOSED)).start()

    def status(self):
        return WindowStatus(
            angle=self.angle,
            state=self.state,
            position=self.position
        )
