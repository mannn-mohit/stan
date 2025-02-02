from lib.Logger import Logger
import logging
from protocol.InstrumentBase import instrument_base
from connectivity.icici.Instrument import Instrument as InstrumentICICI
from connectivity.angel_one.Instrument import Instrument as InstrumentAngelOne
from connectivity.icici.User import Login
from configs import config
from utils.Constants import *
from connectivity.icici.Order import Order
from lib.OrderManager import OrderManager

strategy_logger: logging.Logger = config.loggers[LoggerEnum.STRATEGY]

def store_instruments():
    instrument_icici = InstrumentICICI()
    instrument_angle_one = InstrumentAngelOne()

    instrument_icici.parse_file('data/instrument/icici/NSEScripMaster.txt')
    instrument_angle_one.parse_file('data/instrument/angel_one/EQIns.json')
    instrument_base.print()

    strategy_logger.info('All instruments added successfully')

def try_login():
    login = Login()
    login.try_login()
    login.get_demat_holdings()
    login.get_funds()

def try_order():
    inst = instrument_base.get_instrument(100, BrokerEnum.ICICI)
    strategy_logger.info(f"Instrument: {inst}")

def main():
    store_instruments()
    #try_login()
    try_order()

if __name__ == '__main__':
    main()