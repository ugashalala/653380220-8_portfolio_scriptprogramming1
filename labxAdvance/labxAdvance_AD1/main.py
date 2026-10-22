# agentic-web-scraper/main.py
import sys
import os
import logging

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from config_parser import ConfigParser
from scraper_agent import ScraperAgent

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    config_file_path = os.path.join(os.path.dirname(__file__), 'configs', 'example_site_config.json')
    try:
        config_parser = ConfigParser(config_file_path)
        config = config_parser.load_config()
        
        # ตั้งค่า headless=False หากต้องการเปิดเบราว์เซอร์จริงขึ้นมาดูการทำงานขณะ Debug
        scraper_agent = ScraperAgent(config, browser='chrome', headless=True)
        scraper_agent.run()

    except FileNotFoundError as e:
        logging.error(f"Configuration file error: {e}")
        logging.info("Please ensure 'configs/example_site_config.json' exists.")
    except ValueError as e:
        logging.error(f"Configuration validation error: {e}")
        logging.info("Please check the format and required fields in your config file.")
    except Exception as e:
        logging.critical(f"An unexpected error occurred during execution: {e}")

if __name__ == "__main__":
    main()