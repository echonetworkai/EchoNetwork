import logging
import json
from abc import ABC, abstractmethod

# Setting up basic logging for the agent interface
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AgentInterface(ABC):
    """
    Abstract base class to define the common interface for agents
    in the Echo Network. Each agent will implement the methods for 
    communication, learning, and interaction with the network.
    """

    def __init__(self, agent_id, name):
        self.agent_id = agent_id
        self.name = name
        self.status = "inactive"
        self.data = {}

    @abstractmethod
    def send_message(self, message):
        """
        Send a message to the network or another agent.
        Each agent will implement this method to define how they send messages.
        """
        pass

    @abstractmethod
    def receive_message(self, message):
        """
        Receive a message from the network or another agent.
        Each agent will implement this method to handle incoming messages.
        """
        pass

    @abstractmethod
    def update_status(self, status):
        """
        Update the status of the agent. This could represent different
        states like 'active', 'learning', 'idle', etc.
        """
        self.status = status
        logger.info(f"Agent {self.name} ({self.agent_id}) status updated to {self.status}")

    @abstractmethod
    def learn_from_experience(self, experience_data):
        """
        Each agent learns from experience. This could involve
        updating weights, modifying internal states, or adjusting strategies.
        """
        pass

    @abstractmethod
    def get_state(self):
        """
        Return the current state of the agent. This could be used to track
        things like memory, learning progress, or any relevant data.
        """
        return {
            "agent_id": self.agent_id,
            "name": self.name,
            "status": self.status,
            "data": self.data
        }

class CommunicationAgent(AgentInterface):
    """
    A concrete class for an agent that communicates with other agents or 
    the network. This agent could represent any type of communication-based agent 
    like Lovis, Reiner, etc.
    """

    def __init__(self, agent_id, name):
        super().__init__(agent_id, name)
        self.inbox = []
        self.outbox = []

    def send_message(self, message):
        """
        Send a message to another agent or the network.
        For the sake of this example, we will just log the message and
        store it in the outbox.
        """
        logger.info(f"Agent {self.name} sending message: {message}")
        self.outbox.append(message)

    def receive_message(self, message):
        """
        Receive a message and log it. For this example, we'll store received messages
        in an inbox for later processing.
        """
        logger.info(f"Agent {self.name} received message: {message}")
        self.inbox.append(message)

    def learn_from_experience(self, experience_data):
        """
        Implement the agent's learning process based on the experience data it receives.
        For simplicity, this just updates the agent's internal data with new experiences.
        """
        logger.info(f"Agent {self.name} learning from experience: {experience_data}")
        self.data.update(experience_data)

    def process_inbox(self):
        """
        Process all the messages in the inbox. This could be a more complex
        logic based on the kind of message.
        """
        for message in self.inbox:
            # This is just a placeholder for processing logic
            logger.info(f"Processing message: {message}")

        # Clear inbox after processing
        self.inbox.clear()

class LearningAgent(AgentInterface):
    """
    A concrete class for an agent focused on learning from data and interacting with
    other agents or the environment to improve its performance.
    """

    def __init__(self, agent_id, name, learning_rate=0.1):
        super().__init__(agent_id, name)
        self.learning_rate = learning_rate
        self.knowledge_base = []

    def send_message(self, message):
        """
        Sends a message to the network or another agent. Learning agents
        could send updates based on their learning progress.
        """
        logger.info(f"Agent {self.name} sending learning update: {message}")
        # Example: Could send an update message about its learning process
        # (In real applications, this could be more complex)
        self.outbox.append(message)

    def receive_message(self, message):
        """
        Handle incoming messages, possibly learning from them.
        """
        logger.info(f"Agent {self.name} received learning message: {message}")
        self.inbox.append(message)

    def learn_from_experience(self, experience_data):
        """
        In a learning agent, this function would process experience data to
        update the agent's learning model or knowledge base.
        """
        logger.info(f"Agent {self.name} processing experience: {experience_data}")
        self.knowledge_base.append(experience_data)
        self.update_status("learning")

    def process_inbox(self):
        """
        Process all messages in the inbox that could help improve learning.
        """
        for message in self.inbox:
            # Learn from the message content (for this example, we're appending to the knowledge base)
            self.learn_from_experience(message)

        # Clear inbox after processing
        self.inbox.clear()

# Example usage:
if __name__ == "__main__":
    # Create communication agent and learning agent
    agent_1 = CommunicationAgent(agent_id="001", name="Lovis")
    agent_2 = LearningAgent(agent_id="002", name="Reiner")

    # Simulate sending and receiving messages
    agent_1.send_message("Hello Reiner, let's collaborate!")
    agent_2.receive_message("Hello Reiner, let's collaborate!")

    # Process messages and learn from experience
    agent_2.learn_from_experience({"collaboration_knowledge": "Sharing data improves outcomes"})
    agent_2.process_inbox()

    # Print agent state
    print(agent_2.get_state())