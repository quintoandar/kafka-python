from kafka import KafkaProducer
import json
import time

producer = KafkaProducer(bootstrap_servers='localhost:9092')

while True:
  json_text1 = json.dumps({"test1": "test1"}, ensure_ascii=False)
  producer.send('Test1', json_text1.encode())
  json_text2 = json.dumps({"test2": "test2"}, ensure_ascii=False)
  producer.send('Test2', json_text2.encode())
  time.sleep(10)
