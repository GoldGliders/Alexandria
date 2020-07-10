import os
from flaskr.models.client import firestore_client

ROOTPATH = "/".join(os.getcwd().split("/")[:-2])
ROOTPATH = ROOTPATH if ROOTPATH else "/app"

db = firestore_client(ROOTPATH + "/instance/key.json")
