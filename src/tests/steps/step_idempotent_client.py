from unittest.mock import MagicMock
from behave import given, when, then  # pylint: disable=E0611
from hamcrest import assert_that
from src.idempotent_client import IdempotentClient


@given('IdempotentClient is instanciated')
def step_impl_given_idempotent_client_instance(context):
    context.idempotent_client = IdempotentClient.__new__(IdempotentClient)
    context.idempotent_client.redis = MagicMock()
    context.idempotent_client.groupId = 'test'
    context.idempotent_client.expire = 10
    context.idempotent_client.log = MagicMock()


@when('Key exists in redis')
def step_impl_when_key_exists(context):
    context.idempotent_client.redis.get = MagicMock(return_value={'key': 1})


@when('Key doesnt exist in redis')
def step_impl_when_key_not_exists(context):
    context.idempotent_client.redis.get = MagicMock(return_value=None)


@when('Redis raises an error')
def step_impl_when_redis_error(context):
    context.idempotent_client.redis.get = MagicMock(
        side_effect=Exception('Somethig is not right!'))
    context.idempotent_client.redis.set = MagicMock(
        side_effect=Exception('Somethig is not right!'))


@when('markConsumedMessage is called')
def step_impl_when_markConsumedMessage_called(context):
    context.message = MagicMock()
    context.message.topic = 'Test'
    context.message.value = '{"test": "test"}'
    context.message.__str__.return_value = 'Topic="{}", Value="{}"'.format(
        context.message.topic, context.message.value)
    context.idempotent_client.markConsumedMessage(
        context.message.topic, context.message)


@then('The correct key should be saved on redis')
def step_impl_then_verify_correct_set_params(context):
    context.idempotent_client.redis.set\
        .assert_called_with('{}-{}-{}'
                            .format(context.message.topic, 'test',
                                    hash(str(context.message))),
                            1, ex=context.idempotent_client.expire)


@then('isUnique should return true')
def step_impl_then_verify_true(context):
    message = MagicMock()
    message.value = {'test': 'test'}
    message.topic = 'test'
    assert_that(context.idempotent_client.isUnique(
        message.topic, message) is True)


@then('isUnique should return false')
def step_impl_then_verify_false(context):
    message = MagicMock()
    message.value = {'test': 'test'}
    message.topic = 'test'
    assert_that(context.idempotent_client.isUnique(
        message.topic, message) is False)


@then('markConsumedMessage not rase an error')
def step_impl_then_verify_no_errors(context):
    message = MagicMock()
    message.value = {'test': 'test'}
    message.topic = 'test'
    assert_that(context.idempotent_client.markConsumedMessage(
        message.topic, message) is None)
