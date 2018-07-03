import json
import logging

from retrying import retry
from kafka.consumer.group import KafkaConsumer
from quintoandar_kafka import IdempotenceClient
from functools import partial


class KafkaDefaultConsumer():
    def __init__(self, processor, **kwargs):
        self.log = logging.getLogger(__name__)
        self.processor = processor
        if kwargs.get('deserializer') is None:
            kwargs['deserializer'] = self.default_deserializer
        if kwargs.get('auto_offset_reset') is None:
            kwargs['auto_offset_reset'] = 'latest'
        self.consumer = self.connect(kwargs)
        self.consumer.subscribe(kwargs['topic'])

    @retry(stop_max_attempt_number=10, wait_fixed=3000)
    def connect(self, kwargs):
        return KafkaConsumer(kwargs)

    def default_deserializer(self, m):
        try:
            return json.loads(m.decode('utf8'))
        except Exception as ex:
            self.log.error("Failed to decode message: %s", ex, exc_info=True)
            return {}

    def start(self):
        for message in self.consumer:
            if not message.value:
                continue

            self.processor(message)


class KafkaIdempotentConsumer(KafkaDefaultConsumer):

    def __init__(self, redis_host, redis_port, processor,
                 key_extractor, **kwargs):
        processor = partial(self.idempotent_processor, processor)
        super().__init__(processor, **kwargs)
        self.topic = kwargs['topic']
        self.idempotence_client = IdempotenceClient(
            redis_host, redis_port, kwargs['group_id'],
            key_extractor=key_extractor)

    def idempotent_processor(self, processor, message):
        if not self.idempotence_client.is_unique(self.topic, message):
            return

        processor(message)

        self.idempotence_client.mark_consumed_message(self.topic, message)
