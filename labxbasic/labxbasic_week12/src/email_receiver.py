
import imaplib
import email
import os

from email.header import decode_header
from pathlib import Path

from .utils import setup_logging, ensure_directory_exists

logger = setup_logging(__name__)


class EmailReceiver:
    """Handles receiving and parsing emails via IMAP."""

    def __init__(self, imap_server, sender_email, sender_password):
        self.imap_server = imap_server
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.mail = None

        logger.info(
            f"EmailReceiver initialized for {sender_email} "
            f"via {imap_server}."
        )

    def _connect(self):
        """Establishes and logs into the IMAP server."""
        try:
            self.mail = imaplib.IMAP4_SSL(
                self.imap_server,
                timeout=30
            )

            self.mail.login(
                self.sender_email,
                self.sender_password
            )

            logger.info(
                "Successfully connected and logged into IMAP server."
            )
            return True

        except imaplib.IMAP4.error as e:
            logger.error(
                f"IMAP authentication failed. Error: {e}"
            )

        except Exception as e:
            logger.error(
                f"An unexpected error occurred during IMAP connect: {e}"
            )

        self._disconnect()
        return False

    def _disconnect(self):
        """Disconnects from the IMAP server."""
        if self.mail:
            try:
                self.mail.logout()
                logger.info("Disconnected from IMAP server.")

            except Exception as e:
                logger.warning(
                    f"Error during IMAP disconnection: {e}"
                )

            finally:
                self.mail = None

    def search_emails(
        self,
        mailbox="INBOX",
        criteria="UNSEEN",
        from_sender=None,
        subject_contains=None
    ):
        """Searches for emails and returns their UIDs."""

        if not self._connect():
            return []

        try:
            status, _ = self.mail.select(mailbox)

            if status != "OK":
                logger.error(f"Cannot select mailbox: {mailbox}")
                return []

            search_query = [criteria]

            if from_sender:
                search_query.extend([
                    "FROM",
                    f'"{from_sender}"'
                ])

            if subject_contains:
                search_query.extend([
                    "SUBJECT",
                    f'"{subject_contains}"'
                ])

            status, email_ids = self.mail.uid(
                "SEARCH",
                None,
                *search_query
            )

            if status != "OK":
                logger.error(
                    f"IMAP search failed. Status: {status}"
                )
                return []

            uids = email_ids[0].split()

            logger.info(
                f"Found {len(uids)} emails matching criteria "
                f"in '{mailbox}'."
            )

            return uids

        except Exception as e:
            logger.error(f"Error searching emails: {e}")
            return []

        finally:
            self._disconnect()

    def fetch_email_content(
        self,
        uid,
        mark_as_read=True,
        download_attachments_dir=None
    ):
        """Fetches an email using its UID."""

        if not self._connect():
            return None

        try:
            status, _ = self.mail.select("INBOX")

            if status != "OK":
                logger.error("Cannot select INBOX.")
                return None

            # Fetch email using UID
            status, msg_data = self.mail.uid(
                "FETCH",
                uid,
                "(BODY.PEEK[])"
            )

            if status != "OK":
                logger.error(
                    f"Failed to fetch email UID {uid}."
                )
                return None

            raw_email = None

            for item in msg_data:
                if isinstance(item, tuple):
                    raw_email = item[1]
                    break

            if raw_email is None:
                logger.error("No email content returned.")
                return None

            msg = email.message_from_bytes(raw_email)

            sender = self._decode_header_part(
                msg.get("From")
            )

            subject = self._decode_header_part(
                msg.get("Subject")
            )

            email_body = ""
            attachments_downloaded = []

            for part in msg.walk():
                content_type = part.get_content_type()

                content_disposition = str(
                    part.get("Content-Disposition", "")
                )

                # Download attachments
                if "attachment" in content_disposition.lower():
                    filename = part.get_filename()

                    if filename and download_attachments_dir:
                        filename = self._decode_header_part(
                            filename
                        )

                        # Prevent writing outside the attachment folder
                        filename = os.path.basename(
                            filename.replace("\\", "/")
                        )

                        if not filename:
                            continue

                        ensure_directory_exists(
                            download_attachments_dir
                        )

                        filepath = os.path.join(
                            download_attachments_dir,
                            filename
                        )

                        # Avoid overwriting an existing file
                        path = Path(filepath)
                        counter = 1

                        while path.exists():
                            path = Path(
                                download_attachments_dir
                            ) / (
                                f"{Path(filename).stem}_{counter}"
                                f"{Path(filename).suffix}"
                            )
                            counter += 1

                        try:
                            payload = part.get_payload(
                                decode=True
                            )

                            if payload is None:
                                continue

                            with open(path, "wb") as f:
                                f.write(payload)

                            attachments_downloaded.append(
                                str(path)
                            )

                            logger.info(
                                f"Downloaded attachment: {path}"
                            )

                        except Exception as e:
                            logger.error(
                                f"Error downloading attachment: {e}"
                            )

                # Extract plain text body
                elif (
                    content_type == "text/plain"
                    and "attachment" not in content_disposition.lower()
                ):
                    try:
                        payload = part.get_payload(
                            decode=True
                        )

                        if payload:
                            charset = (
                                part.get_content_charset()
                                or "utf-8"
                            )

                            email_body += payload.decode(
                                charset,
                                errors="replace"
                            )

                    except Exception as e:
                        logger.warning(
                            f"Could not decode email body: {e}"
                        )

                elif content_type == "text/html":
                    # Plain text is prioritized
                    pass

            # Mark email as read
            if mark_as_read:
                self.mail.uid(
                    "STORE",
                    uid,
                    "+FLAGS",
                    r"(\Seen)"
                )

                logger.info(
                    f"Marked email UID {uid} as read."
                )

            uid_string = (
                uid.decode("utf-8")
                if isinstance(uid, bytes)
                else str(uid)
            )

            return {
                "uid": uid_string,
                "sender": sender,
                "subject": subject,
                "body_snippet": (
                    email_body[:200] + "..."
                    if len(email_body) > 200
                    else email_body
                ),
                "attachments_downloaded": attachments_downloaded
            }

        except Exception as e:
            logger.error(
                f"Error fetching/parsing email UID {uid}: {e}"
            )
            return None

        finally:
            self._disconnect()

    def _decode_header_part(self, header_value):
        """Decodes email headers."""

        if header_value is None:
            return ""

        decoded_parts = decode_header(header_value)
        decoded_string = ""

        for part, charset in decoded_parts:
            if isinstance(part, bytes):
                try:
                    decoded_string += part.decode(
                        charset or "utf-8",
                        errors="replace"
                    )

                except (LookupError, UnicodeError):
                    decoded_string += part.decode(
                        "latin-1",
                        errors="replace"
                    )

            else:
                decoded_string += part

        return decoded_string.strip()
