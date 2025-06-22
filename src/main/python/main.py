import os
import uvicorn
from adapters.ServerCommunicationProtocolHttpAdapter import ServerCommunicationProtocolHttpAdapter
from domain.SmartWindow import InvalidOperationError, SmartWindow
from ports.ServerProtocol import ServerAddress

if __name__ == "__main__":
  # device_server_port = os.getenv("DEVICE_SERVER_PORT", "8080")
  # server_port = os.getenv("SERVER_PORT")
  # server = ServerCommunicationProtocolHttpAdapter()
  smart_window = SmartWindow("1", "Smart Window")
  # Usage example
  smart_window.open()
  smart_window.tilt(30.0)
  smart_window.close()
  try:
    smart_window.close()
  except InvalidOperationError as e:
    print(e)