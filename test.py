import unittest

from kafka import KafkaConsumer

from Nika.producer import Producer
from Nika.consumer import Consumer


def handler(*args):
     return args


class TestConsumer(Consumer):
    def connect(self):
        try:
            self.consumer = KafkaConsumer(self.topics,
                                          group_id=self.group_id,
                                          bootstrap_servers=self.brokers,
                                          auto_offset_reset=self.msg_offset,
                                          consumer_timeout_ms=10000)
            return True
        except BaseException as err:
            return False, err

    def listen(self, processor):
        for message in self.consumer:
            return processor(message.topic, message.value)


class TestProducerConsumer(unittest.TestCase):
    def setUp(self):
        self.topics = 'test-topic'
        self.brokers = ["localhost:19092", "localhost:19093"]
        self.group_id = 'test-group'
        self.message = 'Hello'

        self.producer = Producer(self.topics, self.brokers)
        self.producer_connect = self.producer.connect()

        self.consumer = TestConsumer(self.topics, self.group_id, self.brokers)
        self.consumer_connect = self.consumer.connect()

    def test_producer_connect(self):
        self.assertTrue(self.producer_connect)

    def test_producer_send(self):
        sender = self.producer.send('Hello')
        self.assertTrue(sender)
        self.assertEqual(self.topics, sender[1].topic)
        self.assertEqual(len(self.message), sender[1].serialized_value_size)

    def test_consumer_connect(self):
        self.assertTrue(self.consumer_connect)
        self.consumer.close()

    def test_consumer_listen(self):
        receiver = self.consumer.listen(handler)
        self.assertEqual(self.topics, receiver[0])
        self.assertEqual(self.message, receiver[1].decode('utf-8'))
        self.consumer.close()


if __name__ == '__main__':
    unittest.main()
