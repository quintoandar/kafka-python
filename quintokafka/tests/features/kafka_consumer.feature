Feature: KafkaConsumer

    Scenario: KafkaIdempotentConsumer unique message
        Given A KafkaIdempotentConsumer is instanciated
        When The consumer receives an unique message
        Then The message should be returned
        And The idempotence_client should be called with the correct params
        And The idempotence_client should mark the message as consumed
    
    Scenario: KafkaIdempotentConsumer repeated message
        Given A KafkaIdempotentConsumer is instanciated
        When The consumer receives an repeated message
        Then The repeated message should be skipped
