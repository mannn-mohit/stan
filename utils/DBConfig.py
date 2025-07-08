from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["stan"]
instrument_collection = db["instruments"]
instrument_collection.create_index([("token", 1), ("broker", 1)], unique=True)
