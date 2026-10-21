
import logging
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from the project .env file
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

# Configure basic logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def setup_logging(name, level=logging.INFO):
    """Sets up a logger for specific modules."""
    logger = logging.getLogger(name)
    logger.setLevel(level)
    return logger


def get_env_variable(var_name):
    """Retrieves an environment variable."""
    value = os.getenv(var_name)

    if value is None or not value.strip():
        raise ValueError(
            f"Environment variable '{var_name}' not set. "
            "Please check your .env file or environment settings."
        )

    return value.strip()


def ensure_directory_exists(path):
    """Ensures that a directory exists."""
    try:
        os.makedirs(path, exist_ok=True)
        logging.info(f"Directory ensured: {path}")
    except OSError as e:
        logging.error(f"Error creating directory {path}: {e}")
        raise
