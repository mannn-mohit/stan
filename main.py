from lib.Logger import Logger
from protocol.InstrumentBase import instrument_base
from connectivity.icici.Instrument import Instrument as Instrument1
from connectivity.angel_one.Instrument import Instrument as Instrument2
from connectivity.icici.User import User
from configs import config
from utils.Constants import LoggerEnum
from connectivity.icici.Order import Order

strategy_logger = config.loggers[LoggerEnum.STRATEGY]
instrument_logger = config.loggers[LoggerEnum.INSTRUMENT]
login_logger = config.loggers[LoggerEnum.LOGIN]

def main():
    ins = Instrument1()
    ins_ao = Instrument2()

    ins.parse_file('data/instrument/icici/NSEScripMaster.txt')
    ins_ao.parse_file('data/instrument/angel_one/EQIns.json')
    instrument_base.print()

    strategy_logger.info('All instruments added successfully')

    user = User()
    user.try_login()
    user.get_demat_holdings()
    user.get_funds()

    order = Order()
    order.send_order({})

if __name__ == '__main__':
    main()