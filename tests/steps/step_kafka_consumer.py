from unittest.mock import MagicMock
from behave import given, when, then  # pylint: disable=E0611
from hamcrest import assert_that, equal_to
from quintoandar_kafka import KafkaIdempotentConsumer

message = MagicMock()
message.value = {"test1": "test2"}
message.topic = "test3"


@given("A KafkaIdempotentConsumer is instanciated")
def step_impl_given_idempotent_kafka_consumer(context):
    context.idempotent_key = MagicMock()
    context.redis_host = "redis_host"
    context.redis_port = "redis_port"
    context.group_id = "test1"
    context.bootstrap_servers = "test2"
    context.topic = "test3"
    context.consumer = KafkaIdempotentConsumer.__new__(KafkaIdempotentConsumer)
    context.consumer.idempotence_client = MagicMock()
    context.consumer.config = {"consumer_timeout_ms": 0}
    context.consumer._iterator = MagicMock()


@when("The consumer receives an unique message")
def step_impl_when_message(context):
    context.consumer._iterator.__next__ = MagicMock(return_value=message)
    context.consumer.idempotence_client.is_unique = MagicMock(return_value=True)
    for m in context.consumer:
        print(m)
        context.msg = m
        break


@when("The consumer receives an repeated message")
def step_impl_when_repeated_message(context):
    repeated_msg = MagicMock()
    repeated_msg.topic = "repeated"
    repeated_msg.value = "repeated"
    context.consumer._iterator.__next__ = MagicMock()
    context.consumer._iterator.__next__.side_effect = [repeated_msg, message]
    context.consumer.idempotence_client.is_unique = MagicMock()
    context.consumer.idempotence_client.is_unique.side_effect = [False, True]
    for m in context.consumer:
        context.msg = m
        break


@then("The message should be returned")
def step_impl_then_return_msg(context):
    assert_that(context.msg, equal_to(message))


@then("The repeated message should be skipped")
def step_impl_then_skip_msg(context):
    assert_that(context.msg, equal_to(message))


@then("The idempotence_client should be called with the correct params")
def step_impl_then_call_is_unique(context):
    context.consumer.idempotence_client.mark_consumed_message.assert_called_once_with(
        message.topic, message
    )


@then("The idempotence_client should mark the message as consumed")
def step_impl_then_mark_consumed(context):
    context.consumer.idempotence_client.mark_consumed_message.assert_called_once_with(
        message.topic, message
    )
