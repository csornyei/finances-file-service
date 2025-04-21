import pika
import json
import datetime
from json import JSONEncoder

from finances_file_service.logger import logger


class DatetimeEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        return super().default(obj)


class RabbitMQProducer:
    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host="localhost",
                credentials=pika.PlainCredentials("rabbitmq", "rabbitmq"),
            )
        )
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue="statement", durable=True)

    def send_message(self, message: dict):
        message_json = json.dumps(message, cls=DatetimeEncoder)
        logger.info(
            json.dumps(
                {
                    "message": message_json,
                    "status": "sending",
                    "queue": "statement",
                }
            )
        )

        self.channel.basic_publish(
            exchange="",
            routing_key="statement",
            body=json.dumps(message_json),
            properties=pika.BasicProperties(
                delivery_mode=2  # Make message persistent
            ),
        )

    def close(self):
        self.connection.close()


instance: RabbitMQProducer = None


def get_rabbitmq_producer() -> RabbitMQProducer:
    """
    Get the RabbitMQ producer instance.
    """
    global instance
    if instance is None:
        instance = RabbitMQProducer()
    return instance
