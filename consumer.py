import pika
from typing import TYPE_CHECKING

from settings import settings
from logs_base import get_logger
from send_mail import create_message, send_message
from schemas import MailMassageSchema

log = get_logger()

if TYPE_CHECKING:
    from pika.adapters.blocking_connection import BlockingChannel
    from pika.spec import BasicProperties, Basic


def get_blocked_connection() -> pika.BlockingConnection:
    return pika.BlockingConnection(
        parameters=pika.ConnectionParameters(host=settings.rmq.rmq_host,
                                             port=settings.rmq.rmq_port,
                                             credentials=pika.PlainCredentials(username=settings.rmq.rmq_user,
                                                                               password=settings.rmq.rmq_pass))
    )


def consumer(channel: 'BlockingChannel'):
    def task(ch: 'BlockingChannel',
             method: 'Basic.Deliver',
             properties: 'BasicProperties',
             body: bytes):
        mail = MailMassageSchema.model_validate_json(body)
        msg = create_message(to=mail.to,
                             subject=mail.subject,
                             body=mail.body,
                             from_name=mail.from_name)
        if send_message(msg):
            ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.queue_declare(settings.rmq.queue)
    channel.basic_consume(queue=settings.rmq.queue, on_message_callback=task)
    channel.start_consuming()


def start_consumer():
    with get_blocked_connection() as connection:
        log.info('Created blocking connection: %s', connection)
        with connection.channel() as channel:
            log.info('created blocked channel: %s', channel)
            consumer(channel=channel)


if __name__ == '__main__':
    start_consumer()
