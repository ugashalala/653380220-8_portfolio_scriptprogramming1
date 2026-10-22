# agentic-comm-automator/src/template_renderer.py
import string
import os
from utils import setup_logging

logger = setup_logging(__name__)

class TemplateRenderer:
    """A simple template renderer for string templates using Python's format syntax."""
    def __init__(self):
        logger.info("TemplateRenderer initialized.")

    def render(self, template_string, context):
        if not template_string:
            return ""
        try:
            # แทนที่ตัวแปรสภาพแวดล้อมที่ระบุในรูปแบบ ${VAR_NAME} ก่อน
            rendered = template_string
            for key, val in os.environ.items():
                rendered = rendered.replace(f"${{{key}}}", str(val))
            
            # จากนั้นทำการ Format ด้วย Context Dictionary
            return rendered.format(**context)
        except KeyError as e:
            logger.error(f"Missing key in template context: {e}. Template: '{template_string}'")
            return template_string
        except Exception as e:
            logger.error(f"Error rendering template: {e}")
            return template_string