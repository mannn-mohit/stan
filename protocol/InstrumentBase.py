import uuid
import logging
from utils.Constants import *
from configs import config
from utils.DBConfig import instrument_collection
from bson import ObjectId

logger_enum = LoggerEnum.INSTRUMENT

class InstrumentBase:
    def __init__(self):
        self.logger: logging.Logger = config.loggers.get(logger_enum, None)
        self.instruments = {}
        self.broker_key = {}
        self.allowed_keys = {"token",
                             "broker",
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

        value = value.strip()

        if key in {"lot_size"}:
            if value.isdigit():
                return int(value)
            else:
                print(f"⚠️ Cannot convert to int: key='{key}', value='{value}'")
                return None

        if key == "tick_size":
            try:
                return float(value)
            except ValueError:
                print(f"⚠️ Cannot convert to float: key='{key}', value='{value}'")
                return None

        return value
        
    def serialize_for_mongo(self, data: dict) -> dict:
        def serialize(val):
            if isinstance(val, Enum):
                return val.name  # or val.value
            return val
        return {k: serialize(v) for k, v in data.items()}
    
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

        self.instruments["uuid"] = uuid.uuid4()

        instrument_data = self.serialize_for_mongo(instrument_data)

        try:
            result = instrument_collection.update_one(
                {"token": instrument_data["token"], "broker": instrument_data["broker"]},
                {"$set": instrument_data},
                upsert=True
            )
            return True, "Inserted or updated instrument"
        except Exception as e:
            return False, str(e)
    
    def get_instrument_by_uuid(self, uuid_str: str):
        return instrument_collection.find_one({"uuid": uuid_str})

    def get_instrument(self, token: int, broker: BrokerEnum):
        return instrument_collection.find_one({"token": token, "broker": broker.name})

    def get_instrument_by_id(self, mongo_id: str):
        try:
            return instrument_collection.find_one({"_id": ObjectId(mongo_id)})
        except Exception:
            return None

    def remove_instrument(self, token: int, broker: BrokerEnum) -> bool:
        result = instrument_collection.delete_one({"token": token, "broker": broker.name})
        return result.deleted_count > 0

    def get_all_instruments(self):
        return list(instrument_collection.find())

    def get_instrument_by_attribute(self, attribute: str, value: str):
        if attribute not in self.allowed_keys:
            return False, f"Invalid attribute: {attribute}"
        
        results = list(instrument_collection.find({attribute: value}))
        if results:
            return True, results
        return False, f"No instruments found with {attribute} = {value}"

    def print(self) -> None:
        count = instrument_collection.count_documents({})
        self.logger.info(f'All instruments: {count}')

    '''    
    def get_instrument_by_uuid(self, instrument_id: uuid) -> dict:
        return self.instruments.get(instrument_id, None)
    
    def get_instrument(self, token: int, broker: BrokerEnum) -> dict:
        uuid_key = self.broker_key.get((token, broker), None)
        print(f'UUID: {uuid_key}')
        if uuid_key != None:
            return self.get_instrument_by_uuid(uuid_key)
        return None
    
    def remove_instrument(self, instrument_id: uuid) -> bool:
        if instrument_id in self.instruments:
            del self.instruments[instrument_id]
            return True
        return False
    
    def get_all_instrument(self) -> dict:
        return self.instruments
    
    def get_instrument_by_attribute(self, attribute: str, value: str) -> dict:
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
        
    def print(self) -> None:
        self.logger.info(f'All instruments: {len(self.instruments)}')'''

# to have singleton like behavior
instrument_base = InstrumentBase()