from flaskr.models.client import firestore_client

db = firestore_client("instance/key.json")
