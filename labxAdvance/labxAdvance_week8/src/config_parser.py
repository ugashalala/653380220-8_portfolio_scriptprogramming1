# labxAdvance_week8/src/config_parser.py
import json
import os
from utils import setup_logging

logger = setup_logging(__name__)

class ConfigParser:
    """Parses and validates the data automation configuration from a JSON file."""
    def __init__(self, config_path):
        self.config_path = config_path
        self.config = {}

    def load_config(self):
        """Loads the configuration from the specified JSON file."""
        if not os.path.exists(self.config_path):
            logger.critical(f"Configuration file not found: {self.config_path}")
            raise FileNotFoundError(f"Configuration file not found: {self.config_path}")
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
            self._validate_config()
            logger.info(f"Configuration loaded successfully from {self.config_path}")
            return self.config
        except json.JSONDecodeError as e:
            logger.critical(f"Invalid JSON format in config file: {e}")
            raise ValueError(f"Invalid JSON format in config file: {e}")
        except Exception as e:
            logger.critical(f"An error occurred while loading config: {e}")
            raise Exception(f"An error occurred while loading config: {e}")

    def _validate_config(self):
        """Validates the loaded configuration."""
        if "tasks" not in self.config or not isinstance(self.config["tasks"], list):
            raise ValueError("Missing or invalid 'tasks' field in config.")

        for i, task in enumerate(self.config["tasks"]):
            if "type" not in task:
                raise ValueError(f"Task {i} is missing 'type' field.")
            if "output_data_key" not in task and task["type"] not in ["save_csv", "save_json"]:
                logger.warning(f"Task {i} (type: {task['type']}) has no 'output_data_key'.")

            if task["type"] in ["load_csv", "load_json", "save_csv", "save_json"]:
                if "file_path" not in task:
                    raise ValueError(f"Task {i} (type: {task['type']}) requires 'file_path'.")

        logger.info("Configuration validated.")