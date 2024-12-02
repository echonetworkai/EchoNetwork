import json
import logging
import socket
import threading
import time
from queue import Queue

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class CommunicationError(Exception):
    """Custom exception for communication errors."""
    pass

class EchoNetworkCommunication:
    def __init__(self, host='localhost', port=5000, max_retries=3):
        """
        Initializes the communication system.

        :param host: The host for the communication system (default: 'localhost').
        :param port: The port to listen for incoming messages (default: 5000).
        :param max_retries: The maximum number of retries for failed messages (default: 3).
        """
        self.host = host
        self.port = port
        self.sock = None
        self.connected = False
        self.messages = []
        self.message_queue = Queue()
        self.agent_status = {}
        self.max_retries = max_retries

    def start_server(self):
        """Starts the server to listen for incoming agent communications."""
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.bind((self.host, self.port))
            self.sock.listen(5)
            logger.info(f"Server listening on {self.host}:{self.port}")
            self.connected = True

            while self.connected:
                client_sock, client_addr = self.sock.accept()
                logger.info(f"Connection established with {client_addr}")
                threading.Thread(target=self.handle_client, args=(client_sock, client_addr)).start()

        except Exception as e:
            logger.error(f"Error starting server: {e}")
            raise CommunicationError(f"Failed to start server: {e}")

    def handle_client(self, client_sock, client_addr):
        """
        Handles communication with a connected client (agent).

        :param client_sock: The socket object representing the connection.
        :param client_addr: The address of the connected client.
        """
        try:
            while True:
                message = client_sock.recv(1024)
                if not message:
                    break

                logger.info(f"Received message from {client_addr}: {message.decode()}")
                self.messages.append(message.decode())

                # Update agent status (for example, 'active' or 'idle')
                self.update_agent_status(client_addr, 'active')

                # Respond to the client
                client_sock.send(json.dumps({"status": "received", "message": message.decode()}).encode())

        except Exception as e:
            logger.error(f"Error communicating with client {client_addr}: {e}")
            self.update_agent_status(client_addr, 'idle')
            raise CommunicationError(f"Client communication error: {e}")
        finally:
            client_sock.close()

    def send_message(self, host, port, message, retries=0):
        """
        Sends a message to a specific agent (client).

        :param host: The host of the agent.
        :param port: The port where the agent is listening.
        :param message: The message to send.
        :param retries: The number of retries if the message fails to send.
        """
        try:
            client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_sock.connect((host, port))
            logger.info(f"Sending message to {host}:{port}")
            client_sock.send(message.encode())

            response = client_sock.recv(1024)
            logger.info(f"Received response from {host}:{port}: {response.decode()}")
            return json.loads(response.decode())

        except Exception as e:
            logger.error(f"Error sending message to {host}:{port}: {e}")
            if retries < self.max_retries:
                logger.info(f"Retrying ({retries + 1}/{self.max_retries})...")
                time.sleep(1)  # Wait before retrying
                return self.send_message(host, port, message, retries + 1)
            else:
                logger.error(f"Failed to send message after {self.max_retries} retries.")
                raise CommunicationError(f"Failed to send message: {e}")
        finally:
            client_sock.close()

    def broadcast_message(self, agents, message):
        """
        Broadcasts a message to all connected agents.

        :param agents: List of agent host:port tuples.
        :param message: The message to send to all agents.
        """
        for agent in agents:
            host, port = agent
            try:
                self.send_message(host, port, message)
                logger.info(f"Broadcasted message to {host}:{port}")
            except CommunicationError as e:
                logger.error(f"Failed to send to {host}:{port} - {e}")

    def update_agent_status(self, agent_addr, status):
        """
        Updates the status of an agent.

        :param agent_addr: The address of the agent (host, port).
        :param status: The status to set (e.g., 'active', 'idle').
        """
        self.agent_status[agent_addr] = status
        logger.info(f"Updated agent {agent_addr} status to {status}")

    def get_agent_status(self, agent_addr):
        """
        Retrieves the status of a specific agent.

        :param agent_addr: The address of the agent (host, port).
        :return: The current status of the agent.
        """
        return self.agent_status.get(agent_addr, 'unknown')

    def close_server(self):
        """Closes the communication server."""
        if self.sock:
            self.sock.close()
            self.connected = False
            logger.info("Server connection closed.")
        else:
            logger.warning("Server is not active.")

    def process_message_queue(self):
        """Process the message queue and send out pending messages."""
        while not self.message_queue.empty():
            message = self.message_queue.get()
            self.broadcast_message(message['agents'], message['content'])
            logger.info(f"Processed queued message: {message['content']}")

    def queue_message(self, agents, message):
        """
        Adds a message to the queue for later broadcasting.

        :param agents: List of agents to send the message to.
        :param message: The content of the message.
        """
        self.message_queue.put({'agents': agents, 'content': message})
        logger.info(f"Message queued: {message}")

# Example usage

if __name__ == "__main__":
    comm = EchoNetworkCommunication(host='localhost', port=5000)

    # Start the server in a separate thread
    threading.Thread(target=comm.start_server).start()

    # Simulate sending a message to a specific agent with retry logic
    try:
        comm.send_message('localhost', 5001, "Hello, Reiner!")
    except CommunicationError:
        logger.error("Failed to send message after retries.")

    # Broadcast a message to multiple agents
    agents = [('localhost', 5001), ('localhost', 5002)]
    comm.broadcast_message(agents, "System update!")

    # Queue a message for later broadcasting
    comm.queue_message(agents, "Scheduled update in 5 minutes.")

    # Process queued messages
    comm.process_message_queue()

    # Stop the server after a while
    # comm.close_server()