from unittest.mock import MagicMock
from behave import given, when, then  # pylint: disable=E0611
from hamcrest import assert_that
from quintoandar_kafka import IdempotenceClient


message = MagicMock()
message.value = {'test1': 'test2'}
message.topic = 'test3'


@given('IdempotenceClient is instanciated')
def step_impl_given_idempotence_client_instance(context):
    context.IdempotenceClient = IdempotenceClient.__new__(IdempotenceClient)
    context.IdempotenceClient.redis = MagicMock()
    context.IdempotenceClient.group_id = 'test'
    context.IdempotenceClient.expire = 10
    context.IdempotenceClient.log = MagicMock()
    context.IdempotenceClient.key_extractor = lambda message: message


@given('A key extractor is defined')
def step_impl_given_key_extractor_defined(context):
    context.IdempotenceClient.key_extractor = lambda message: message.value


@when('Key exists in redis')
def step_impl_when_key_exists(context):
    context.IdempotenceClient.redis.get = MagicMock(return_value={'key': 1})


@when('Key doesnt exist in redis')
def step_impl_when_key_not_exists(context):
    context.IdempotenceClient.redis.get = MagicMock(return_value=None)


@when('Redis raises an error')
def step_impl_when_redis_error(context):
    context.IdempotenceClient.redis.get = MagicMock(
        side_effect=Exception('Somethig is not right!'))
    context.IdempotenceClient.redis.set = MagicMock(
        side_effect=Exception('Somethig is not right!'))


@when('mark_consumed_message is called')
def step_impl_when_mark_consumed_message_called(context):
    context.message = message
    context.message.__str__.return_value = 'Topic="{}", Value="{}"'.format(
        context.message.topic, context.message.value)
    key = context.IdempotenceClient.key_extractor(context.message)
    context.expected_key = '{}-{}-{}'\
        .format(context.message.topic, context.IdempotenceClient.group_id,
                hash(str(key)))
    context.IdempotenceClient.mark_consumed_message(
        context.message.topic, context.message)


@when('is_unique is called')
def step_impl_when_is_unique_called(context):
    context.message = message
    context.message.__str__.return_value = 'Topic="{}", Value="{}"'.format(
        context.message.topic, context.message.value)
    key = context.IdempotenceClient.key_extractor(context.message)
    context.expected_key = '{}-{}-{}'\
        .format(context.message.topic, context.IdempotenceClient.group_id,
                hash(str(key)))
    context.IdempotenceClient.is_unique(
        context.message.topic, context.message)


@then('The correct key should be saved on redis')
def step_impl_then_verify_correct_set_params(context):
    context.IdempotenceClient.redis.set\
        .assert_called_with(context.expected_key,
                            1, ex=context.IdempotenceClient.expire)


@then('The correct key should be passed to redis')
def step_impl_then_verify_correct_get_params(context):
    context.IdempotenceClient.redis.get\
        .assert_called_with(context.expected_key)


@then('is_unique should return true')
def step_impl_then_verify_true(context):
    assert_that(context.IdempotenceClient.is_unique(
        message.topic, message) is True)


@then('is_unique should return false')
def step_impl_then_verify_false(context):
    assert_that(context.IdempotenceClient.is_unique(
        message.topic, message) is False)


@then('mark_consumed_message not rase an error')
def step_impl_then_verify_no_errors(context):
    assert_that(context.IdempotenceClient.mark_consumed_message(
        message.topic, message) is None)
