import json
import os
from datetime import datetime
from utilities import save_json, load_json, ensure_directory_exists
from config import Config

class TrainingData:
    def __init__(self, agent_id):
        """Initialize with agent ID, and set up the data directory."""
        self.agent_id = agent_id
        self.data_dir = os.path.join(Config.AGENT_DATA_DIR, agent_id, 'training')
        ensure_directory_exists(self.data_dir)

    def save_training_step(self, step_data):
        """Save a single training step's data."""
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S%f')
        step_file = os.path.join(self.data_dir, f'step_{timestamp}.json')
        save_json(step_data, step_file)

    def load_training_steps(self):
        """Load all training steps for the agent."""
        training_steps = []
        for filename in os.listdir(self.data_dir):
            if filename.endswith('.json'):
                step_data = load_json(os.path.join(self.data_dir, filename))
                training_steps.append(step_data)
        return training_steps

    def get_latest_training_step(self):
        """Retrieve the most recent training step."""
        files = [f for f in os.listdir(self.data_dir) if f.endswith('.json')]
        if not files:
            return None
        latest_file = max(files, key=lambda f: os.path.getmtime(os.path.join(self.data_dir, f)))
        return load_json(os.path.join(self.data_dir, latest_file))

    def clear_training_data(self):
        """Clear all training data."""
        for filename in os.listdir(self.data_dir):
            file_path = os.path.join(self.data_dir, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)

    def get_training_summary(self):
        """Summarize training data for analytics."""
        total_steps = len(self.load_training_steps())
        summary = {
            'agent_id': self.agent_id,
            'total_training_steps': total_steps,
            'last_training_step': self.get_latest_training_step(),
        }
        return summary

    def log_training_progress(self):
        """Log the training progress to a file."""
        summary = self.get_training_summary()
        log_file = os.path.join(Config.LOGS_DIR, f'training_progress_{self.agent_id}.log')
        with open(log_file, 'a') as log:
            log.write(f"{datetime.now()} - Training Progress: {json.dumps(summary, indent=4)}\n")