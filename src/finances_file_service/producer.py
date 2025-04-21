import datetime
import json
from json import JSONEncoder

import aio_pika

from finances_file_service.logger import logger
from finances_file_service.params import get_rabbitmq_connection


class DatetimeEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        return super().default(obj)


ROUTING_KEY = "statement"


class RabbitMQProducer:
    def __init__(
        self, connection: aio_pika.Connection = None, channel: aio_pika.Channel = None
    ):
        if connection is None or channel is None:
            logger.error("RabbitMQ connection or channel is not provided!")
            raise ValueError(
                "RabbitMQ connection or channel is not provided! Use connect() method to establish a connection."
            )
        self.connection = connection
        self.channel = channel

    @staticmethod
    async def connect() -> "RabbitMQProducer":
        conn_url = get_rabbitmq_connection()

        connection = await aio_pika.connect_robust(conn_url)

        channel = await connection.channel()  # type: ignore

        logger.info("RabbitMQ connection established and channel created.")
        return RabbitMQProducer(connection, channel)

    async def send_message(self, message: dict):
        if self.connection is None or self.channel is None or self.channel.is_closed:
            logger.error(
                "RabbitMQ connection or channel is not established! Use connect() method to establish a connection."
            )
            raise ValueError(
                "RabbitMQ connection or channel is not established! Use connect() method to establish a connection."
            )

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

        await self.channel.default_exchange.publish(
            aio_pika.Message(
                body=message_json.encode("utf-8"),
                content_type="application/json",
            ),
            routing_key=ROUTING_KEY,
        )

    async def close(self):
        if self.connection:
            await self.connection.close()
            logger.info("RabbitMQ connection closed.")
        else:
            logger.error("RabbitMQ connection is not established!")


async def get_producer():
    producer = await RabbitMQProducer.connect()
    try:
        yield producer
    finally:
        logger.info("Closing RabbitMQ producer...")
        await producer.close()
