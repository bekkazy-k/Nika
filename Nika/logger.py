import logging
from datetime import datetime
import os
from Nika import util, colorprint as p


class Logger:
    def __init__(self, app_name, conf_type, log_level, pg, table_to_log):
        """
        Создает логгер.
        :param app_name: Имя приложения
        :param log_level: Уровень логирования
        :param pg: Инстанс подключения к PostgreSql
        """
        self.app_name = app_name
        self.conf_type = conf_type
        self.log_level = log_level
        self.logger = logging.getLogger(self.app_name)
        self.logger.setLevel(logging.INFO)
        self.postgres = pg
        self.table_to_log = table_to_log
        self.path_to_log = os.path.join(os.getcwd(), 'logs')
        self.log_file_name = None
        self.fh = None

        if not os.path.exists(self.path_to_log):
            os.makedirs(self.path_to_log)
            p.pr("##", 'Folder for logs created!', c='b,c')

        self.check_log_folder()

    def log(self, log_type, msg):
        """
        Метод для записи логов
        :param log_type: Тип лога: D, I, W, E, C
        :param msg: Текст лога
        """
        self.check_log_folder()
        message = msg
        if log_type == "D":
            if self.check_log_level("debug"):
                self.logger.debug(msg)

        elif log_type == "I":
            if self.check_log_level("info"):
                self.logger.info(msg)

        elif log_type == "W":
            if self.check_log_level("warning"):
                self.logger.warning(msg)

        elif log_type == "E":
            if self.check_log_level("error"):
                self.logger.error(msg)
                p.red(msg)
                if self.conf_type != 'dev':
                    self.postgres.new_log(self.app_name, "E", util.escape(message))

        elif log_type == "C":
            if self.check_log_level("critical"):
                self.logger.critical(msg)

    def check_log_level(self, level):
        """
        Проверяет тип лога из конфигов и входящих логов
        :param level: Уровень лога
        """
        if self.log_level == "debug":
            return True
        if self.log_level == "info" and level in ("info", "warning", "error", "critical"):
            return True
        if self.log_level == "warning" and level in ("warning", "error", "critical"):
            return True
        if self.log_level == "error" and level in ("error", "critical"):
            return True
        if self.log_level == "critical" and level == "critical":
            return True
        return False

    def check_log_folder(self):
        """
        Проверяет наличие папки по дате, при необходимости создает папку
        """
        name = datetime.today().strftime('%Y-%m-%d')
        # if not os.path.isfile(self.path_to_log + "/" + name + ".log"):
        if self.log_file_name is None:
            self.fh = logging.FileHandler(self.path_to_log + "/" + name + ".log", encoding="UTF-8")
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            self.fh.setFormatter(formatter)
            self.logger.addHandler(self.fh)

            self.log_file_name = name

        if self.log_file_name != name:
            # Create the logging file, if file is not found
            self.fh = logging.FileHandler(self.path_to_log + "/" + name + ".log", encoding="UTF-8")
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            self.fh.setFormatter(formatter)
            self.logger.addHandler(self.fh)

            self.log_file_name = name
