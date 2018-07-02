import redis
import logging


class IdempotenceClient:
    def __init__(self, host, port, group_id, db=0,
                 expire=14 * 24 * 3600, key_extractor=None):
        self.redis = redis.StrictRedis(host=host, port=port, db=db)
        self.group_id = group_id
        self.expire = expire  # default 2 weeks
        self.log = logging.getLogger(__name__)
        self.key_extractor = key_extractor

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
        if self.key_extractor:
            key = self.key_extractor(message)
        return '{}-{}-{}'.format(topic, self.group_id,
                                 hash(str(key)))
