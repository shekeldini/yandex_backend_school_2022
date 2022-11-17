import datetime
import threading
import os
from abc import ABC, abstractmethod
from enum import Enum
from pathlib import Path
import aiofiles


class LogLevel(Enum):
    TRACE = 1
    DEBUG = 2
    INFO = 3
    WARN = 4
    ERROR = 5
    OFF = 6


class LogEvent:
    def __init__(
            self,
            level: LogLevel,
            logger_name: str,
            message: str,
            event_datetime: datetime = datetime.datetime.utcnow(),
            thread: threading.Thread = threading.current_thread()
    ):
        self.level = level
        self.logger_name = logger_name
        self.message = message
        self.event_datetime = event_datetime
        self.thread = thread

    def __setattr__(self, attr, value):
        if hasattr(self, attr):
            raise Exception("Attempting to alter read-only value")

        self.__dict__[attr] = value


class LogAppender(ABC):
    @abstractmethod
    async def handle_event(self, event: LogEvent):
        pass


class ConsoleLogAppender(LogAppender):
    def __init__(self, level: LogLevel):
        self.level = level

    async def handle_event(self, event: LogEvent):
        if self.level.value > event.level.value:
            return
        print(event.message)


class FileLogAppender(LogAppender):
    def __init__(self, level: LogLevel, log_file_path: str):
        self.level = level
        self.log_file_path = Path(log_file_path)
        parent_dir = self.log_file_path.parent
        if not parent_dir.exists():
            os.makedirs(parent_dir)

    async def handle_event(self, event: LogEvent):
        if self.level.value > event.level.value:
            return
        async with aiofiles.open(self.log_file_path, "a", encoding='utf-8') as log_file:
            await log_file.write(event.message + "\n")
            await log_file.flush()


class FormattedLogAppender(LogAppender):
    def __init__(self, level: LogLevel, appender: LogAppender, log_format: str = "%D %T %l [%t] - %n: %m"):
        self.level = level
        self.appender = appender
        self.log_format = log_format

    async def handle_event(self, event: LogEvent):
        if self.level.value > event.level.value:
            return
        formatted_event = await self.__formatted_event__(event)
        await self.appender.handle_event(formatted_event)

    async def __formatted_event__(self, event: LogEvent):
        message = self.log_format
        message = message \
            .replace('%l', event.level.name) \
            .replace('%m', event.message) \
            .replace('%t', event.thread.name) \
            .replace('%n', event.logger_name) \
            .replace('%D', event.event_datetime.date().isoformat()) \
            .replace('%T', event.event_datetime.time().isoformat())
        return LogEvent(event.level, event.logger_name, message, event.event_datetime, event.thread)


class Logger:
    def __init__(self, name: str, logger_appender_list: list):
        self.name = name
        self.logger_appender_list = logger_appender_list

    async def trace(self, message: str):
        event = LogEvent(LogLevel.TRACE, self.name, message)
        await self.__proceed_event__(event)

    async def debug(self, message: str):
        event = LogEvent(LogLevel.DEBUG, self.name, message)
        await self.__proceed_event__(event)

    async def info(self, message: str):
        event = LogEvent(LogLevel.INFO, self.name, message)
        await self.__proceed_event__(event)

    async def warn(self, message: str):
        event = LogEvent(LogLevel.WARN, self.name, message)
        await self.__proceed_event__(event)

    async def error(self, message: str):
        event = LogEvent(LogLevel.ERROR, self.name, message)
        await self.__proceed_event__(event)

    async def __proceed_event__(self, event: LogEvent):
        for appender in self.logger_appender_list:
            await appender.handle_event(event)


class LoggerFactory:
    def __init__(self, appender_list: list):
        self.__appender_list = appender_list
        self.__loggers = dict()
        self.__logger_creation_lock = threading.Lock()

    def get_logger(self, name: str):
        if name not in self.__loggers:
            self.__logger_creation_lock.acquire()
            try:
                if name not in self.__loggers:
                    self.__loggers[name] = Logger(name, self.__appender_list)
            finally:
                self.__logger_creation_lock.release()
        return self.__loggers[name]


my_appender_list = [
    FormattedLogAppender(LogLevel.WARN, ConsoleLogAppender(level=LogLevel.WARN)),
    FormattedLogAppender(LogLevel.TRACE, FileLogAppender(LogLevel.TRACE, "logs/operations.log")),
]
factory = LoggerFactory(my_appender_list)
logger = factory.get_logger("main-logger")
