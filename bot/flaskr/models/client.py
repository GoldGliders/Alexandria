import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


class firestore_client(object):
    def __init__(self, path2keyfile):
        cred = credentials.Certificate(path2keyfile)
        firebase_admin.initialize_app(cred)

        self.db = firestore.client()
        self.collection_name = None
        self.document = None
        self.documents = None


    @property
    def library(self):
        self.collection_name = "library"

        return self


    @property
    def user(self):
        self.collection_name = "user"

        return self


    def find(self, name):
        self.document = self.db.collection(self.collection_name).document(name).get().to_dict()

        return self.document


    def filter(self, key, operator, value):
        documents = self.db.collection(self.collection_name).where(key, operator, value).stream()
        self.documents = {}
        for doc in documents:
            self.documents[doc.id] = doc.to_dict()

        return self.documents


    def set(self, document_name, document):
        self.db.collection(self.collection_name).document(document_name).set(document)


    def remove(self, document_name):
        self.db.collection(self.collection_name).document(document_name).delete()
