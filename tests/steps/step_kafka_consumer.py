from unittest.mock import MagicMock
from behave import given, when, then  # pylint: disable=E0611
from hamcrest import assert_that, equal_to
from quintoandar_kafka import KafkaConsumer


@given('KafkaConsumer is instantiated')
def step_impl_given_instance(context):
    context.kafka_consumer = KafkaConsumer.__new__(KafkaConsumer)
    context.kafka_consumer.log = MagicMock()
    message0 = MagicMock()
    message0.value = {"eventName": "test_event", "payload": "test_payload"}
    message1 = MagicMock()
    message1.value = {"eventName": "test_event1", "payload": "test_payload1"}
    message2 = MagicMock()
    message2.value = None
    context.kafka_consumer.consumer = [message0, message1, message2]


@when('I read from KafkaConsumer')
def step_impl_when_read(context):
    context.message_processor1 = MagicMock()
    context.message_processor2 = MagicMock()
    context.kafka_consumer.read([("test_event", context.message_processor1), ("test_event", context.message_processor2)])


@then('the message processor should be called with the correct parameters')
def step_impl_then_verify(context):
    context.message_processor1.assert_called_once()
    context.message_processor1.assert_called_with({
        'payload': 'test_payload',
        'eventName': 'test_event'
    })
    context.message_processor2.assert_called_once()
    context.message_processor2.assert_called_with({
        'payload': 'test_payload',
        'eventName': 'test_event'
    })


@when('I deserialize a dictionary')
def step_impl_when_deserialize(context):
    context.deserialized = context.kafka_consumer._deserializer(
        bytes('{"test": "test"}', 'utf8'))


@then('I expect the correct json')
def step_impl_then_verify_deserialize(context):
    assert_that(context.deserialized, equal_to({"test": "test"}))