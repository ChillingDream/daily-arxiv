from flask_pymongo import PyMongo
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:21117')
mongo = PyMongo()
db = client.daily_arxiv