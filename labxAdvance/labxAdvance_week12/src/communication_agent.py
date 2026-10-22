# agentic-comm-automator/src/communication_agent.py
import os
import json
import datetime
from utils import setup_logging, log_audit_entry, ensure_directory_exists, get_env_variable
from email_tasks import EmailTasks
from sms_tasks import SMSTasks
from template_renderer import TemplateRenderer

logger = setup_logging(__name__)

class CommunicationAgent:
    """Core Agent for orchestrating email and SMS workflows."""
    def __init__(self, config, base_dir):
        self.config = config
        self.audit_log = []
        self.context = {}
        self.start_time = datetime.datetime.now()
        self.base_dir = base_dir

        sender_email = get_env_variable("SENDER_EMAIL")
        sender_app_password = get_env_variable("SENDER_APP_PASSWORD")
        smtp_server = get_env_variable("SMTP_SERVER")
        smtp_port = int(get_env_variable("SMTP_PORT"))
        imap_server = get_env_variable("IMAP_SERVER")

        self.email_tasks = EmailTasks(smtp_server, smtp_port, imap_server, sender_email, sender_app_password)
        self.sms_tasks = SMSTasks(self.email_tasks)
        self.template_renderer = TemplateRenderer()
        logger.info("CommunicationAgent initialized successfully.")

    def _update_context(self, key, value):
        self.context[key] = value

    def _render_template(self, template_string):
        return self.template_renderer.render(template_string, self.context)

    def _process_task(self, task):
        task_type = task.get("type")
        task_name = task.get("name", task_type)
        task_params = task.get("parameters", {})
        output_context_key = task.get("output_context_key")

        logger.info(f"Executing task: '{task_name}' ({task_type})")
        log_audit_entry(self.audit_log, "INFO", f"Starting task '{task_name}'", task_type)

        try:
            success = False
            task_output_data = None

            if task_type == "send_email":
                recipients = {k: [self._render_template(r) for r in v] for k, v in task_params.get('recipients', {}).items()}
                subject = self._render_template(task_params.get("subject_template", ""))
                body = self._render_template(task_params.get("body_template", ""))
                attachments = [os.path.join(self.base_dir, self._render_template(att)) for att in task_params.get("attachments", [])]
                is_html = task_params.get("is_html", False)

                success = self.email_tasks.send_email(recipients, subject, body, attachments, is_html)
                if success:
                    task_output_data = {"recipients": recipients, "subject": subject}

            elif task_type == "send_sms":
                phone_numbers = [self._render_template(p) for p in task_params.get("phone_numbers", [])]
                message = self._render_template(task_params.get("message_template", ""))
                carrier = self._render_template(task_params.get("carrier_name", ""))
                success = self.sms_tasks.send_sms(phone_numbers, message, carrier)

            elif task_type == "process_inbox":
                mailbox = task_params.get("mailbox", "INBOX")
                search_criteria = task_params.get("search_criteria", {})
                download_dir = os.path.join(self.base_dir, task_params.get("download_attachments_base_dir", "data/incoming_attachments"))

                rendered_sender = self._render_template(search_criteria.get("from_sender", "")) if search_criteria.get("from_sender") else None
                rendered_subject = self._render_template(search_criteria.get("subject_contains", "")) if search_criteria.get("subject_contains") else None

                uids = self.email_tasks.search_emails(mailbox, search_criteria.get("status", "UNSEEN"), rendered_sender, rendered_subject)
                for uid in uids:
                    email_info = self.email_tasks.fetch_email_content(uid, True, download_dir)
                    if email_info:
                        for rule in task_params.get("rules", []):
                            if_cond = rule.get("if", {})
                            then_act = rule.get("then", {})

                            match = True
                            if "subject_contains" in if_cond and if_cond["subject_contains"].lower() not in email_info["subject"].lower():
                                match = False

                            if match:
                                if then_act.get("send_sms_alert"):
                                    alert_msg = self.template_renderer.render(then_act.get("alert_message_template", ""), {**self.context, **email_info})
                                    alert_phones = [self._render_template(p) for p in then_act.get("alert_phone_numbers", [])]
                                    self.sms_tasks.send_sms(alert_phones, alert_msg, then_act.get("alert_carrier"))
                                if "reply_with_template" in then_act:
                                    reply_body = self.template_renderer.render(then_act["reply_with_template"], {**self.context, **email_info})
                                    reply_subj = "Re: " + email_info["subject"]
                                    self.email_tasks.send_email({'to': [email_info['sender']]}, reply_subj, reply_body)
                success = True

            if success:
                if task_output_data and output_context_key:
                    self._update_context(output_context_key, task_output_data)
                log_audit_entry(self.audit_log, "SUCCESS", f"Task '{task_name}' completed successfully.", task_type)
            else:
                log_audit_entry(self.audit_log, "ERROR", f"Task '{task_name}' failed.", task_type)
        except Exception as e:
            log_audit_entry(self.audit_log, "ERROR", f"Error during task '{task_name}': {e}", task_type)

    def generate_audit_report(self, output_dir="reports"):
        ensure_directory_exists(output_dir)
        report_filename = f"audit_report_comm_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        report_path = os.path.join(output_dir, report_filename)
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(self.audit_log, f, indent=4, ensure_ascii=False)
        logger.info(f"Audit report saved to: {report_path}")

    def run(self):
        logger.info("Starting Communication Agent run...")
        self._update_context("report_name", "DailySalesSummary")
        self._update_context("report_date", datetime.date.today().strftime("%Y-%m-%d"))
        self._update_context("sales_figure", 12345.67)
        self._update_context("total_customers", 500)

        for task in self.config.get("tasks", []):
            self._process_task(task)

        self.generate_audit_report(os.path.join(self.base_dir, 'reports'))