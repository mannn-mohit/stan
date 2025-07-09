import uuid
import logging
from configs import config
from utils.Constants import *
from connectivity.icici import Order
from protocol.InstrumentBase import instrument_base

logger_enum = LoggerEnum.ORDER

class OrderManager:
    def __init__(self):
        self.logger: logging.Logger = config.loggers.get(logger_enum, None)
        self.instrument_base = instrument_base

    def create_order(self,
                     token: int,
                     broker: BrokerEnum,
                     side: SideEnum,
                     order_type: OrderTypeEnum,
                     validity: ValidityEnum):
        instrument = self.instrument_base.get_instrument(instrument_id=instrument_id)
        self.logger.info(f'Instrument: {instrument}')