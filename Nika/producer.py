from kafka import KafkaProducer
from kafka.errors import KafkaError


class Producer:
    def __init__(self, topics, brokers):
        """
        Конструктор класса Зкщвгсук
        :param topics: Топик для отправки сообщения
        :param brokers: Брокеры кафки
        """
        self.topics = topics
        self.brokers = brokers
        self.producer = None

    def connect(self):
        """
        Создает соединение к кафке
        :return: True при успешном соединении, False при неудачном
        """
        try:
            self.producer = KafkaProducer(bootstrap_servers=self.brokers)
            return True
        except KafkaError:
            print("Kafka Producer connection Error!", KafkaError)
            return False

    def send(self, message):
        """
        Метод отправки сообщения в кафку
        :param message: Сообщение для отправки
        :return: True при успешной отправке, False при неудачном
        """
        future = self.producer.send(self.topics, bytes(message, 'utf-8'))

        # Block for 'synchronous' sends
        try:
            record_metadata = future.get(timeout=10)
        except KafkaError as kafkaErr:
            # Decide what to do if produce request failed...
            print(kafkaErr)
            return False

        # Successful result returns assigned partition and offset
        # print(record_metadata.topic)
        # print(record_metadata.partition)
        # print(record_metadata.offset)
        if record_metadata.partition:
            return True
        else:
            return False
