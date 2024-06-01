from pymongo import MongoClient

# # Database configuration

from config import MONGO_URI
client = MongoClient(MONGO_URI)
db = client.scraperdb

