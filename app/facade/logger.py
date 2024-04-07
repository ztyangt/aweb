import os
import sys
import logging
from typing import cast
from types import FrameType
from datetime import datetime
from loguru import logger


class Logger:
    def __init__(self) -> None:
        self.LOG_FOLDER = "runtime/logs/"
        self.LOG_ROTATION = "00:00"
        self.LOG_RETENTION_PERIOD = "30 days"
        self.LOG_ENCODING = "utf-8"
        self.LOG_BACKTRACE = True
        self.LOG_DIAGNOSE = True
        self.LOG_COMPRESSION_FORMAT = "zip"
        self.LOG_FORMAT = '<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> ' \
            '| <magenta>{process}</magenta>:<yellow>{thread.name}</yellow> ' \
            '| <cyan>{name}</cyan>:<cyan>{function}</cyan>:<yellow>{line}</yellow> - <level>{message}</level>'

        self.logger = logger
        self.logger.remove()

        try:
            os.makedirs(self.LOG_FOLDER, exist_ok=True)
        except OSError as e:
            print(
                f"Failed to create log directory: {e}. Falling back to a temporary directory.")
            self.LOG_FOLDER = "/tmp/logs/"

            # Re-attempt to create the directory after changing the path
            try:
                os.makedirs(self.LOG_FOLDER, exist_ok=True)
            except OSError as e:
                print(
                    f"Failed to create the fallback log directory as well: {e}. Exiting.")
                sys.exit(1)

    def init_config(self) -> None:
        self.add_logfile("DEBUG")
        self.add_logfile("INFO")
        self.add_logfile("WARNING")
        self.add_logfile("ERROR")
        self.add_logfile("CRITICAL")

        # self.logger.add(sys.stdout, format=self.LOG_FORMAT)

        LOGGER_NAMES = ("uvicorn.asgi", "uvicorn.access", "uvicorn")

        # change handler for default uvicorn logger
        logging.getLogger().handlers = [InterceptHandler()]
        for logger_name in LOGGER_NAMES:
            logging_logger = logging.getLogger(logger_name)
            logging_logger.handlers = [InterceptHandler()]

    def add_logfile(self, level):
        filename = f'{level.lower()}/{datetime.now().strftime("%Y-%m-%d")}.log'
        logger.add(
            sink=self.LOG_FOLDER + filename,
            level=level,
            backtrace=self.LOG_BACKTRACE,
            diagnose=self.LOG_DIAGNOSE,
            format=self.LOG_FORMAT,
            rotation=self.LOG_ROTATION,
            retention=self.LOG_RETENTION_PERIOD,
            encoding=self.LOG_ENCODING,
            compression=self.LOG_COMPRESSION_FORMAT,
            enqueue=True,
            catch=True,
            filter=lambda record: record["level"].no == logger.level(level).no
        )

    def get_logger(self):
        return self.logger


class InterceptHandler(logging.Handler):

    def emit(self, record: logging.LogRecord) -> None:  # pragma: no cover
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = str(record.levelno)

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:  # noqa: WPS609
            frame = cast(FrameType, frame.f_back)
            depth += 1
        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage(),
        )


Loggers = Logger()
log = Loggers.get_logger()
