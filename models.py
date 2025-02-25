from flask_login import UserMixin
from exts import mongo
from pymongo import WriteConcern
from pymongo.errors import PyMongoError
from pymongo.client_session import ClientSession

class User(UserMixin):
    '''
    Currently does not require password.
    '''
    def __init__(self, username):
        self.username = username
        self.keywords = self._get_keywords()

    @staticmethod
    def get(username):
        user_data = mongo.db.users.find_one({"username": username})
        if user_data:
            return User(user_data['username'])
        return None

    @staticmethod
    def find_by_username(username):
        user_data = mongo.db.users.find_one({"username": username})
        if user_data:
            return User(user_data['username'])
        return None

    @staticmethod
    def get_all():
        return list(mongo.db.users.find())

    def _get_keywords(self):
        return mongo.db.keywords.find_one({"username": self.username})["keywords"]
    
    def set_keywords(self, keywords):
        self.keywords = keywords
        with mongo.cx.start_session() as session:
            with session.start_transaction(write_concern=WriteConcern("majority")):
                try:
                    mongo.db.keywords.delete_many({"username": self.username}, session=session)
                    for keyword in keywords:
                        mongo.db.keywords.insert_one({"username": self.username, "keyword": keyword}, session=session)
                except PyMongoError:
                    session.abort_transaction()
                    raise
