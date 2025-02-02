import csv
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
            "Token": "token",
            "ShortName": "symbol",
            "CompanyName": "name",
            "ticksize": "tick_size",
            "LotSize": "lot_size",
            "Expiry": "expiry",
            "InstrumentType": "instrument_type",
        }

    def parse_row(self, row: dict):
        instrument_data = {}

        for source, destination in self.field_mapping.items():
            if source in row:
                instrument_data[destination] = self.instrument_base.convert_value(destination, row[source])

        instrument_data["expiry"] = None
        instrument_data["strike"] = None
        instrument_data["lot_size"] = 1
        instrument_data["exchange"] = "NSE"

        ret_val, msg = self.instrument_base.add_instrument(instrument_data)
        self.logger.info(f"RetVal: {ret_val} and Msg: {msg} for data: {instrument_data}")

    def parse_file(self, file_path: str):
        with open(file_path, mode='r', newline='', encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file)

            csv_reader.fieldnames = [field.strip().replace('"', '') for field in csv_reader.fieldnames] 

            for row in csv_reader:
                cleaned_row = {key.strip().replace('"', ''): value.strip() for key, value in row.items()}
                self.parse_row(cleaned_row)