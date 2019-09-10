import profig


class Config:
    def __init__(self, conf_type="dev"):
        """
        Класс конфигураций.
        В корне проекта требуются файлы config.cfg и configDev.cfg
        :param conf_type: Тип конфигураций (prod | dev)
        """
        self.conf_type = conf_type
        if conf_type == "prod":
            self.config = profig.Config('config.cfg')
        else:
            self.config = profig.Config('configDev.cfg')

        self.sync()

    def init(self, key, val):
        """
        Инициализация параметров конфигураций
        :param key: Ключ конфига
        :param val: Дефолтное значение конфига. Будет перезаписан
        :return:
        """
        self.config.init(key, val)

    def sync(self):
        """
        Метод синхронизирует конфиги и перезапишет дефолтные конфиги указанные через метод init()
        :return:
        """
        self.config.sync()

    def get(self, key):
        """
        Метод возвращает значение конфига
        :param key: Ключ конфига который надо вернуть
        :return: Значение конфига
        """
        try:
            conf_value = self.config[key]
            return conf_value
        except Exception as err:
            raise FileNotFoundError(f'Cannot find config: Key: {key}.  Error: {str(err)}')
