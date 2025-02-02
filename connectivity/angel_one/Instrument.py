import json
from protocol.InstrumentBase import instrument_base
import logging
from utils.Constants import LoggerEnum
from configs import config

logger_enum = LoggerEnum.INSTRUMENT

class Instrument:
    def __init__(self):
        self.logger: logging.Logger = config.loggers[logger_enum]
        self.instrument_base = instrument_base
        self.field_mapping = {
            "token": "token",
            "symbol": "symbol",
            "name": "name",
            "strike": "strike",
            "tick_size": "tick_size",
            "lotsize": "lot_size",
            "expiry": "expiry",
            "instrumenttype": "instrument_type",
            "exch_seg": "exchange"
        }

    def parse_row(self, row: dict):
        instrument_data = {}

        for source, destination in self.field_mapping.items():
            if source in row:
                instrument_data[destination] = self.instrument_base.convert_value(destination, row[source])

        ret_val, msg = self.instrument_base.add_instrument(instrument_data)
        self.logger.info(f"RetVal: {ret_val} and Msg: {msg} for data: {instrument_data}")

    def parse_file(self, file_path: str):
        with open(file_path, mode='r', newline='', encoding='utf-8') as json_file:
            parsed_data = json.load(json_file)

        for row in parsed_data:
            self.parse_row(row)