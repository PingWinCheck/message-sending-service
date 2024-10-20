from settings import settings
from pydantic import EmailStr
from smtplib import SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from logs_base import get_logger

log = get_logger()


def create_message(to: EmailStr, subject: str, body: str, from_name: str | None = None) -> MIMEMultipart:
    message = MIMEMultipart()
    if from_name:
        message['From'] = f'{from_name} <{settings.smtp.smtp_login}>'
    else:
        message['From'] = settings.smtp.smtp_login
    message['To'] = to
    message['Subject'] = subject
    message.attach(MIMEText(body))
    log.info('Message created')
    return message


def send_message(message: MIMEMultipart) -> bool:
    try:
        with SMTP(host=settings.smtp.smtp_server, port=settings.smtp.smtp_port) as server:
            log.debug('Connect to smtp server %s', server)
            server.starttls()
            log.debug('Server starttls')
            server.login(user=settings.smtp.smtp_login, password=settings.smtp.smtp_pass)
            log.debug('Server login')
            server.send_message(message)
            log.info('Message sended.')
    except Exception as e:
        log.error('Exception send_message %s', e)
        return False
    return True
