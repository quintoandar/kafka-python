Feature: IdempotenceClient

    Scenario: Message is not duplicate
        Given IdempotenceClient is instanciated
        When Key exists in redis
        Then is_unique should return false

    Scenario: Message is duplicate
        Given IdempotenceClient is instanciated
        When Key doesnt exist in redis
        Then is_unique should return true

    Scenario: Corretly create key on mark_consumed_message
        Given IdempotenceClient is instanciated
        When mark_consumed_message is called
        Then The correct key should be saved on redis

    Scenario: Redis error on is_unique
        Given IdempotenceClient is instanciated
        When Redis raises an error
        Then is_unique should return true

    Scenario: Redis error on mark_consumed_message
        Given IdempotenceClient is instanciated
        When Redis raises an error
        Then mark_consumed_message not rase an error


    Scenario: mark_consumed_message with extractor
        Given IdempotenceClient is instanciated
        And A key extractor is defined
        When mark_consumed_message is called
        Then The correct key should be saved on redis

    Scenario: is_unique with extractor
        Given IdempotenceClient is instanciated
        And A key extractor is defined
        When is_unique is called
        Then The correct key should be passed to redis