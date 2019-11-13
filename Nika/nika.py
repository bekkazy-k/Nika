from Nika import config, postgres, logger, consumer, producer, error, util, colorprint as p
import os


class Nika:
    def __init__(self, config_type='dev'):
        p.pr("################################################################################################", c='b')
        p.pr("##", f'Nika started with config', config_type, c='b,c,y')
        self.config_type = config_type
        self.conf = self.conf_init()
        self.pg = self.postgres_init('Postgres')
        self.log = self.log_init()
        self.srcData = None
        self.trgData = None

        self.console_info()

        self.log('I', 'Program started!')

    def conf_init(self):
        """
        Инициализация конфигов
        """
        try:
            return config.Config(self.config_type)
        except BaseException:
            text = error.handle()
            self.log('E', text)
            os._exit(1)
        pass


    def postgres_init(self, prefix):
        """
        Инициализация подключения к PostgreSql
        """
        try:
            user = self.conf.get(prefix + '.user')
            password = self.conf.get(prefix + '.password')
            host = self.conf.get(prefix + '.host')
            port = self.conf.get(prefix + '.port')
            database = self.conf.get(prefix + '.database')
            table_to_log = self.conf.get('Logger.table_to_log')
            return postgres.PostgresConn(user, password, host, port, database, table_to_log)
        except FileNotFoundError:
            text = error.handle()
            self.log('E', text)
            os._exit(1)
        except BaseException:
            text = error.handle()
            self.log('E', text)
            os._exit(1)

    def log_init(self):
        """
        Инициализация инстанса логирования
        """
        try:
            app_name = self.conf.get('Nika.name')
            log_level = self.conf.get('Logger.level')
            lg = logger.Logger(app_name, self.config_type, log_level, self.pg)
            return lg.log
        except FileNotFoundError:
            text = error.handle()
            self.log('E', text)
            os._exit(1)
        except BaseException:
            text = error.handle()
            self.log('E', text)
            os._exit(1)

    def console_info(self):
        """
        При запуске выводит информацию о приложении в консоль
        """
        if self.conf.get('Nika.srcData') == "kafka":
            p.pr("##", f'Source data is: "Kafka". Topic: "{self.conf.get("kafkaConsumer.topic")}". '
                 f'Brokers: {self.conf.get("kafkaConsumer.brokers")}', c='b,c')

        if self.conf.get("Nika.trgData") == "kafka":
            p.pr('##', f'Target data is: "Kafka". Topic: "{self.conf.get("kafkaProducer.topic")}". '
                 f'Brokers: {self.conf.get("kafkaProducer.brokers")}', c='b,c')
        elif self.conf.get("Nika.trgData") == 'postgres':
             p.pr('##', f'Target data is: "Postgres". User: "{self.conf.get("trgPostgres.user")}". Host: "{self.conf.get("trgPostgres.host")}". '
                 f'Port: {self.conf.get("trgPostgres.port")}. DB: "{self.conf.get("trgPostgres.database")}"', c='b,c')
        p.pr("################################################################################################", c='b')

    def init_trg_connection(self):
        """
        Создает объект Producer и соединение к кафке
        """
        if self.conf.get("Nika.trgData") == "kafka":
            topic = self.conf.get("kafkaProducer.topic")
            brokers = self.conf.get("kafkaProducer.brokers").replace(' ', '').replace('\"', '').split(',')
            self.trgData = producer.Producer(topic, brokers)
            if not self.trgData.connect():
                raise ConnectionError('Nika.trgData cannot connect to Kafka')
                
        elif self.conf.get("Nika.trgData") == 'postgres':
            try:
                if util.check_identical_pg(self.conf.get):
                    self.trgData = self.pg
                else:
                    self.trgData = self.postgres_init('trgPostgres')
            except BaseException:
                text = error.handle()
                self.log('E', text)
                os._exit(1)
        else:
            raise ConnectionError(f'Nika.trgData incorrect or not found in config file. '
                                  f'Nika.trgData: {self.conf.get("Nika.trgData")}')

    def validate_data(self, message):
        return message

    def pre_process_data(self, message):
        return message

    def process_data(self, message):
        return message

    def post_process_data(self, message):
        return message

    def prepare_to_send(self, message):
        return message

    def send_data(self, message):
        if self.conf.get("Nika.trgData") == 'kafka':
            if type(message) == list:
                for i in message:
                    message_for_send = i
                    if type(i) != str:
                        message_for_send = util.unmarshall(i)
                    self.trgData.send(message_for_send)
            elif type(message) == dict:
                self.trgData.send(util.unmarshall(message))
            elif type(message) == str:
                self.trgData.send(message)
            else:
                raise TypeError(f'Incorrect type of message to send. Type: {type(message)}')

        elif self.conf.get("Nika.trgData") == 'postgres':
            if type(message) != tuple:
                raise TypeError(f'Incorrect type of message to send. Type: {type(message)}. Need tuple.')
            if type(message[0]) != str:
                raise TypeError(f'Incorrect table name. Name: {message[0]}.')
            if type(message[1]) != list:
                raise TypeError(f'Incorrect type of message keys to send. Type: {type(message[1])}. Need list.')
            if type(message[2]) != list:
                raise TypeError(f'Incorrect type of message values to send. Type: {type(message[2])}. Need list.')
            try:
                self.trgData.insert(message[0], message[1], message[2])
            except BaseException:
                text = error.handle()
                self.log('E', text)
                os._exit(1)
                
            

    def process(self, message):
        msg = message.value
        msg = self.validate_data(msg)
        msg = self.pre_process_data(msg)
        msg = self.process_data(msg)
        msg = self.post_process_data(msg)
        msg = self.prepare_to_send(msg)
        self.send_data(msg)

    def start(self):
        """
        Создает объект Сonsumer, начиная слушать кафку
        """
        try:
            self.init_trg_connection()
        except BaseException:
            text = error.handle()
            self.log('E', text)
            os._exit(1)

        if self.conf.get("Nika.srcData") == 'kafka':
            try:
                topics = self.conf.get("kafkaConsumer.topic")
                group_id = self.conf.get("kafkaConsumer.groupID")
                brokers = self.conf.get("kafkaConsumer.brokers").replace(' ', '').replace('\"', '').split(',')
                msg_offset = 'earliest'
                self.srcData = consumer.Consumer(topics, group_id, brokers, msg_offset)
                self.srcData.listen(self.process)
            except FileNotFoundError:
                text = error.handle()
                self.log('E', text)
            except BaseException:
                text = error.handle()
                self.log('E', text)
            finally:
                # Закрываем соединение с кафкой и коммитим сообщение,
                # чтобы не получить исключение обратно от этого сообщения
                if self.srcData:
                    self.srcData.close()
                os._exit(1)
        else:
            text = "Nika.srcData incorrect or not found in config file"
            self.log('E', text)
            os._exit(1)
