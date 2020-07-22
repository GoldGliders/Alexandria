import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import csv
import logging

formatter = "%(asctime)s  %(levelname)s  %(name)s  %(funcName)s  %(lineno)d : %(message)s"
logging.basicConfig(level=logging.DEBUG, format=formatter)
logger = logging.getLogger(__name__)


cred = credentials.Certificate("../bot/instance/key.json")
firebase_admin.initialize_app(cred)
db = firestore.client()


with open("./libraries.csv", "r", encoding="utf-8") as f:
    logger.info("I will register about 7400 libraries to specified db")
    cnt = 0
    reader = csv.DictReader(f)
    for library in reader:
        try:
            db.collection("library").document(library["libid"]).set(library)
            cnt += 1
            logger.info(f"NO.{cnt} sucess")

        except Exception as e:
            logger.info("Faild to registaring new library!")
            logger.info(e)
