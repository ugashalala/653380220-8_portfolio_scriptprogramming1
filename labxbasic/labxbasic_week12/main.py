
import os
import sys
import time

from src.email_sender import EmailSender
from src.email_receiver import EmailReceiver
from src.sms_gateway import SMSGateway

from src.utils import (
    setup_logging,
    get_env_variable,
    ensure_directory_exists
)

logger = setup_logging(__name__)


def main():
    """Main function for email and SMS automation."""

    base_dir = os.path.dirname(os.path.abspath(__file__))

    data_dir = os.path.join(base_dir, "data")

    attachments_dir = os.path.join(
        data_dir,
        "attachments"
    )

    ensure_directory_exists(data_dir)
    ensure_directory_exists(attachments_dir)

    # Load credentials from environment variables
    try:
        sender_email = get_env_variable(
            "SENDER_EMAIL"
        )

        sender_app_password = get_env_variable(
            "SENDER_APP_PASSWORD"
        )

        smtp_server = get_env_variable(
            "SMTP_SERVER"
        )

        smtp_port = int(
            get_env_variable("SMTP_PORT")
        )

        imap_server = get_env_variable(
            "IMAP_SERVER"
        )

        test_recipient_email = get_env_variable(
            "TEST_RECIPIENT_EMAIL"
        )

        enable_sms = os.getenv(
            "ENABLE_SMS_TEST",
            "false"
        ).lower() == "true"

        if enable_sms:
            test_sms_phone_number = get_env_variable(
                "TEST_SMS_PHONE_NUMBER"
            )

            test_sms_carrier = get_env_variable(
                "TEST_SMS_CARRIER"
            )

    except ValueError as e:
        logger.critical(
            f"Configuration error: {e}. "
            "Please check your .env file."
        )
        sys.exit(1)

    # Initialize handlers
    email_sender = EmailSender(
        smtp_server,
        smtp_port,
        sender_email,
        sender_app_password
    )

    email_receiver = EmailReceiver(
        imap_server,
        sender_email,
        sender_app_password
    )

    sms_gateway = SMSGateway(email_sender)

    # -----------------------------------------
    # Task 1: Send a simple plaintext email
    # -----------------------------------------

    logger.info(
        "\n--- Task 1: Sending a simple plaintext email ---"
    )

    email_sender.send_email(
        recipient_email=test_recipient_email,
        subject="Automated Python Test Email",
        body=(
            "อัครพงษ์ ศรีโฉม 653380220-8 "
            "This is a plain text email."
        )
    )

    time.sleep(2)

    # -----------------------------------------
    # Task 2: Send email with attachment
    # -----------------------------------------

    logger.info(
        "\n--- Task 2: Sending an email with an attachment ---"
    )

    attachment_file_path = os.path.join(
        data_dir,
        "dummy_report.pdf"
    )

    if os.path.exists(attachment_file_path):
        email_sender.send_email(
            recipient_email=test_recipient_email,
            subject=(
                "Python Test Email with Attachment - Daily Report"
            ),
            body="อัครพงษ์ ศรีโฉม 653380220-8 ",
            attachment_path=attachment_file_path
        )

    else:
        logger.warning(
            f"Attachment file not found at "
            f"'{attachment_file_path}'. "
            "Skipping attachment email."
        )

    time.sleep(2)

    # -----------------------------------------
    # Task 3: Send SMS via email gateway
    # -----------------------------------------

    logger.info(
        "\n--- Task 3: Sending an SMS via email gateway ---"
    )

    if enable_sms:
        sms_message = (
            "Hello from Python! "
            "This is an automated SMS via email gateway."
        )

        sms_gateway.send_sms(
            phone_number=test_sms_phone_number,
            message=sms_message,
            carrier_name=test_sms_carrier
        )

        time.sleep(5)

    else:
        logger.info(
            "SMS test skipped. Set ENABLE_SMS_TEST=true "
            "in .env to enable this task."
        )

    # -----------------------------------------
    # Task 4: Receive and process emails
    # -----------------------------------------

    logger.info(
        "\n--- Task 4: Receiving and processing emails ---"
    )

    # Send an email to self for receiving demonstration
    demo_subject = "Python Test: Email for Receiving Demo"

    demo_sent = email_sender.send_email(
        recipient_email=sender_email,
        subject=demo_subject,
        body=(
            "อัครพงษ์ ศรีโฉม 653380220-8"
            "It has an attachment!"
        ),
        attachment_path=(
            attachment_file_path
            if os.path.exists(attachment_file_path)
            else None
        )
    )

    if not demo_sent:
        logger.error(
            "Could not send the receiving demo email."
        )
        return

    logger.info(
        "Sent a demo email to self. Waiting for delivery..."
    )

    time.sleep(10)

    # Search for unread emails from self
    uids = email_receiver.search_emails(
        criteria="UNSEEN",
        from_sender=sender_email,
        subject_contains=demo_subject
    )

    if uids:
        logger.info(
            f"Found {len(uids)} matching unread email(s)."
        )

        for uid in uids:
            uid_string = uid.decode("utf-8")

            logger.info(
                f"Processing email UID: {uid_string}"
            )

            email_details = email_receiver.fetch_email_content(
                uid=uid,
                mark_as_read=True,
                download_attachments_dir=attachments_dir
            )

            if email_details:
                logger.info(
                    f"Sender: {email_details['sender']}"
                )

                logger.info(
                    f"Subject: {email_details['subject']}"
                )

                logger.info(
                    f"Body Snippet: {email_details['body_snippet']}"
                )

                if email_details["attachments_downloaded"]:
                    logger.info(
                        "Attachments downloaded: "
                        + ", ".join(
                            email_details["attachments_downloaded"]
                        )
                    )

                else:
                    logger.info(
                        "No attachments downloaded for this email."
                    )

            else:
                logger.error(
                    f"Could not retrieve email UID: {uid_string}"
                )

    else:
        logger.info(
            "No matching unread emails found for receiving demo."
        )

    logger.info(
        "\n--- All communication automation tasks completed ---"
    )


if __name__ == "__main__":
    main()
