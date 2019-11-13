from kafka import KafkaConsumer
import json
# Docs: https://kafka-python.readthedocs.io/en/master/apidoc/KafkaConsumer.html


class Consumer:
    def __init__(self, topics, group_id, brokers, msg_offset='earliest'):
        """
        Класс для прослушивания кафки
        :param topics: (str) Прослушиваемый топик
        :param group_id: (str) Группа слушателей
        :param brokers: Массив(list) из брокеров
        :param msg_offset: (str) указатель очереди обработки сообщений
        """
        self.topics = topics
        self.group_id = group_id
        self.brokers = brokers
        self.msg_offset = msg_offset
        self.consumer = None

        self.value = lambda m: json.loads(m.decode('utf-8'))

        self.connect()

    def connect(self):
        """
        Создает подключение к кафке
        """
        try:
            self.consumer = KafkaConsumer(self.topics,
                                          group_id=self.group_id,
                                          bootstrap_servers=self.brokers,
                                          auto_offset_reset=self.msg_offset)
        except BaseException as err:
            raise err
        else:
            print('Consumer created successfully!')

    def listen(self, processor):
        """
        Начинает слушать кафку
        :param processor: (func) функция обработки для каждого сообщения из кафки
        """
        # message.topic
        # message.partition
        # message.offset
        # message.key
        # message.value
        for message in self.consumer:
            processor(message)

    def close(self):
        print('Consumer closed')
        self.consumer.close()
