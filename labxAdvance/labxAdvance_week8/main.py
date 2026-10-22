# labxAdvance_week8/main.py
import sys
import os

# เพิ่มไดเรกทอรี 'src' เข้าสู่ Python Path เพื่อป้องกัน ModuleNotFoundError
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from config_parser import ConfigParser
from data_agent import DataAgent
from utils import setup_logging, ensure_directory_exists

logger = setup_logging(__name__)

def main():
    base_dir = os.path.dirname(__file__)
    config_file_path = os.path.join(base_dir, 'configs', 'data_pipeline_config.json')

    try:
        ensure_directory_exists(os.path.join(base_dir, 'data'))
        ensure_directory_exists(os.path.join(base_dir, 'configs'))
        ensure_directory_exists(os.path.join(base_dir, 'reports'))

        config_parser = ConfigParser(config_file_path)
        config = config_parser.load_config()

        # แปลงไฟล์ Path ใน Config ให้เป็น Absolute Path ป้องกันปัญหาไฟล์หาไม่พบ
        for task in config['tasks']:
            if 'file_path' in task:
                task['file_path'] = os.path.join(base_dir, task['file_path'])

        agent = DataAgent(config)
        agent.run()
        logger.info("Data automation process completed successfully.")

    except Exception as e:
        logger.critical(f"An error occurred: {e}", exc_info=True)

if __name__ == "__main__":
    main()