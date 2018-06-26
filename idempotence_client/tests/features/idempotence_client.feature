Feature: IdempotenceClient

    Scenario: Message is not duplicate
        Given IdempotenceClient is instanciated
        When Key exists in redis
        Then isUnique should return false

    Scenario: Message is duplicate
        Given IdempotenceClient is instanciated
        When Key doesnt exist in redis
        Then isUnique should return true

    Scenario: Corretly create key on markConsumedMessage
        Given IdempotenceClient is instanciated
        When markConsumedMessage is called
        Then The correct key should be saved on redis

    Scenario: Redis error on isUnique
        Given IdempotenceClient is instanciated
        When Redis raises an error
        Then isUnique should return true

    Scenario: Redis error on markConsumedMessage
        Given IdempotenceClient is instanciated
        When Redis raises an error
        Then markConsumedMessage not rase an error
