import random
import time
import logging

# Setup logging configuration
logging.basicConfig(filename='agent_learning_log.txt', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

class Agent:
    def __init__(self, id, learning_rate=0.1, discount_factor=0.9, exploration_rate=1.0, exploration_decay=0.995):
        self.id = id
        self.learning_rate = learning_rate  # Learning rate for updates
        self.discount_factor = discount_factor  # Discount factor for future rewards
        self.exploration_rate = exploration_rate  # Exploration-exploitation tradeoff
        self.exploration_decay = exploration_decay  # Decay of exploration over time
        
        self.q_table = {}  # Q-Table to store learned values
        self.actions = ["move_left", "move_right", "move_up", "move_down"]  # Example set of actions
        
    def get_state(self):
        # Simulating agent's state as a tuple of (x, y) coordinates, which may change over time
        return (random.randint(0, 10), random.randint(0, 10))
    
    def choose_action(self, state):
        # Exploration vs exploitation: choose a random action or the best-known action
        if random.uniform(0, 1) < self.exploration_rate:
            action = random.choice(self.actions)  # Exploration: random action
        else:
            action = self.get_best_action(state)  # Exploitation: best known action based on Q-table
        return action
    
    def get_best_action(self, state):
        # If state is not in Q-table, initialize it
        if state not in self.q_table:
            self.q_table[state] = {action: 0.0 for action in self.actions}
        
        # Return the action with the highest Q-value for the current state
        best_action = max(self.q_table[state], key=self.q_table[state].get)
        return best_action
    
    def update_q_table(self, state, action, reward, next_state):
        # Initialize state-action pair in Q-table if not present
        if state not in self.q_table:
            self.q_table[state] = {action: 0.0 for action in self.actions}
        if next_state not in self.q_table:
            self.q_table[next_state] = {action: 0.0 for action in self.actions}

        # Q-learning update rule
        best_future_q = max(self.q_table[next_state].values())  # Best future Q-value
        self.q_table[state][action] += self.learning_rate * (reward + self.discount_factor * best_future_q - self.q_table[state][action])
    
    def simulate_environment(self, state, action):
        # Simulate environment response based on the chosen action
        # This is a dummy environment with rewards and penalties
        if action == "move_left":
            next_state = (state[0] - 1, state[1])
            reward = -1  # Moving left is penalized
        elif action == "move_right":
            next_state = (state[0] + 1, state[1])
            reward = 1  # Moving right is rewarded
        elif action == "move_up":
            next_state = (state[0], state[1] + 1)
            reward = 0  # Neutral action
        elif action == "move_down":
            next_state = (state[0], state[1] - 1)
            reward = 0  # Neutral action
        else:
            next_state = state
            reward = -1  # Unknown action penalized

        return next_state, reward
    
    def learn_from_experience(self, episodes=100):
        # Simulate the agent learning over a number of episodes
        for episode in range(episodes):
            state = self.get_state()  # Start at a random state
            done = False
            total_reward = 0

            while not done:
                action = self.choose_action(state)  # Choose an action based on the state
                next_state, reward = self.simulate_environment(state, action)  # Simulate the environment's response
                
                # Update the Q-table with the experience
                self.update_q_table(state, action, reward, next_state)
                
                # Update state and total reward
                state = next_state
                total_reward += reward
                
                # Simulate episode ending condition (e.g., reaching a certain state)
                if state[0] >= 10 or state[1] >= 10:
                    done = True

            # Decay exploration rate after each episode
            self.exploration_rate *= self.exploration_decay
            
            # Log learning progress
            logging.info(f"Episode {episode+1}/{episodes} - Total Reward: {total_reward} - Exploration Rate: {self.exploration_rate:.4f}")
        
    def print_q_table(self):
        # Print the Q-table for debugging purposes
        for state, actions in self.q_table.items():
            print(f"State: {state} -> {actions}")

def main():
    # Initialize agent with basic parameters
    agent = Agent(id=1)
    
    # Start learning process
    agent.learn_from_experience(episodes=100)
    
    # Print Q-table after learning
    agent.print_q_table()

if __name__ == "__main__":
    main()