from kafka import KafkaProducer
from kafka.errors import KafkaError


class Producer:
    def __init__(self, topics, brokers):
        """
        Конструктор класса для отправки сообщений
        :param topics: (str) Топик для отправки сообщения
        :param brokers: Массив(list) брокеров кафки
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
        :param message: (str) Сообщение для отправки
        :return: True при успешной отправке, False при неудачном
        """
        future = self.producer.send(self.topics, bytes(message, 'utf-8'))

        # блокирование 'синхронных' отправок
        try:
            record_metadata = future.get(timeout=10)
        except KafkaError as kafkaErr:
            print(kafkaErr)
            return False

        if record_metadata:
            return True, record_metadata
        else:
            return False
