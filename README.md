[![Build Status](https://travis-ci.org/quintoandar/python-kafka.svg?branch=master)](https://travis-ci.org/quintoandar/python-kafka)

# Python Kafka

QuintoAndar's kafka-python lib wrapper with additional functionalities.

## KafkaIdempotentConsumer

A simple wrapper for kafka-python lib that uses redis to check duplicate events.

### Configuration

|        Name       |                 Description                  |
| ----------------- | -------------------------------------------- |
| group_id          | The consumer group id                        |
| bootstrap_servers | The bootstrap servers                        |
| redis_host        | The topic to consume from                    |
| redis_port        | The function that processes the event        |
| idempotent_key    | Function which extract an unique identifier from the event |


See [examples](/quintokafka/examples)
