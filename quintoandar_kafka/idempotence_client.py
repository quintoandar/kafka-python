import redis
import logging


class IdempotenceClient:
    def mark_consumed_message(self, topic, message):
        pass

    def is_unique(self, topic, message):
        pass


class RedisIdempotenceClient(IdempotenceClient):
    def __init__(
        self, host, port, group_id, db=0, expire=14 * 24 * 3600, idempotent_key=None
    ):
        self.redis = redis.StrictRedis(host=host, port=port, db=db)
        self.group_id = group_id
        self.expire = expire  # default 2 weeks
        self.log = logging.getLogger(__name__)
        self.idempotent_key = idempotent_key

    def mark_consumed_message(self, topic, message):
        try:
            key = self.format_key(topic, message)
            self.redis.set(key, 1, ex=self.expire)
        except Exception as e:
            self.log.warn(e)

    def is_unique(self, topic, message):
        try:
            key = self.format_key(topic, message)
            result = self.redis.get(key)
            if result is not None:
                return False
            else:
                return True
        except Exception as e:
            self.log.warn(e)
            return True

    def format_key(self, topic, message):
        key = message
        if self.idempotent_key:
            key = self.idempotent_key(message)
        return "{}-{}-{}".format(topic, self.group_id, hash(str(key)))
