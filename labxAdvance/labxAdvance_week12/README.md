
# Week 22: Agentic Communication Workflows (Advanced Email &amp; SMS)

This project introduces an &quot;Agentic Communication Automator&quot; that executes complex email
and SMS workflows defined declaratively in a JSON configuration file. It extends basic
sending/receiving capabilities to include dynamic content generation, rule-based inbox
processing, and contextual data flow between tasks.

## Key Concepts Demonstrated

* **Communication Agent**: The `CommunicationAgent` orchestrates a sequence of
  communication tasks from a `comm_pipeline_config.json`.
* **Contextual Data Flow**: The agent maintains an internal `context` dictionary (`self.context`) that
  stores dynamic information (e.g., simulated report details, results of previous tasks). This

context is used to populate templates for subjects, bodies, and messages.

* **Dynamic Content Templating**: Email subjects, bodies, and SMS messages can be defined
  as templates with placeholders (e.g., `{report_date}`, `{sales_figure}`). The `TemplateRenderer`
  populates these from the agent&#39;s `context`.
* **Advanced Email Sending**:
* Sending emails with multiple recipients (To, CC).
* Attaching multiple files whose paths can be dynamic or static.
* **Rule-Based Inbox Processing**:
* The agent connects to an IMAP server and searches for emails based on flexible criteria
  (sender, subject, status).
* It then applies a list of &quot;if-then&quot; rules to each fetched email.
* **Conditions**: `subject_contains`, `body_contains`, `has_attachments`.
* **Actions**: `download_attachments_to` a specified directory, `mark_as_read`, `send_sms_alert`
  to specified numbers with a dynamic message, `reply_with_template` to the sender.
* **Secure Credential Handling**: All sensitive information (email, app password) is loaded from a
  `.env` file, ensuring it&#39;s never hardcoded or committed to version control.
* **Modular Design**: Code is logically separated into `email_tasks.py` (SMTP/IMAP),
  `sms_tasks.py` (SMS gateways), `template_renderer.py`, `config_parser.py`, and `utils.py`.
* **Comprehensive Logging &amp; Auditing**: Detailed logs are printed to the console and a JSON
  audit report is generated, tracking every step, success, and failure of the agent&#39;s workflow.

## Setup &amp; How to Run

1. **Clone the repository:**

```bash
git clone [https://github.com/YOUR_USERNAME/agentic-comm-
automator.git](https://github.com/YOUR_USERNAME/agentic-comm-automator.git)
cd agentic-comm-automator
```

2. **Install Dependencies:**
   This project primarily uses built-in Python modules (`smtplib`, `imaplib`, `email`). The only external
   dependency is `python-dotenv`.

```bash
python -m venv venv
source venv/bin/activate # On Windows: venv\Scripts\activate.bat
pip install python-dotenv
```

3. **Prepare Input Data Files:**

* Create the necessary directories:

```bash
mkdir -p data/reports data/incoming_attachments
```

* **`data/reports/sales_report.pdf`**: Create any simple PDF file and save it here. This will be used as a
  sample attachment to send.
* **`data/reports/summary_data.xlsx`**: Create any simple Excel (or similar) file and save it here. This
  will be used as another sample attachment to send.

4. **Configure Environment Variables (`.env` file):**

* In the root directory of your project, create a file named `.env`.
* **DO NOT COMMIT THIS FILE TO GITHUB OR ANY PUBLIC REPOSITORY!**
* Populate it with your email credentials and test recipient information:

```ini
# .env
SENDER_EMAIL=your_gmail_address@gmail.com
SENDER_APP_PASSWORD=your_generated_gmail_app_password
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
IMAP_SERVER=imap.gmail.com
# Recipient for test emails and SMS
TEST_RECIPIENT_EMAIL=another_email@example.com
TEST_SMS_PHONE_NUMBER=1234567890
TEST_SMS_CARRIER=att # or verizon, tmobile, sprint, boost, us_cellular, cricket, etc.
```

* **Important for Gmail Users:** If you have 2-Step Verification (2FA) enabled (highly
  recommended), you **must** generate an &quot;App password&quot; for your Python script to log in. Your
  regular Gmail password will *not* work for programmatic access.
* Go to your Google Account -&gt; &quot;Security&quot; -&gt; &quot;How you sign in to Google&quot; -&gt; &quot;App
  passwords&quot;.
* Follow the instructions to generate a new app password. Use this password for
  `SENDER_APP_PASSWORD`.
* If you *do not* have 2FA, you might need to enable &quot;Less secure app access&quot; in your
  Google Account settings, but this is **not recommended** for security reasons. Enable 2FA and
  use an App Password instead.

5. **Review `configs/comm_pipeline_config.json`:**

* This file defines the entire communication workflow.
* Ensure that the `file_path` entries for attachments (if any) correctly point to your created files,
  relative to the project root.
* Modify recipient emails and phone numbers to match your `TEST_RECIPIENT_EMAIL` and
  `TEST_SMS_PHONE_NUMBER` from the `.env` file.
* Feel free to experiment with the `subject_template`, `body_template`, `message_template`,
  search `criteria`, and `rules`.

6. **Run the script:**

```bash
python main.py
```

The script will execute the pipeline defined in `comm_pipeline_config.json`:

* **Send a dynamic email**: Uses the agent&#39;s context (`report_date`, `sales_figure`, `total_customers`)
  and attachments.
* **Send a dynamic SMS**: Uses the same context for the message.
* **Simulate Incoming Email**: Sends an email to your own `SENDER_EMAIL` account with a specific

subject and attachment. This is to create an email for the `process_inbox` task to find.

* **Process Inbox**:
* Searches your inbox for unread emails with &quot;Data Request&quot; in the subject and from your
  `SENDER_EMAIL`.
* When found, it applies rules:
* If the subject contains &quot;Urgent&quot; AND it has attachments, it sends an SMS alert.
* If the body contains &quot;new data processing&quot;, it sends an automated reply email.
* Attachments from processed emails are downloaded to `data/incoming_attachments/`.
* A detailed `audit_report_comm_*.json` will be generated in the `reports/` directory.

## Project Structure

agentic-comm-automator/
├── src/
│ ├── init.py # Python package marker
│ ├── communication_agent.py # Core agent logic: orchestrates tasks and manages context
│ ├── email_tasks.py # Logic for sending/receiving emails (SMTP/IMAP)
│ ├── sms_tasks.py # Logic for sending SMS via email gateways
│ ├── config_parser.py # Loads and validates the JSON pipeline configuration
│ ├── template_renderer.py # Simple utility for rendering string templates
│ └── utils.py # Logging, env var loading, directory helpers
├── configs/
│ └── comm_pipeline_config.json # The declarative JSON configuration for the communication
pipeline
├── data/
│ ├── attachments/ # Directory for general attachments (e.g., from generated reports)
│ ├── reports/ # Directory for simulated generated reports
│ │ ├── sales_report.pdf # Sample PDF (YOU CREATE)
│ │ └── summary_data.xlsx # Sample Excel (YOU CREATE)
│ └── incoming_attachments/ # Directory where attachments from processed emails are
downloaded
├── .env # Environment variables for sensitive credentials (YOU CREATE &amp; DO NOT
COMMIT)
├── main.py # Application entry point
├── .gitignore # Files/folders to ignore in Git
└── README.md # This project overview

## Debugging Agentic Communication Workflows

* **`ValueError: Environment variable &#39;...&#39; not set`**: Ensure your `.env` file exists in the root
  directory and all required variables (`SENDER_EMAIL`, `SENDER_APP_PASSWORD`, etc.)

are correctly set.

* **`SMTPAuthenticationError` / `IMAP4.error`**:
* **Crucial:** Confirm you are using an **App password** for Gmail, not your regular
  password. See `.env` setup instructions.
* Verify `SMTP_SERVER`, `SMTP_PORT`, `IMAP_SERVER` in `.env` are correct (e.g., for
  Gmail: `smtp.gmail.com`, `587`, `imap.gmail.com`).
* Check your internet connection and firewall settings.
* **Emails/SMS not sending/receiving as expected**:
* **Review `comm_pipeline_config.json`**:
* **Typos**: Any typo in `type`, `name`, `parameters` keys, or template placeholders
  (`{report_date}`).
* **Recipient/Phone Number**: Are `TEST_RECIPIENT_EMAIL` and
  `TEST_SMS_PHONE_NUMBER` correct in your `.env` and referenced properly in the config?
* **Attachment Paths**: Are paths in `attachments` correct and relative to the project root
  (`data/reports/...`)? Do the files actually exist?
* **Inbox Processing Rules**: Are the `search_criteria` (sender, subject, status) specific
  enough to find your test emails? Are the `if` conditions accurate (e.g., `subject_contains`,
  `body_contains`, `has_attachments`)?
* **Check Console Logs**: The `setup_logging` in `utils.py` provides detailed output. Look for
  `ERROR` or `WARNING` messages.
* **Check Audit Report**: The `reports/audit_report_comm_*.json` provides a chronological
  log of what the agent attempted and its status. This is invaluable for debugging workflow logic.
* **Template Rendering Issues (`KeyError`)**: If a placeholder like `{missing_key}` is in your
  template but not in the agent&#39;s `context` or the current `email_info` (for `process_inbox` actions),
  a `KeyError` will occur. Ensure all dynamic values are available in the context.
* **SMS Delivery**: Email-to-SMS gateways can be unreliable and messages might be filtered
  as spam. Test with small, simple messages first.

## Extension Ideas (Future Work)

* **Integrate with Data Agent (Week 20)**: Chain the `CommunicationAgent` with the
  `DataAgent`. The `DataAgent` could generate a report (`.pdf`, `.xlsx`) and save its path into a
  shared context, which the `CommunicationAgent` then uses to attach and email the report.
* **External Event Triggers**: Instead of just running `main.py` manually, use tools like
  `watchdog` to monitor a folder for new files, or integrate with a webhook listener that triggers
  agent tasks upon receiving specific HTTP requests.
* **Database Integration**: Store email history, received email metadata, or dynamically
  generated content in a database for long-term tracking and querying.
* **Advanced Templating**: Replace the simple `TemplateRenderer` with a more powerful
  templating engine like [Jinja2](https://jinja.palletsprojects.com/) for more complex email layouts
  (e.g., HTML emails with tables, loops).
* **Natural Language Processing (NLP)**: Use NLP libraries (e.g., `spaCy`, `NLTK`) within
  `process_inbox` rules to analyze email content for sentiment, keywords, or intent, triggering
  more intelligent actions.
* **Custom Action Modules**: Allow the configuration to specify custom Python functions or
  scripts to run as `then` actions in `process_inbox` rules, enabling highly specific automations.
* **User Interface**: Develop a simple web-based UI (e.g., with Flask or Streamlit) to manage
  configurations, view audit logs, and trigger agent runs.
* **Reply Threading**: Implement logic to reply to emails within their existing threads for better
  conversation management.

---

แหล่งที่มา

1. https://github.com/Cernurt/INF876_Automne2023
2. https://www.metaltoad.com/blog/aws-codewhisperer-ml-augmented-development-3-3
3. https://github.com/B2B-GJR-Nestle/B2BEmailBlast
