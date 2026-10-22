# labxAdvance_week8/src/json_tasks.py
import json
import os
from utils import setup_logging, ensure_directory_exists

logger = setup_logging(__name__)

class JSONTasks:
    """Handles reading, writing, and updating JSON data."""
    def __init__(self):
        logger.info("JSONTasks initialized.")

    def load_json(self, file_path):
        if not os.path.exists(file_path):
            logger.error(f"JSON file not found: {file_path}")
            return None
        try:
            with open(file_path, mode='r', encoding='utf-8') as file:
                data = json.load(file)
            logger.info(f"Successfully loaded JSON from {file_path}.")
            return data
        except Exception as e:
            logger.error(f"Error loading JSON file {file_path}: {e}")
            return None

    def save_json(self, data, file_path, indent=2):
        ensure_directory_exists(os.path.dirname(file_path))
        try:
            with open(file_path, mode='w', encoding='utf-8') as file:
                json.dump(data, file, indent=indent, ensure_ascii=False)
            logger.info(f"Successfully saved JSON to {file_path}.")
            return True
        except Exception as e:
            logger.error(f"Error saving JSON file {file_path}: {e}")
            return False

    def update_json_data(self, data, updates):
        if not data:
            return data
        modified_data = json.loads(json.dumps(data))
        for update in updates:
            path = update.get("path", "")
            value = update.get("value")
            operation = update.get("operation", "set")

            if operation == "add_to_list" and path == "" and isinstance(modified_data, list):
                modified_data.append(value)
                continue

            keys = path.split('.')
            current = modified_data
            try:
                for key in keys[:-1]:
                    if key.isdigit() and isinstance(current, list):
                        current = current[int(key)]
                    elif isinstance(current, dict):
                        current = current[key]

                target = keys[-1]
                if operation == "set":
                    if target.isdigit() and isinstance(current, list):
                        current[int(target)] = value
                    elif isinstance(current, dict):
                        current[target] = value
                elif operation == "add_to_list" and isinstance(current.get(target), list):
                    current[target].append(value)
            except Exception as e:
                logger.warning(f"Could not apply update {update}: {e}")
        return modified_data

    def query_json_data(self, data, path):
        if not data:
            return None
        keys = path.split('.')
        current = data
        try:
            for key in keys:
                if key.isdigit() and isinstance(current, list):
                    current = current[int(key)]
                elif isinstance(current, dict):
                    current = current.get(key)
                else:
                    return None
            return current
        except Exception as e:
            logger.error(f"Error querying JSON path {path}: {e}")
            return None