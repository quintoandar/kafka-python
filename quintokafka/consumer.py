import logging

from kafka.consumer.group import KafkaConsumer
from quintokafka.idempotence_client import RedisIdempotenceClient


class KafkaSimpleConsumer(KafkaConsumer):
    def __init__(self, *topics, **kwargs):
        self.log = logging.getLogger(__name__)
        if kwargs.get('value_deserializer') is None:
            kwargs['value_deserializer'] = lambda m: m.decode('utf8')
        if kwargs.get('auto_offset_reset') is None:
            kwargs['auto_offset_reset'] = 'latest'
        super().__init__(*topics, **kwargs)


class KafkaIdempotentConsumer(KafkaSimpleConsumer):

    def __init__(self, *topics, **kwargs):
        self.idempotence_client = RedisIdempotenceClient(
            kwargs['redis_host'], kwargs['redis_port'], kwargs['group_id'],
            idempotent_key=kwargs['idempotent_key'])
        del kwargs['redis_host']
        del kwargs['redis_port']
        del kwargs['idempotent_key']
        super().__init__(*topics, **kwargs)

    def __next__(self):
        msg = super().__next__()
        while not self.idempotence_client.is_unique(msg.topic, msg):
            msg = super().__next__()
        self.idempotence_client.mark_consumed_message(msg.topic, msg)
        return msg
