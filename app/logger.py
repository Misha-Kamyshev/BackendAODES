"""
Модуль для настройки системы логирования приложения.

Создает директории для логов, настраивает два логгера с файловыми обработчиками:

- error_logger: для записи ошибок (уровень ERROR)
- info_logger: для записи информационных сообщений (уровень INFO)

Импорты:
- os: Для работы с файловой системой и создания директорий
- logging: Стандартный модуль логирования Python
- logging.Logger: Тип для аннотации логгеров
- logging.FileHandler: Обработчик для записи логов в файлы

Переменные:
- PATH_LOG_DIR: Путь к директории для хранения логов
- PATH_LOG_ERROR: Путь к файлу для ошибок
- PATH_LOG_INFO: Путь к файлу для информационных сообщений

Функции:
- create_dirs: Создает необходимые директории для логов
- connect_log_file: Настраивает и возвращает кортеж логгеров (error_logger, info_logger)

Глобальные переменные:
- error_logger: Логгер для записи ошибок
- info_logger: Логгер для записи информационных сообщений
"""
import errno
import os
import logging
from logging import Logger, FileHandler

PATH_LOG_DIR = 'logs/'
PATH_LOG_ERROR = 'logs/error.log'
PATH_LOG_INFO = 'logs/info.log'


def create_dirs() -> None:
    """
    Создает директорию для логов, если она не существует.

    Обрабатывает возможные исключения при создании директорий и выводит их в консоль.
    """
    try:
        if not os.path.exists(PATH_LOG_DIR):
            os.makedirs(PATH_LOG_DIR)

    except PermissionError as e:
        print(f"Permission denied: Cannot create log directory '{PATH_LOG_DIR}': {e}")

    except OSError as e:
        if e.errno != errno.EEXIST:
            print(f"OS error creating directory '{PATH_LOG_DIR}': {e}")


def connect_log_file() -> tuple[Logger, Logger]:
    """
    Настраивает и возвращает два файловых логгера для ошибок и информации.

    :return: Кортеж из двух логгеров (error_logger, info_logger)
    """
    formatter = logging.Formatter('%(levelname)s %(asctime)s: %(message)s')

    logger_error: Logger = logging.getLogger('error_logger')
    logger_info: Logger = logging.getLogger('info_logger')

    logger_error.setLevel(logging.ERROR)
    logger_info.setLevel(logging.INFO)

    error_handler: FileHandler = logging.FileHandler(PATH_LOG_ERROR)
    info_handler: FileHandler = logging.FileHandler(PATH_LOG_INFO)

    error_handler.setFormatter(formatter)
    info_handler.setFormatter(formatter)

    logger_error.addHandler(error_handler)
    logger_info.addHandler(info_handler)

    return logger_error, logger_info


create_dirs()
error_logger, info_logger = connect_log_file()
