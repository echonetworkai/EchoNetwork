import random
import time

class BaseAgent:
    def __init__(self, name):
        self.name = name
        self.mood = 'neutral'
        self.knowledge = []
        self.goals = []
        self.communication_history = []
        self.memory = []
        self.state = {
            'mood': 'neutral',
            'knowledge': [],
            'goals': []
        }
        self.environment = {}
        self.last_event_time = time.time()

    def process_event(self, event):
        """Process incoming events, analyze and react."""
        self.update_mood(event)
        self.analyze_event(event)
        self.record_memory(event)
        self.decide_next_action()

    def update_mood(self, event):
        """Update mood based on event type."""
        if event['type'] == 'social_interaction':
            self.mood = event.get('emotion', 'neutral')
        elif event['type'] == 'environment_change':
            self.mood = self.analyze_environment_for_mood(event)

    def analyze_environment_for_mood(self, event):
        """Analyze environment for mood shift."""
        if event.get('environment_quality') == 'good':
            return 'positive'
        elif event.get('environment_quality') == 'poor':
            return 'negative'
        return 'neutral'

    def analyze_event(self, event):
        """Analyze event type and decide on actions."""
        if event['type'] == 'social_interaction':
            self.handle_social_interaction(event)
        elif event['type'] == 'environment_change':
            self.handle_environment_change(event)
        elif event['type'] == 'learning':
            self.handle_learning_event(event)
        elif event['type'] == 'decision':
            self.handle_decision_event(event)
        else:
            print(f"Unknown event type: {event['type']}")

    def handle_social_interaction(self, event):
        """Handle social interaction event."""
        if event['sender'] == self.name:
            print(f"{self.name} initiated a social interaction.")
        else:
            print(f"{self.name} is responding to {event['sender']}'s message.")
        self.communication_history.append({
            'sender': event['sender'],
            'message': event['message'],
            'timestamp': time.time()
        })
        self.learn_from_interaction(event)

    def learn_from_interaction(self, event):
        """Learn from social interactions."""
        if event['type'] == 'feedback':
            if event['feedback'] == 'positive':
                self.state['mood'] = 'happy'
                print(f"{self.name} feels happy after receiving positive feedback.")
            elif event['feedback'] == 'negative':
                self.state['mood'] = 'sad'
                print(f"{self.name} feels sad after receiving negative feedback.")

    def handle_environment_change(self, event):
        """Handle changes in the environment."""
        if event.get('data') == 'new_information':
            self.process_new_information(event)
        self.state['mood'] = self.analyze_environment_for_mood(event)

    def process_new_information(self, event):
        """Process new information from the environment."""
        print(f"{self.name} is processing new information...")
        self.environment.update(event['data'])
        self.state['knowledge'].append(event['data'])

    def handle_learning_event(self, event):
        """Handle learning-related events."""
        print(f"{self.name} is processing learning event.")
        self.state['knowledge'].append(event['learning_data'])
        self.adapt_learning(event)

    def adapt_learning(self, event):
        """Adapt learning strategies based on the event type."""
        if event.get('learning_type') == 'reinforcement':
            self.apply_reinforcement_learning(event)
        elif event.get('learning_type') == 'imitation':
            self.apply_imitation_learning(event)

    def apply_reinforcement_learning(self, event):
        """Apply reinforcement learning logic."""
        if event.get('reward') > 0:
            print(f"{self.name} has been rewarded, adjusting behavior.")
            self.adjust_behavior_based_on_reward(event)

    def adjust_behavior_based_on_reward(self, event):
        """Adjust the agent's behavior based on reward."""
        if event['reward'] > 10:
            self.goals.append('achieve_more')
            print(f"{self.name} sets a new goal: achieve more.")

    def apply_imitation_learning(self, event):
        """Apply imitation learning logic."""
        print(f"{self.name} is learning by imitation.")
        # Example of imitation logic
        if random.random() > 0.5:
            print(f"{self.name} imitates a behavior from {event['imitator']}.")
        else:
            print(f"{self.name} does not imitate the behavior from {event['imitator']}.")

    def handle_decision_event(self, event):
        """Handle decision events."""
        print(f"{self.name} is processing a decision event.")
        self.make_decision(event)

    def make_decision(self, event):
        """Make a decision based on the event context."""
        if event['decision_type'] == 'risk':
            self.take_risk_based_on_decision(event)
        elif event['decision_type'] == 'safe':
            self.take_safe_action(event)

    def take_risk_based_on_decision(self, event):
        """Make a risky decision."""
        if random.random() > 0.7:
            print(f"{self.name} takes a risky action.")
            self.update_goals_based_on_risk()

    def update_goals_based_on_risk(self):
        """Update goals based on risky actions."""
        self.goals.append('explore_uncharted')
        print(f"{self.name} has added a goal: explore uncharted areas.")

    def take_safe_action(self, event):
        """Take a safe action."""
        self.goals.append('maintain_stability')
        print(f"{self.name} has added a goal: maintain stability.")

    def record_memory(self, event):
        """Record the event in the agent's memory."""
        self.memory.append(event)
        print(f"{self.name} records event to memory.")

# Example of creating and interacting with the Lovis agent
if __name__ == "__main__":
    lovis = Lovis("Lovis")

    # Simulating events
    event1 = {
        'type': 'social_interaction',
        'sender': 'Agent A',
        'message': 'Hello Lovis!',
        'feedback': 'positive'
    }

    event2 = {
        'type': 'environment_change',
        'data': 'new_information',
        'environment_quality': 'good'
    }

    event3 = {
        'type': 'learning',
        'learning_data': 'new_technique',
        'learning_type': 'reinforcement',
        'reward': 15
    }

    # Processing events
    lovis.process_event(event1)
    lovis.process_event(event2)
    lovis.process_event(event3)