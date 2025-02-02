import time
from enum import Enum

class RateLimiterEnum(Enum):
    LOGIN_BY_PASSWORD = 1
    GET_PROFILE = 2
    LOGOUT = 3
    GENERATE_LIMIT = 4
    PLACE_ORDER = 5
    MODIFY_ORDER = 6
    CANCEL_ORDER = 7
    GET_LTP_DATA = 8
    GET_ORDER_BOOK = 9
    GET_TRADE_BOOK = 10
    GET_RMS = 11
    GET_HOLDING = 12
    GET_POSITION = 13
    CONVERT_POSITION = 14
    GET_CANDLE_DATA = 15
    CREATE_RULE = 16
    MODIFY_RULE = 17
    CANCEL_RULE = 18
    RULE_DETAILS = 19
    RULE_LIST = 20
    MARKET_DATA = 21

class RateLimiter():
    def __init__(self):
        self.limitData = {  
            RateLimiterEnum.LOGIN_BY_PASSWORD :         [1, 0, []],
            RateLimiterEnum.GET_PROFILE :               [1, 0, []],
            RateLimiterEnum.LOGOUT :                    [1, 0, []],
            RateLimiterEnum.GENERATE_LIMIT :            [1, 0, []],
            RateLimiterEnum.PLACE_ORDER :               [20, 0, []],
            RateLimiterEnum.MODIFY_ORDER :              [20, 0, []],
            RateLimiterEnum.CANCEL_ORDER :              [20, 0, []],
            RateLimiterEnum.GET_LTP_DATA :              [10, 0, []],
            RateLimiterEnum.GET_ORDER_BOOK :            [1, 0, []],
            RateLimiterEnum.GET_TRADE_BOOK :            [1, 0, []],
            RateLimiterEnum.GET_RMS :                   [1, 0, []],
            RateLimiterEnum.GET_HOLDING :               [1, 0, []],
            RateLimiterEnum.GET_POSITION :              [1, 0, []],
            RateLimiterEnum.CONVERT_POSITION :          [10, 0, []],
            RateLimiterEnum.GET_CANDLE_DATA :           [3, 0, []],
            RateLimiterEnum.CREATE_RULE :               [10, 0, []],
            RateLimiterEnum.MODIFY_RULE :               [10, 0, []],
            RateLimiterEnum.CANCEL_RULE :               [10, 0, []],
            RateLimiterEnum.RULE_DETAILS :              [1, 0, []],
            RateLimiterEnum.RULE_LIST :                 [1, 0, []],
            RateLimiterEnum.MARKET_DATA :               [10, 0, []]
        }

    def getCurrentTimeInMillis(self):
        return round(time.time() * 1000)

    def isAllowed(self, type):
        limitData = self.limitData[type]

        limit = limitData[0]
        count = limitData[1]
        timestampArr = limitData[2]

        if limit <= 0:
            return False
        
        currentTime = self.getCurrentTimeInMillis()

        index = count % limit
        
        if len(timestampArr) <= index:
            timestampArr.insert(index, currentTime)
            allowed = True
        else:
            previousTime = timestampArr[index]

            if currentTime - previousTime < 1000:
                allowed = False
            else:
                timestampArr[index] = currentTime
                allowed = True

        if allowed:
            count += 1
            self.limitData[type] = [limit, count, timestampArr]
            #print(limit, count, timestampArr)
            return True, 0
        else:
            return False, currentTime - previousTime
        
    def handleThrottling(self, type: RateLimiterEnum):
        while True:
            allowed, waitTime = self.isAllowed(type)

            if not allowed:
                print(f'Rate limit exceeded for {type.name}, need to wait for {waitTime}millis')
                time.sleep(waitTime/1000)
            else:
                break
