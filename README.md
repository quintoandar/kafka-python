[![Build Status](https://travis-ci.org/quintoandar/python-kafka.svg?branch=master)](https://travis-ci.org/quintoandar/python-kafka)

# QuintoAndar Kafka Python Library

QuintoAndar's kafka-python lib wrapper with additional functionalities.

## KafkaIdempotentConsumer

A simple wrapper for kafka-python lib that uses redis to check duplicate events.

### Configuration

|        Name       |                 Description                  |
| ----------------- | -------------------------------------------- |
| group_id          | The consumer group id                        |
| bootstrap_servers | The bootstrap servers                        |
| redis_host        | The topic to consume from                    |
| redis_port        | The function that processes the event        |
| idempotent_key    | Function which extract an unique identifier from the event |


See [examples](/examples)

## Development

### Environment

At the bare minimum you'll need the following for your development
environment:

1. [Python 3.6.8](http://www.python.org/)

It is strongly recommended to also install and use [pyenv](https://github.com/pyenv/pyenv):

 - [pyenv-installer](https://github.com/pyenv/pyenv-installer)

This tool eases the burden of dealing with virtualenvs and having to activate and
deactivate'em by hand. Once you run `pyenv local my-project-venv` the directory you're
in will be bound to the `my-project-venv` virtual environment and then you will have
never to bother again activating the correct venv.

### Getting Started

#### 1. Clone the project:

```bash
git clone git@github.com:quintoandar/kafka-python.git
cd kafka-python
```

#### 2. Setup the python environment for the project:

```bash
make environment
```

#### 3. Install dependencies

You can just the make recipe:

```bash
make install
```
