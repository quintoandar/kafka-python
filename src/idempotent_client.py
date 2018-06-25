import redis
import logging


class IdempotentClient:
    def __init__(self, host, port, groupId, db=0, expire=14 * 24 * 3600):
        self.redis = redis.StrictRedis(host=host, port=port, db=db)
        self.groupId = groupId
        self.expire = expire  # default 2 weeks
        self.log = logging.getLogger(__name__)

    def markConsumedMessage(self, topic, message):
        try:
            key = self.formatKey(topic, message)
            self.redis.set(key, 1, ex=self.expire)
        except Exception as e:
            self.log.warn(e)

    def isUnique(self, topic, message):
        try:
            key = self.formatKey(topic, message)
            result = self.redis.get(key)
            if result is not None:
                return False
            else:
                return True
        except Exception as e:
            self.log.warn(e)
            return True

    def formatKey(self, topic, message):
        return '{}-{}-{}'.format(topic, self.groupId,
                                 hash(str(message)))
