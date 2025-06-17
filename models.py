from flask_login import UserMixin
from pymongo.errors import PyMongoError

from exts import mongo
from algorithms import download_and_extract_tex


class User(UserMixin):
    """
    Currently does not require password.
    """

    def __init__(self, username):
        self.username = username
        self.keywords = self._get_keywords()
        self.read_paper_ids = self._get_read_paper_ids()
        self.favorite_paper_ids = self._get_favorite_paper_ids()

    @staticmethod
    def get(username):
        user_data = mongo.db.users.find_one({"username": username})
        if user_data:
            return User(user_data["username"])
        return None

    @staticmethod
    def find_by_username(username):
        user_data = mongo.db.users.find_one({"username": username})
        if user_data:
            return User(user_data["username"])
        return None

    @classmethod
    def get_all(cls):
        return [cls(user_data["username"]) for user_data in mongo.db.users.find()]

    def _get_keywords(self):
        if user := mongo.db.keywords.find_one({"username": self.username}):
            return user["keywords"]
        return []

    def get_keywords(self):
        return self.keywords

    def set_keywords(self, keywords):
        self.keywords = keywords
        try:
            mongo.db.keywords.update_one(
                {"username": self.username},
                {"$set": {"keywords": keywords}},
                upsert=True,
            )
        except PyMongoError as e:
            print(e)
            return False
        return True
    
    def _get_read_paper_ids(self):
        if info := mongo.db.read_papers.find_one({"username": self.username}):
            return info.get("arxiv_ids", [])
        return []
    
    def get_read_paper_ids(self):
        return self.read_paper_ids
    
    def set_read_paper(self, paper_ids, increment=False):
        """
        Set the read paper IDs for the user.
        """
        if not isinstance(paper_ids, list):
            paper_ids = [paper_ids]
        
        if increment:
            read_paper_ids = self.read_paper_ids
            for id in paper_ids:
                if id not in read_paper_ids:
                    read_paper_ids.append(id)
        else:
            read_paper_ids = paper_ids
            
        mongo.db.read_papers.update_one(
            {"username": self.username},
            {"$set": {"arxiv_ids": read_paper_ids}},
            upsert=True,
        )
        self.read_paper_ids = read_paper_ids
        return True
    
    def _get_favorite_paper_ids(self):
        """
        Get the favorite paper IDs for the user.
        """
        if info := mongo.db.favorite_papers.find_one({"username": self.username}):
            return info.get("arxiv_ids", [])
        return []
    
    def get_favorite_paper_ids(self):
        return self.favorite_paper_ids
    
    def set_favorite_paper(self, paper_ids, increment=False):
        """
        Set the favorite paper IDs for the user.
        """
        if not isinstance(paper_ids, list):
            paper_ids = [paper_ids]

        if increment:
            favorite_paper_ids = self.favorite_paper_ids
            for id in paper_ids:
                if id not in favorite_paper_ids:
                    favorite_paper_ids.append(id)
        else:
            favorite_paper_ids = paper_ids
            
        mongo.db.favorite_papers.update_one(
            {"username": self.username},
            {"$set": {"arxiv_ids": favorite_paper_ids}},
            upsert=True,
        )
        self.favorite_paper_ids = favorite_paper_ids
        return True


class PaperTex:
    """
    """

    def __init__(self, arxiv_id):
        self.arxiv_id = arxiv_id
        paper = mongo.db.papertex.find_one({"arxiv_id": arxiv_id})
        if paper:
            self.sections = paper["sections"]
            self.paraphrase = paper["paraphrase"]
        else:
            self.sections = download_and_extract_tex(arxiv_id)
            self.paraphrase = {}
    
    def get_paraprhrase(self, section_name):
        """
        Get the paraphrase of a specific section.
        """
        if section_name in self.paraphrase:
            return self.paraphrase[section_name]
        
