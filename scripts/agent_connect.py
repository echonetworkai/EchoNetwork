import sys
import time
import logging
from agents.agent import Agent  # Assuming Agent class exists in agents/agent.py
from network.server import Server  # Assuming Server class exists in network/server.py

# Setup logging configuration
logging.basicConfig(filename='connection_log.txt', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def simulate_agent_connection():
    try:
        # Initialize the server and start it
        server = Server()
        server.start()  # Start the server, assuming start() method exists
        logging.info("Server started successfully.")

        # Create an agent instance
        agent = Agent()

        # Attempt to connect the agent
        connection_status = agent.connect()  # Assuming connect() method exists in Agent class
        
        if connection_status:
            logging.info(f"Agent {agent.id} connected successfully.")
            print(f"Agent {agent.id} connected to the server.")
        else:
            logging.warning(f"Agent {agent.id} failed to connect.")
            print(f"Agent {agent.id} failed to connect.")

        # Simulate agent registration
        registration_status = agent.register()  # Assuming register() method exists in Agent class
        if registration_status:
            logging.info(f"Agent {agent.id} registered successfully.")
            print(f"Agent {agent.id} registered successfully.")
        else:
            logging.warning(f"Agent {agent.id} registration failed.")
            print(f"Agent {agent.id} registration failed.")
        
        # Simulate communication with server
        if agent.is_connected():
            print(f"Agent {agent.id} is connected and ready for communication.")
            logging.info(f"Agent {agent.id} is ready for communication.")
        else:
            logging.warning(f"Agent {agent.id} is not connected.")
            print(f"Agent {agent.id} is not connected.")
        
        # Simulate agent disconnection after some time
        time.sleep(5)  # Wait for 5 seconds to simulate active agent communication
        agent.disconnect()  # Assuming disconnect() method exists in Agent class
        
        # Check if agent disconnected successfully
        if not agent.is_connected():
            logging.info(f"Agent {agent.id} disconnected successfully.")
            print(f"Agent {agent.id} disconnected successfully.")
        else:
            logging.warning(f"Agent {agent.id} failed to disconnect.")
            print(f"Agent {agent.id} failed to disconnect.")
        
    except Exception as e:
        logging.error(f"Error during agent connection simulation: {e}")
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    simulate_agent_connection()