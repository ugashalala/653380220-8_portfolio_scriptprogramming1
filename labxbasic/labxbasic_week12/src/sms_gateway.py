
from .utils import setup_logging
from .email_sender import EmailSender

logger = setup_logging(__name__)


class SMSGateway:
    """
    Provides an interface to send SMS via email-to-SMS gateways.

    Note: Carrier gateway support must be verified before use.
    """

    def __init__(self, email_sender_instance):
        if not isinstance(email_sender_instance, EmailSender):
            raise TypeError(
                "SMSGateway requires an instance of EmailSender."
            )

        self.email_sender = email_sender_instance

        # Historical carrier gateway examples from the lab
        # Availability is not guaranteed.
        self.carrier_gateways = {
            "att": "@txt.att.net",
            "verizon": "@vtext.com",
            "tmobile": "@tmomail.net",
            "sprint": "@messaging.sprintpcs.com",
            "boost": "@sms.boostmobile.com",
            "cricket": "@mms.cricketwireless.net",
            "us_cellular": "@email.uscc.net"
        }

        logger.info("SMSGateway initialized.")

    def send_sms(
        self,
        phone_number,
        message,
        carrier_name=None
    ):
        """Sends an SMS via an email gateway."""

        sms_gateway_address = None

        if (
            carrier_name
            and carrier_name.lower() in self.carrier_gateways
        ):
            sms_gateway_address = (
                f"{phone_number}"
                f"{self.carrier_gateways[carrier_name.lower()]}"
            )

        elif "@" in phone_number and "." in phone_number:
            sms_gateway_address = phone_number

        else:
            logger.warning(
                "No valid carrier provided and phone number "
                "is not a full gateway address. Cannot send SMS."
            )
            return False

        subject = ""

        logger.info(
            f"Attempting to send SMS to {phone_number} "
            f"via gateway: {sms_gateway_address}"
        )

        return self.email_sender.send_email(
            recipient_email=sms_gateway_address,
            subject=subject,
            body=message
        )
