import os

# Configuration for Echo Network
class Config:
    # Directories
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    AGENT_MODELS_DIR = os.path.join(BASE_DIR, 'data', 'models')
    AGENT_DATA_DIR = os.path.join(BASE_DIR, 'data', 'agents')
    LOGS_DIR = os.path.join(BASE_DIR, 'logs')
    
    # Ensure required directories exist
    if not os.path.exists(AGENT_MODELS_DIR):
        os.makedirs(AGENT_MODELS_DIR)
    if not os.path.exists(AGENT_DATA_DIR):
        os.makedirs(AGENT_DATA_DIR)
    if not os.path.exists(LOGS_DIR):
        os.makedirs(LOGS_DIR)

    # Agent settings
    AGENT_LIFESPAN = 3600  # in seconds, example lifespan of an agent
    LEARNING_RATE = 0.01  # Learning rate for agent models
    AGENT_MEMORY_SIZE = 1000  # Maximum size of agent's memory

    # Communication settings
    NETWORK_TIMEOUT = 30  # Timeout in seconds for network connections
    COMMUNICATION_PROTOCOL = 'HTTP'  # Protocol used for agent communication

    # Server settings
    SERVER_HOST = '127.0.0.1'
    SERVER_PORT = 5000
    MAX_CONNECTIONS = 10  # Maximum number of concurrent connections
    
    # Logging settings
    LOGGING_LEVEL = 'INFO'  # Options: DEBUG, INFO, WARNING, ERROR, CRITICAL
    LOG_FILE_NAME = 'echo_network.log'  # Log file name
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

    # Network simulation settings
    SIMULATION_STEP_INTERVAL = 1  # Interval in seconds between each simulation step
    AGENT_INTERACTION_THRESHOLD = 0.8  # Threshold to trigger agent interactions

    # Other configurations
    ENABLE_AGENT_MONITORING = True
    SKIP_INTRO = False  # Whether to skip the introduction sequence
    AGENT_INTERACTION_RATE = 0.1  # Probability of agent interaction per step

    @staticmethod
    def get_config():
        """Returns the current configuration settings."""
        return {
            'agent_lifespan': Config.AGENT_LIFESPAN,
            'learning_rate': Config.LEARNING_RATE,
            'network_timeout': Config.NETWORK_TIMEOUT,
            'communication_protocol': Config.COMMUNICATION_PROTOCOL,
            'server_host': Config.SERVER_HOST,
            'server_port': Config.SERVER_PORT,
            'max_connections': Config.MAX_CONNECTIONS,
            'logging_level': Config.LOGGING_LEVEL,
            'log_file_name': Config.LOG_FILE_NAME,
            'simulation_step_interval': Config.SIMULATION_STEP_INTERVAL,
            'agent_interaction_threshold': Config.AGENT_INTERACTION_THRESHOLD,
            'enable_agent_monitoring': Config.ENABLE_AGENT_MONITORING,
            'skip_intro': Config.SKIP_INTRO,
            'agent_interaction_rate': Config.AGENT_INTERACTION_RATE,
        }
