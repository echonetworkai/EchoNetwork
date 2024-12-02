import json
import os
from utilities import save_json, load_json, ensure_directory_exists
from config import Config

class AgentData:
    def __init__(self, agent_id):
        """Initialize the agent data object with a unique agent ID."""
        self.agent_id = agent_id
        self.data_dir = os.path.join(Config.AGENT_DATA_DIR, agent_id)
        ensure_directory_exists(self.data_dir)
        self.agent_file = os.path.join(self.data_dir, 'agent_data.json')

    def save_agent_state(self, state_data):
        """Save the current state of the agent."""
        save_json(state_data, self.agent_file)

    def load_agent_state(self):
        """Load the current state of the agent."""
        return load_json(self.agent_file)

    def update_agent_state(self, state_data):
        """Update the state of the agent."""
        current_state = self.load_agent_state()
        current_state.update(state_data)
        self.save_agent_state(current_state)

    def get_agent_summary(self):
        """Get a summary of the agent's data (e.g., performance, model status)."""
        agent_state = self.load_agent_state()
        summary = {
            'agent_id': self.agent_id,
            'status': agent_state.get('status', 'unknown'),
            'last_updated': agent_state.get('last_updated', 'unknown'),
            'performance': agent_state.get('performance', {}),
        }
        return summary

    def clear_agent_data(self):
        """Clear the agent's data."""
        if os.path.exists(self.agent_file):
            os.remove(self.agent_file)

    def log_agent_performance(self):
        """Log the agent's performance to a log file."""
        agent_summary = self.get_agent_summary()
        log_file = os.path.join(Config.LOGS_DIR, f'agent_performance_{self.agent_id}.log')
        with open(log_file, 'a') as log:
            log.write(f"{datetime.now()} - Agent Performance: {json.dumps(agent_summary, indent=4)}\n")

    def save_agent_model(self, model_data):
        """Save the agent's model data (e.g., weights)."""
        model_file = os.path.join(self.data_dir, 'agent_model.json')
        save_json(model_data, model_file)

    def load_agent_model(self):
        """Load the agent's model data."""
        model_file = os.path.join(self.data_dir, 'agent_model.json')
        return load_json(model_file)