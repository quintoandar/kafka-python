from quintoandar_kafka import KafkaIdempotentConsumer


consumer = KafkaIdempotentConsumer(
    "Test1",
    redis_host="localhost",
    redis_port=6379,
    idempotent_key=lambda m: m.value,
    group_id="Test",
    bootstrap_servers="localhost:9092",
)

for m in consumer:
    print(m)
