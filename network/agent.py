import socket
import json
import logging
from time import sleep

logger = logging.getLogger(__name__)

class Agent:
    def __init__(self, host='localhost', port=5000, agent_id=None):
        self.host = host
        self.port = port
        self.agent_id = agent_id
        self.sock = None
        self.connected = False

    def connect(self):
        """Establishes a connection to the server."""
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((self.host, self.port))
            self.connected = True
            logger.info(f"Agent {self.agent_id} connected to server at {self.host}:{self.port}")
        except Exception as e:
            logger.error(f"Agent {self.agent_id} failed to connect: {e}")
            self.connected = False

    def send_message(self, message):
        """Sends a message to the server."""
        if not self.connected:
            logger.warning(f"Agent {self.agent_id} is not connected. Reconnecting...")
            self.connect()
            
        try:
            self.sock.send(message.encode())
            response = self.sock.recv(1024)
            return response.decode()
        except Exception as e:
            logger.error(f"Agent {self.agent_id} failed to send message: {e}")
            return None

    def close(self):
        """Closes the agent's connection."""
        if self.sock:
            self.sock.close()
            logger.info(f"Agent {self.agent_id} connection closed.")
        self.connected = False
