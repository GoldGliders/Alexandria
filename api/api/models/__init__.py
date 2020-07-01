import os
from flaskr import logger
from pymongo import MongoClient

client = MongoClient(os.environ["MONGO_URI"])
db = client.LIBRARYBOT
