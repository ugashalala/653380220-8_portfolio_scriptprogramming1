# agentic-spreadsheet-processor/main.py
import sys
import os

# เพิ่มไดเรกทอรี 'src' เข้าสู่ Python Path ป้องกัน ModuleNotFoundError
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from config_parser import ConfigParser
from spreadsheet_agent import SpreadsheetAgent
from utils import setup_logging

logger = setup_logging(__name__)

def main():
    base_dir = os.path.dirname(__file__)
    config_file_path = os.path.join(base_dir, 'configs', 'example_spreadsheet_config.json')

    try:
        os.makedirs(os.path.join(base_dir, 'data'), exist_ok=True)
        config_parser = ConfigParser(config_file_path)
        config = config_parser.load_config()

        # แปลง Path ไฟล์เป็น Absolute Path
        config["input_file"] = os.path.join(base_dir, config["input_file"])
        config["output_file"] = os.path.join(base_dir, config["output_file"])

        if not os.path.exists(config["input_file"]):
            logger.critical(f"Input file not found: {config['input_file']}. Please create 'data/input_data.xlsx'")
            return

        agent = SpreadsheetAgent(config)
        agent.run()
        logger.info("Spreadsheet processing workflow completed.")

    except Exception as e:
        logger.critical(f"An unexpected error occurred: {e}", exc_info=True)

if __name__ == "__main__":
    main()