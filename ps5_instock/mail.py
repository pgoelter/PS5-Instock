import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email(mail_content: str, subject: str, receivers: list, credentials: dict):
    """

    :param mail_content: The content of the mail.
    :param subject: The subject of the mail.
    :param receivers: List of receivers for the mail.
    :param credentials: Contains the keys sender and password, which in return contain the sender mail adress and the
    corresponding password.
    :return:
    """

    # The mail addresses and password
    sender_address = 'notifier.dev.saar@gmail.com'
    sender_pass = 'qrbhtriwjfxndrup'
    receiver_address = 'pgoelter@gmail.com'

    # Setup MIME
    message = MIMEMultipart()
    message['From'] = credentials["login"]
    message['To'] = ', '.join(receivers)
    message['Subject'] = subject

    # The body and the attachments for the mail
    message.attach(MIMEText(mail_content, 'plain'))

    # Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587)
    session.ehlo()
    session.starttls()
    session.ehlo()

    # Login with mail_id and password
    session.login(sender_address, credentials["password"])
    text = message.as_string()
    session.sendmail(sender_address, receivers, text)
    session.quit()
