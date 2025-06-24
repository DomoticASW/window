import asyncio
from enum import Enum
from threading import Thread
import threading
import time
from pydantic import BaseModel

from adapters.ServerCommunicationProtocolHttpAdapter import ServerCommunicationProtocolHttpAdapter
from domain.SmartWindow import SmartWindow, WindowPosition, WindowState
from ports.ServerProtocol import ServerAddress

class Event(str, Enum):
  OPENED = "Opened"
  CLOSED = "Closed"

class SmartWindowAgent(Thread):
  _server_address: ServerAddress
  def __init__(self, smart_window: SmartWindow, server: ServerCommunicationProtocolHttpAdapter, period_sec=1):
    super().__init__(daemon=True)
    self.loop = asyncio.new_event_loop()
    threading.Thread(target=self.loop.run_forever, daemon=True).start()
    self._stop = False
    self.smart_window = smart_window
    self.server = server
    self._server_address = None
    self.period_sec = period_sec
    self._last_state = None

  def stop(self):
    self._stop = True

  def run(self):
    print(f"AGENT: Starting agent for smart window {self.smart_window.id} with period {self.period_sec} seconds")
    while not self._stop:
      time.sleep(self.period_sec)
      status = self.smart_window.status()
      if self._has_meaningful_change(status.state):
        print(f"AGENT: EVENT!!: {status.state}")
        future = asyncio.run_coroutine_threadsafe(self.server.send_event(self._server_address, self._build_event(status.position), self.smart_window.id), self.loop)
        try: 
          future.result()
        except Exception as e:
          print(f"AGENT ERROR! Errore nell'invio dell'evento' {e}")  # Only for debugging purposes
      for property_name, property_value in status.items():
        future = asyncio.run_coroutine_threadsafe(self.server.update_state(self._server_address, property_name, property_value, self.smart_window.id), self.loop)
        try: 
          future.result()
        except Exception as e:
          print(f"AGENT ERROR! Errore nell'aggiornamento dello stato {e}")
      self._last_state = status.state

  def _has_meaningful_change(self, current_state: WindowState) -> bool:
    print(f"AGENT: Checking for meaningful change: Last state: {self._last_state}, Current state: {current_state}")
    return self._last_state != current_state
    
  def _build_event(self, position: WindowPosition) -> Event | None:
    if position == WindowPosition.OPEN:
      return Event.OPENED
    elif position == WindowPosition.CLOSED:
      return Event.CLOSED
    return None

  def set_server_address(self, server_address: ServerAddress):
    print(f"AGENT: Device registered with address: {server_address.host}:{server_address.port}")
    self._server_address = server_address