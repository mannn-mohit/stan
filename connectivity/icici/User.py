import urllib
from breeze_connect import BreezeConnect
import logging
from utils.Constants import UserEnum, LoggerEnum
from configs import config

#print("https://api.icicidirect.com/apiuser/login?api_key="+urllib.parse.quote_plus(api_key))

logger_enum = LoggerEnum.LOGIN
user_enum = UserEnum.ICICI

class User:
    def __init__(self):
        self.logger: logging.Logger = config.loggers[logger_enum]
        self.api_key="00eo58S31N42J0p844~c34196CI7n025"
        self.secret_key="8707619d(996h638l2H81t9bX8KG2523"
        self.api_session="50468906"

    def try_login(self):

        config.users[user_enum] = BreezeConnect(api_key=self.api_key)
        self.breeze: BreezeConnect = config.users[user_enum]

        try:
            self.breeze.generate_session(api_secret=self.secret_key, session_token=self.api_session)
        except:
            self.logger.warning(f'Error in creating a session, please login details')
            return
        
        self.logger.info("Login sucessful")

    def get_demat_holdings(self):
        ret = self.breeze.get_demat_holdings()
        self.logger.info(ret)

    def get_funds(self):
        ret = self.breeze.get_funds()
        self.logger.info(ret)