import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email(mail_content: str, subject: str, receivers: list, credentials: dict):
    """Send an e-mail with a given content and subject to one or more receivers. The credentials for the sender passed
    in parameter credentials.
    credentials = {
        "login": "sender@example.com",
        "password": "PASSWORD_SENDER_MAIL",
        "smtp_host": "SMTP_SERVER_ADDRESS",
        "smtp_port": "SMTP_SERVER_PORT"
    }
    Args:
        mail_content: Content of the email
        subject: Subject of the email
        receivers: A list of e-mail addresses which should receive the mail.
        credentials: A dictionary containing the credentials of the sender e-mail address.

    """

    # Setup MIME
    message = MIMEMultipart()
    message['From'] = credentials["login"]
    message['To'] = ', '.join(receivers)
    message['Subject'] = subject

    # The body and the attachments for the mail
    message.attach(MIMEText(mail_content, 'plain'))

    # Create SMTP session for sending the mail
    session = smtplib.SMTP(credentials["smtp_host"], credentials["smtp_port"])
    session.ehlo()
    session.starttls()
    session.ehlo()

    # Login with mail_id and password
    session.login(credentials["login"], credentials["password"])
    text = message.as_string()
    session.sendmail(credentials["login"], receivers, text)
    session.quit()
