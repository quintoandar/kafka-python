import json
import logging
from retrying import retry

from kafka.consumer.group import KafkaConsumer
from quintoandar_kafka.idempotence_client import RedisIdempotenceClient


class KafkaSimpleConsumer(KafkaConsumer):
    def __init__(self, *topics, **kwargs):
        self.log = logging.getLogger(__name__)
        if kwargs.get("value_deserializer") is None:
            kwargs["value_deserializer"] = lambda m: m.decode("utf8")
        if kwargs.get("auto_offset_reset") is None:
            kwargs["auto_offset_reset"] = "latest"
        super().__init__(*topics, **kwargs)


class KafkaIdempotentConsumer(KafkaSimpleConsumer):
    def __init__(self, *topics, **kwargs):
        self.idempotence_client = RedisIdempotenceClient(
            kwargs["redis_host"],
            kwargs["redis_port"],
            kwargs["group_id"],
            idempotent_key=kwargs["idempotent_key"],
        )
        del kwargs["redis_host"]
        del kwargs["redis_port"]
        del kwargs["idempotent_key"]
        super().__init__(*topics, **kwargs)

    def __next__(self):
        msg = super().__next__()
        while not self.idempotence_client.is_unique(msg.topic, msg):
            msg = super().__next__()
        self.idempotence_client.mark_consumed_message(msg.topic, msg)
        return msg


class KafkaConsumer:
    def __init__(
        self, redis_host, redis_port, group_id, bootstrap_servers, topic, idempotent_key
    ):
        self.log = logging.getLogger(__name__)
        self.consumer = self._connect(
            redis_host, redis_port, group_id, bootstrap_servers, idempotent_key
        )
        self.consumer.subscribe(topic)

    @retry(stop_max_attempt_number=10, wait_fixed=3000)
    def _connect(
        self, redis_host, redis_port, group_id, bootstrap_servers, idempotent_key
    ):
        return KafkaIdempotentConsumer(
            redis_host=redis_host,
            redis_port=redis_port,
            idempotent_key=idempotent_key,
            value_deserializer=self._deserializer,
            group_id=group_id,
            bootstrap_servers=bootstrap_servers,
            auto_offset_reset="latest",
        )

    def _deserializer(self, m):
        try:
            return json.loads(m.decode("utf8"))
        except TypeError as ex:
            self.log.error("Failed to decode message: %s", ex, exc_info=True)
            return {}

    def read(self, event_processor_tuples):
        for message in self.consumer:
            if not message.value:
                continue

            self.log.info(message)

            for (event, processor) in event_processor_tuples:
                # skip
                if message.value.get("eventName") != event:
                    continue

                try:
                    processor(message.value)
                except Exception as ex:
                    self.log.error("Error processing message: %s", ex, exc_info=True)
