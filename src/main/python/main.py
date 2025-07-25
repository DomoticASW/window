import os
import uvicorn
from adapters.ServerCommunicationProtocolHttpAdapter import ServerCommunicationProtocolHttpAdapter
from domain.SmartWindow import InvalidOperationError, SmartWindow
from domain.SmartWindowAgent import SmartWindowAgent
from adapters.DomoticASWHttpProtocol import create_server
from ports.ServerProtocol import ServerAddress

if __name__ == "__main__":
  device_server_port = os.getenv("DEVICE_SERVER_PORT", "8092")
  server_port = os.getenv("SERVER_PORT", None)
  server = ServerCommunicationProtocolHttpAdapter()
  server_broadcast_port = os.getenv("SERVER_DISCOVERY_PORT",  "30000")
  server_broadcast_host = os.getenv("SERVER_DISCOVERY_ADDR", "255.255.255.255")
  server_broadcast_address = ServerAddress(server_broadcast_host, int(server_broadcast_port))
  sw_id = os.getenv("ID", "sm_1")
  sw_name = os.getenv("NAME", "Smart Window 1")
  smart_window = SmartWindow(sw_id, sw_name)
  smart_window_agent = SmartWindowAgent(smart_window, server, server_broadcast_address, device_port=int(device_server_port), period_sec=1)
  app = create_server(smart_window_agent)
  if(server_port is not None and server_port != ""):
    print("Server: ", server_port)
    smart_window_agent.set_server_address(
        ServerAddress("localhost", int(server_port))
    )
  smart_window_agent.start()
  uvicorn.run(app, host="0.0.0.0", port=int(device_server_port))