from pymongo import MongoClient
from pymongo.database import Database
import os


MONGO_URI = os.getenv("MONGO_URI", "mongodb://parkmate:parkmate@localhost:27017")


def get_db() -> Database:
    client = MongoClient(MONGO_URI)
    db = client["parkmate-demo"]  # Replace with your database name
    return db
