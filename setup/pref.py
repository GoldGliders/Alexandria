# coding: utf-8
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


pref = {}
with open("./libraries.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        p = pref.get(row["pref"])
        if p is None:
            p = set()
        p.add(row["city"])
        pref[row["pref"]] = p

for p in pref:
    logger.info(p)
    db.collection("pref").document(p).set({p: list(pref[p])})
