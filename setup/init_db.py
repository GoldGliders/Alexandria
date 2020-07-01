import csv
import logging
import os
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

client = MongoClient(os.environ["MONGO_URI"])
db = client.LIBRARYBOT


formatter = "%(asctime)s  %(levelname)s  %(name)s  %(funcName)s  %(lineno)d : %(message)s"
logging.basicConfig(level=logging.DEBUG, format=formatter)
logger = logging.getLogger(__name__)

with open("./libraries.csv", "r", encoding="utf-8") as f:
    logger.info("I will register about 7400 libraries to specified mongodb")
    cnt = 0
    reader = csv.DictReader(f)
    for library in reader:
        try:
            db.libraries.insert(library)
            cnt += 1 
            logger.info(f"NO.{cnt} sucess")

        except DuplicateKeyError:
            logger.info("This user is already registared.")

        except Exception as e:
            logger.info("Faild to registaring new library!")
            logger.info(e)
