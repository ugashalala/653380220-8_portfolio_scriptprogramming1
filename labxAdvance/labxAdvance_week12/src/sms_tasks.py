# agentic-comm-automator/src/sms_tasks.py
from utils import setup_logging
from email_tasks import EmailTasks
from template_renderer import TemplateRenderer

logger = setup_logging(__name__)

class SMSTasks:
    """Provides a simplified interface to send SMS via email-to-SMS gateways."""
    def __init__(self, email_tasks_instance):
        if not isinstance(email_tasks_instance, EmailTasks):
            raise TypeError("SMSTasks requires an instance of EmailTasks.")
        self.email_tasks = email_tasks_instance
        self.template_renderer = TemplateRenderer()
        self.carrier_gateways = {
            "att": "@txt.att.net",
            "verizon": "@vtext.com",
            "tmobile": "@tmomail.net",
            "sprint": "@messaging.sprintpcs.com"
        }
        logger.info("SMSTasks initialized.")

    def send_sms(self, phone_numbers, message, carrier_name=None):
        success_count = 0
        for phone_number in phone_numbers:
            gateway_addr = None
            if carrier_name and carrier_name.lower() in self.carrier_gateways:
                gateway_addr = f"{phone_number}{self.carrier_gateways[carrier_name.lower()]}"
            elif '@' in phone_number:
                gateway_addr = phone_number

            if gateway_addr:
                logger.info(f"Sending SMS to {phone_number} via {gateway_addr}")
                if self.email_tasks.send_email({'to': [gateway_addr]}, "", message):
                    success_count += 1
        return success_count == len(phone_numbers)