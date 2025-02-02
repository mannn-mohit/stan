import uuid
import logging
from utils.Constants import LoggerEnum
from configs import config

logger_enum = LoggerEnum.INSTRUMENT

class InstrumentBase:
    def __init__(self):
        self.logger: logging.Logger = config.loggers.get(logger_enum, None)
        self.instruments = {}
        self.allowed_keys = {"token",
                             "symbol",
                             "name",
                             "strike",
                             "tick_size",
                             "lot_size",
                             "expiry",
                             "instrument_type",
                             "exchange"}
        self.required_keys = self.allowed_keys
        return
    
    def convert_value(self, key: str, value: str):
        if value is None:
            return None
        
        if key in ["token", "lot_size"]:
            return int(value)
        elif key == "tick_size":
            return float(value)
        else:
            return value
    
    def add_instrument(self, instrument_data: dict):
        if not isinstance(instrument_data, dict):
            error = "Details must be a dictionary."
            return False, error
        
        missing_keys = self.required_keys - instrument_data.keys()
        if missing_keys:
            error = f"Missing required keys in details: {', '.join(missing_keys)}"
            return False, error
        
        extra_keys = instrument_data.keys() - self.allowed_keys
        if extra_keys:
            error = f"Unsupported keys in details: {', '.join(extra_keys)}"
            return False, error
        
        uuid_key = uuid.uuid4()

        self.instruments[uuid_key] = instrument_data
        return True, uuid_key
    
    def get_instrument(self, instrument_id: uuid):
        return self.instruments.get(instrument_id, None)
    
    def remove_instrument(self, instrument_id: uuid):
        if instrument_id in self.instruments:
            del self.instruments[instrument_id]
            return True
        return False
    
    def get_all_instrument(self):
        return self.instruments
    
    def get_instrument_by_attribute(self, attribute: str, value: str):
        if attribute not in self.allowed_keys:
            error = f"Invalid attribute: {attribute}"
            return False, error
        
        result = []
        for _, instrument_data in self.instruments.items():
            if instrument_data.get(attribute) == value:
                result.append(instrument_data)

        if result:
            return True, result
        else:
            error = f"No instruments found with {attribute} = {value}"
            return False, error
        
    def print(self):
        self.logger.info(f'All instruments: {len(self.instruments)}')

# to have singleton like behavior
instrument_base = InstrumentBase()