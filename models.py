from flask_login import UserMixin
from exts import mongo
from pymongo.errors import PyMongoError

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

    @classmethod
    def get_all(cls):
        return [cls(user_data['username']) for user_data in mongo.db.users.find()]

    def _get_keywords(self):
        return mongo.db.keywords.find_one({"username": self.username})["keywords"]

    def get_keywords(self):
        return self.keywords
    
    def set_keywords(self, keywords):
        self.keywords = keywords
        try:
            mongo.db.keywords.update_one({"username": self.username}, {"$set": {"keywords": keywords}}, upsert=True)
        except PyMongoError as e:
            print(e)
            return False
        return True
