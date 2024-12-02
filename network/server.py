import socket
import threading
import json
import logging
import time
from communication import EchoNetworkCommunication
from agent import Agent
from utils import format_message, setup_logger

# Setup logger
setup_logger()
logger = logging.getLogger(__name__)

class Server:
    def __init__(self, host='localhost', port=5000):
        self.host = host
        self.port = port
        self.server_socket = None
        self.agents = {}  # Dictionary to store agent objects by their ID
        self.communication = EchoNetworkCommunication(host=self.host, port=self.port)
        self.running = False

    def start(self):
        """Starts the server and begins accepting incoming connections."""
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)  # Max 5 queued connections

        self.running = True
        logger.info(f"Server started, listening on {self.host}:{self.port}")

        # Start the communication process in a separate thread
        threading.Thread(target=self.communication.start_server).start()

        # Accept incoming connections
        while self.running:
            try:
                client_socket, client_address = self.server_socket.accept()
                logger.info(f"New connection from {client_address}")

                # Create an agent for the connected client
                agent = Agent(socket=client_socket, address=client_address)
                threading.Thread(target=self.handle_agent, args=(agent,)).start()
            except Exception as e:
                logger.error(f"Error accepting connections: {e}")

    def handle_agent(self, agent):
        """Handles communication with an individual agent."""
        try:
            # Adding agent to the agent dictionary
            self.agents[agent.agent_id] = agent
            logger.info(f"Agent {agent.agent_id} added to server")

            # Continuously receive messages from the agent
            while self.running:
                message = agent.receive_message()
                if message:
                    logger.info(f"Received message from Agent {agent.agent_id}: {message}")
                    self.process_message(agent, message)
                else:
                    # If no message, the agent might have disconnected
                    logger.info(f"Agent {agent.agent_id} disconnected.")
                    break
        except Exception as e:
            logger.error(f"Error handling agent {agent.agent_id}: {e}")
        finally:
            self.remove_agent(agent)

    def process_message(self, agent, message):
        """Processes the message received from an agent."""
        try:
            # Example: Process the message and broadcast it to other agents
            formatted_message = format_message(message, agent.agent_id)
            self.broadcast_message(formatted_message, agent)

            # Optionally handle specific messages (e.g., command processing)
            if message == "shutdown":
                logger.info("Shutdown command received. Closing server...")
                self.shutdown()
        except Exception as e:
            logger.error(f"Error processing message from Agent {agent.agent_id}: {e}")

    def broadcast_message(self, message, sender_agent):
        """Broadcasts a message to all connected agents."""
        for agent_id, agent in self.agents.items():
            if agent_id != sender_agent.agent_id:  # Don't send the message back to the sender
                agent.send_message(message)
                logger.info(f"Broadcasting message to Agent {agent_id}: {message}")

    def shutdown(self):
        """Shuts down the server gracefully."""
        logger.info("Server shutting down...")
        self.running = False
        self.server_socket.close()

        # Close all agent connections
        for agent in self.agents.values():
            agent.close()

        # Stop the communication service
        self.communication.close_server()
        logger.info("Server successfully shut down.")

    def remove_agent(self, agent):
        """Removes an agent from the server."""
        if agent.agent_id in self.agents:
            del self.agents[agent.agent_id]
            agent.close()
            logger.info(f"Agent {agent.agent_id} removed from server.")

# Example of running the server
if __name__ == "__main__":
    try:
        server = Server(host='localhost', port=5000)
        server.start()
    except KeyboardInterrupt:
        logger.info("Server interrupted. Shutting down...")
        server.shutdown()