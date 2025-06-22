from abc import ABC, abstractmethod
from dataclasses import dataclass

from domoticASW.domoticASWProtocol import PropertyId

@dataclass(frozen=True)
class ServerAddress():
    host: str
    port: int

class ServerCommunicationProtocol(ABC):
    @abstractmethod
    async def send_event(self, server_address: ServerAddress, event, id: str):
        pass

    @abstractmethod
    async def update_state(self, server_address: ServerAddress, property_name: PropertyId, property_value, id: str):
        pass