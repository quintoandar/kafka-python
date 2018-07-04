import json
import logging

from retrying import retry
from kafka.consumer.group import KafkaConsumer
from quintokafka.idempotence_client import RedisIdempotenceClient
from functools import partial


class KafkaSimpleConsumer():
    def __init__(self, processor, **kwargs):
        self.log = logging.getLogger(__name__)
        self.processor = processor
        if kwargs.get('value_deserializer') is None:
            kwargs['value_deserializer'] = self.__default_deserializer
        if kwargs.get('auto_offset_reset') is None:
            kwargs['auto_offset_reset'] = 'latest'
        self.consumer = self.__connect(kwargs)
        self.consumer.subscribe(kwargs['topic'])

    @retry(stop_max_attempt_number=10, wait_fixed=3000)
    def __connect(self, kwargs):
        return KafkaConsumer(kwargs)

    def __default_deserializer(self, m):
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


class KafkaIdempotentConsumer(KafkaSimpleConsumer):

    def __init__(self, redis_host, redis_port, processor,
                 idempotent_key, **kwargs):
        processor = partial(self.idempotent_processor, processor)
        super().__init__(processor, **kwargs)
        self.topic = kwargs['topic']
        self.idempotence_client = RedisIdempotenceClient(
            redis_host, redis_port, kwargs['group_id'],
            idempotent_key=idempotent_key)

    def idempotent_processor(self, processor, message):
        if not self.idempotence_client.is_unique(self.topic, message):
            return

        processor(message)

        self.idempotence_client.mark_consumed_message(self.topic, message)
