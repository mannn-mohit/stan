import logging
from configs import config
from utils.Constants import *
from breeze_connect import BreezeConnect

broker_enum = BrokerEnum.ICICI
logger_enum = LoggerEnum.ORDER

class Order:
    def __init__(self):
        self.logger: logging.Logger = config.loggers[logger_enum]
        self.user: BreezeConnect = config.brokers[broker_enum]

    def send_order(self, order_options: dict):
        order_response = self.user.place_order(stock_code="",
                                    exchange_code="",
                                    product="",
                                    action="buy",
                                    order_type="market",
                                    stoploss="",
                                    quantity="",
                                    price="",
                                    validity="")

        self.logger.info(f'Order response: {order_response}')

