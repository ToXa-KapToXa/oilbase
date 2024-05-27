import logging.config
import logging
import yaml
from flask import Flask


def get_logger(logging_cfg_path: str, flask_log: bool, flask_app: Flask = None) -> logging.Logger:
    """
    Инициализация логирования.

    Создает оператор логирования с учетом конфигурации, прописанной в файле.
    Путь к файлу передается как строковый параметр.

    Arguments:
        logging_cfg_path (str): Путь до файла с конфигурацией
        flask_log (bool): Включать ли логирование от Flask
        flask_app (Flask): Объект класса API

    Returns:
        logging.Logger: Оператор логирования.
    """
    if flask_log:
        flask_app.logger.disabled = True
        log = logging.getLogger('werkzeug')
        log.setLevel(logging.ERROR)

    logger_api = logging.getLogger('log')

    with open(logging_cfg_path) as config_fin:
        logging.config.dictConfig(yaml.safe_load(config_fin.read()))

    return logger_api
