from enum import IntEnum
from logging import CRITICAL, DEBUG, ERROR, INFO, WARNING


class LogLevel(IntEnum):
    debug = DEBUG
    info = INFO
    warn = WARNING
    error = ERROR
    critical = CRITICAL
