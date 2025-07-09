from enum import Enum

class LoggerEnum(Enum):
    STRATEGY = 1
    INSTRUMENT = 2
    LOGIN = 3
    ORDER = 4

class BrokerEnum(Enum):
    ICICI = 1
    ANGEL_ONE = 2

class SideEnum(Enum):
    BUY = 1
    SELL = 2

class OrderTypeEnum(Enum):
    MARKET = 1
    LIMIT = 2
    STOP_LOSS = 3

class ValidityEnum(Enum):
    DAY = 1
    IOC = 2