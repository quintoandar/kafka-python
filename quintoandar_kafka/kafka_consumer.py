import json
import logging

from retrying import retry
from kafka.consumer.group import KafkaConsumer


class KafkaConsumerClient:

    def __init__(self, group_id, bootstrap_servers, topic,
                 processor, deserializer=None, idempotence_client=None):
        self.log = logging.getLogger(__name__)
        self.topic = topic
        self.processor = processor
        self.deserializer = deserializer or self.default_deserializer
        self.idempotence_client = idempotence_client or\
            DefaultIdempotenceClient()
        self.consumer = self.connect(group_id, bootstrap_servers)
        self.consumer.subscribe(topic)

    @retry(stop_max_attempt_number=10, wait_fixed=3000)
    def connect(self, group_id, bootstrap_servers):
        return KafkaConsumer(
            value_deserializer=self.deserializer,
            group_id=group_id,
            bootstrap_servers=bootstrap_servers,
            auto_offset_reset='latest')

    def start(self):
        for message in self.consumer:
            if not message.value:
                continue

            if not self.idempotence_client.is_unique(self.topic, message):
                continue

            self.processor(message)

            self.idempotence_client.mark_consumed_message(self.topic, message)

    def default_deserializer(self, m):
        try:
            return json.loads(m.decode('utf8'))
        except Exception as ex:
            self.log.error("Failed to decode message: %s", ex, exc_info=True)
            return {}


class DefaultIdempotenceClient:

    def is_unique(self, topic, message):
        return True

    def mark_consumed_message(self, topic, message):
        pass
