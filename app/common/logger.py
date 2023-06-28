import os
import time

from loguru import logger


class Logger:
    @staticmethod
    def log():
        basedir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        log_path = os.path.join(basedir, "logs")

        if not os.path.exists(log_path):
            os.mkdir(log_path)

        log_path = os.path.join(log_path, f'{time.strftime("%Y-%m-%d")}.log')

        logger.add(
            log_path,
            encoding="utf-8",
            level="DEBUG",
            rotation="00:00",
            retention="5 days",
            enqueue=True,
            backtrace=True,
            diagnose=True,
        )
        return logger


log = Logger().log()
