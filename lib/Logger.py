import logging
from datetime import datetime
from configs import config
from utils.Constants import LoggerEnum

class Logger:
    def __init__(self, logger_name, log_file_name):
        today_date = datetime.today().date()
        self.log_file_name = 'logs/' + log_file_name + '_' + str(today_date) + '.log'

        self.logger: logging.Logger = logging.getLogger(logger_name)
        self.logger.setLevel(logging.DEBUG)

        print_format = (
            '%(asctime)s.%(msecs)d ||'
            ' %(levelname)7s ||'
            ' %(process)d  ||'
            ' %(funcName)s() ||'
            ' %(filename)s:%(lineno)s ||'
            ' %(message)s'
        )
        
        formatter = logging.Formatter(print_format)

        file_handler = logging.FileHandler(self.log_file_name, mode='a')
        file_handler.setFormatter(formatter)

        self.logger.addHandler(file_handler)
        
        self.logger.info(f'Logger started for {logger_name}')
        
    def get_logger(self):
        return self.logger
    
    def get_logfilename(self):
        return self.log_file_name

config.loggers[LoggerEnum.STRATEGY] = Logger('strategy', 'strategy').get_logger()
config.loggers[LoggerEnum.INSTRUMENT] = Logger('instrument', 'instrument').get_logger()
config.loggers[LoggerEnum.LOGIN] = Logger('login', 'login').get_logger()
config.loggers[LoggerEnum.ORDER] = Logger('order', 'order').get_logger()