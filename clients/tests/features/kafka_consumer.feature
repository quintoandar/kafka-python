Feature: KafkaConsumer

    Scenario: Consumer configuration
        Given A default KafkaConsumerClient is instanciated
        Then The KafkaConsumer should be instanciated with the correct params

    Scenario: Custom consumer configuration
        Given KafkaConsumerClient with custom deserializer and idempotenceClinet
        Then The KafkaConsumer should be instanciated with the correct params
        And The idempotenceClient should be the provided client

    Scenario: Default serializer exception
        Given A default KafkaConsumerClient is instanciated
        When An invalid value is deserialized
        Then The deserialized value should be an empty object

    Scenario: Default serializer
        Given A default KafkaConsumerClient is instanciated
        When A valid value is deserialized
        Then The deserialized value should be the expected object

    Scenario: Default idempotenceClient unique message
        Given A default KafkaConsumerClient is instanciated
        And The consumer receives a message
        When The message is processed
        Then The processor should be called

    Scenario: Default idempotenceClient repeated message
        Given A default KafkaConsumerClient is instanciated
        And The consumer receives repeated messages
        When The message is processed
        Then The processor should be called for every message

    Scenario: Custom idempotenceClient unique message
        Given A default KafkaConsumerClient is instanciated
        And The consumer receives a message
        And The idempotenceClient marks the message as unique
        When The message is processed
        Then The processor should be called
        And The idempotenceClient should mark the message as consumed


    Scenario: Custom idempotenceClient repeated message
        Given A default KafkaConsumerClient is instanciated
        And The consumer receives a message
        And The idempotenceClient marks the message as repeated
        When The message is processed
        Then The processor should not be called