Feature: KafkaConsumer

    Scenario: Read messages from kafka
        Given KafkaConsumer is instantiated
        When I read from KafkaConsumer
        Then the message processor should be called with the correct parameters

    Scenario: Test json deserializer
        Given KafkaConsumer is instantiated
        When I deserialize a dictionary
        Then I expect the correct json