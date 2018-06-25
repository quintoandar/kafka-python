[![Build Status](https://travis-ci.org/quintoandar/python-kafka-idempotence-client.svg?branch=master)](https://travis-ci.org/quintoandar/python-kafka-idempotence-client)

# Idempotence Client for Kafka

Checks messages to avoid reprocessing events.

## Usage

`markConsumedMessage(topic, message)` creates a hash from the message and concatenates it with the topic and the group id. The message is reigstered as consumed with a default ttl of 2 weeks.
