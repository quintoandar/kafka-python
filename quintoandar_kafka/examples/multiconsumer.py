from quintoandar_kafka import KafkaConsumerClient

consumer1 = KafkaConsumerClient(group_id='Test',
                                bootstrap_servers='localhost:9092', topic='Test1',
                                processor=print)
consumer2 = KafkaConsumerClient(group_id='Test',
                                bootstrap_servers='localhost:9092', topic='Test2',
                                processor=print)


consumer2.start()
consumer1.start()
