import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from celery import Celery

from app.settings import settings

celery = Celery(__name__)
celery.conf.broker_url = settings.celery_broker_url
celery.conf.result_backend = settings.celery_broker_url

celery.conf.update(
    # broker_use_ssl=settings.ssl_options,
    # redis_backend_use_ssl=settings.ssl_options,
    task_serializer='json',
    result_serializer='json',
    accept_content=['json'],
    enable_utc=True,  # Убедитесь, что UTC включен
    timezone='Europe/Moscow',  # Устанавливаем московское время
    broker_connection_retry_on_startup=True,
    task_acks_late=True,
    task_reject_on_worker_lost=True,
)


@celery.task(name='send_email_task')
def send_email_task(subject: str, text: str, to: str):
    msg = _build_message(subject, text, to)
    _send_email(msg=msg)


def _build_message(subject: str, text: str, to: str) -> MIMEMultipart:
    msg = MIMEMultipart()

    msg['From'] = settings.from_email
    msg['To'] = to
    msg['Subject'] = subject
    msg.attach(MIMEText(text, 'plain'))
    return msg


def _send_email(msg: MIMEMultipart) -> None:
    context = ssl.create_default_context()
    server = smtplib.SMTP_SSL(settings.smtp_host, settings.smtp_port, context=context)
    server.login(settings.from_email, settings.smtp_password)
    server.send_message(msg)
    server.quit()
