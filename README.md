# Idempotence Client for Kafka

Checks messages to avoid reprocessing events.

## Usage

`markConsumedMessage(topic, message)` creates a hash from the message and concatenates it with the topic and the group id. The message is reigstered as consumed with a default ttl of 2 weeks.
