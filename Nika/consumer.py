from kafka import KafkaConsumer
import json
# Docs: https://kafka-python.readthedocs.io/en/master/apidoc/KafkaConsumer.html


class Consumer:
    def __init__(self, topics, group_id, brokers, msg_offset='earliest'):
        """
        Класс для прослушивания кафки
        :param topics: Прослушиваемый топик
        :param group_id: Группа слушателей
        :param brokers: Массив(list) из брокеров
        :param log: Функция логирования
        """
        self.topics = topics
        self.group_id = group_id
        self.brokers = brokers
        self.msg_offset = msg_offset
        self.consumer = None

        self.connect()

    def connect(self):
        """
        Создает подключение к кафке
        """
        try:
            self.consumer = KafkaConsumer(self.topics,
                                          group_id=self.group_id,
                                          bootstrap_servers=self.brokers,
                                          auto_offset_reset=self.msg_offset,
                                          # value_deserializer=lambda m: json.loads(m.decode('utf-8'))
                                          )
        except BaseException as err:
            raise err
        else:
            print('Consumer created sucessfully!')

    def listen(self, processor):
        """
        Начинает слушать кафку
        :param processor: функция обработки для каждого сообщения из кафки
        :return:
        """
        for message in self.consumer:
            processor(message)

    def close(self):
        print('Consumer closed')
        self.consumer.close()
