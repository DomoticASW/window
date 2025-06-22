import httpx
from domoticASW.domoticASWProtocol import PropertyId
from ports import ServerProtocol
from ports.ServerProtocol import ServerCommunicationProtocol

class ServerCommunicationProtocolHttpAdapter(ServerCommunicationProtocol):
  async def send_event(self, server_address: ServerProtocol.ServerAddress, event, id: str) -> None:
    print(f"CLIENT: Sending event http://{server_address.host}:{server_address.port}/api/devices/{id}/events")
    async with httpx.AsyncClient() as client:
      await client.post(f"http://{server_address.host}:{server_address.port}/api/devices/{id}/events",
                              json={"event": event.value})
  
  async def update_state(self, server_address: ServerProtocol.ServerAddress, property_name: PropertyId, property_value, id: str) -> None:
    async with httpx.AsyncClient() as client:
      print(f"CLIENT: Updating state for washing machine value: {property_name} = {property_value}")
      await client.patch(f"http://{server_address.host}:{server_address.port}/api/devices/{id}/properties/{property_name}",
                              json={"value": property_value})
