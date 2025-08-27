from dataclasses import asdict
import json
import socket
import httpx
from ports import ServerProtocol
from ports.ServerProtocol import ServerCommunicationProtocol

class ServerCommunicationProtocolHttpAdapter(ServerCommunicationProtocol):
  async def send_event(self, server_address: ServerProtocol.ServerAddress, event, id: str) -> None:
    print(f"CLIENT: Sending event http://{server_address.host}:{server_address.port}/api/devices/{id}/events")
    async with httpx.AsyncClient() as client:
      await client.post(f"http://{server_address.host}:{server_address.port}/api/devices/{id}/events",
                              json={"event": event.value})
  
  async def update_state(self, server_address: ServerProtocol.ServerAddress, property_name: str, property_value, id: str) -> None:
    async with httpx.AsyncClient() as client:
      print(f"CLIENT: Updating state for washing machine value: {property_name} = {property_value}")
      await client.patch(f"http://{server_address.host}:{server_address.port}/api/devices/{id}/properties/{property_name}",
                              json={"value": property_value})
      
  async def announce(self, discovery_broadcast_address: ServerProtocol.ServerAddress, device_port: int, smart_window_id: str, smart_window_name: str, lan_hostname: str) -> None:
    message = ServerProtocol.BroadcastMessage(
        id=smart_window_id,
        name=smart_window_name,
        lanHostname = lan_hostname,
        port=device_port
    )
    broadcast_ip = discovery_broadcast_address.host
    broadcast_port = discovery_broadcast_address.port
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            sock.settimeout(1)

            data = json.dumps(asdict(message)).encode('utf-8')
            sock.sendto(data, (broadcast_ip, broadcast_port))