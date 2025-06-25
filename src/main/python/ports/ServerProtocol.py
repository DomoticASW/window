from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass(frozen=True)
class ServerAddress():
    host: str
    port: int

@dataclass(frozen=True)
class BroadcastMessage():
    id: str
    name: str
    port: int

class ServerCommunicationProtocol(ABC):
    @abstractmethod
    async def send_event(self, server_address: ServerAddress, event, id: str):
        pass

    @abstractmethod
    async def update_state(self, server_address: ServerAddress, property_name, property_value, id: str):
        pass

    @abstractmethod
    async def announce(self, discovery_broadcast_address: ServerAddress, device_port: int, smart_window_id: str, smart_window_name: str) -> None:
        pass