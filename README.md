[![Build Status](https://travis-ci.org/quintoandar/python-kafka.svg?branch=master)](https://travis-ci.org/quintoandar/python-kafka)

# Python Kafka

QuintoAndar's kafka-python lib wrapper with additional fuctionalities.

## KafkaConsumer

A simple wrapper for kafka-python lib.

### Configuration

|        Name       |                 Description                  |
| ----------------- | -------------------------------------------- |
| group_id          | The consumer group id                        |
| bootstrap_servers | The bootstrap servers                        |
| topic             | The topic to consume from                    |
| processor         | The function that processes the event        |
| idempotenceClient | (optional) A client that checks for repeated events. Must implement the same interface as [IdempotenceClient](/clients/idempotence_client.py) |
| deserializer      | (optional) The deserializer                  |

## IdempotenceClient for Kafka

A redis implementation to check messages and avoid reprocessing events.

### Usage

`markConsumedMessage(topic, message)` creates a hash from the message and concatenates it with the topic and the group id. The message is reigstered as consumed with a default ttl of 2 weeks.

`isUnique(message)` verifies if the message has already been processed.

### Configuration

|        Name   |                 Description     |
| ------------- | ------------------------------- |
| host          | The redis host                  |
| port          | The redis port                  |
| groupId       | The consumer group id           |
| db            | (optional) The redis db option  |
| expire        | (optional) The redis ttl        |
| key_extractor | (optional) A funtion that extracts a key that uniquely identifies the event |