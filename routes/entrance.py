### Entrance of the application. Prompt user to select account.

import json
from flask import Blueprint, render_template, request, redirect, url_for
from datetime import datetime
from calendar import monthrange

from exts import mongo
from models import User
from algorithms import exact_match

entrance = Blueprint('entrance', __name__)

@entrance.route('/')
def index():
    users = User.get_all()
    return render_template('index.html', users=users)

@entrance.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    user = User.get(username)
    if user:
        return redirect(url_for('entrance.home', username=username))
    else:
        return json.dumps({"code": 404, "msg": "User not found"})

@entrance.route('/home', methods=['GET'])
def home():
    username = request.args.get('username')
    year = request.args.get('year')
    month = request.args.get('month')

    restrictions = []
    if year or month:
        if year is None:
            year = datetime.now().year
        else:
            year = int(year)
            
        if month is None:
            start_date = datetime(year, 1, 1)
            end_date = datetime(year, 12, 31, 23, 59, 59)
        else:
            _, last_day = monthrange(year, int(month))
            start_date = datetime(year, int(month), 1)
            end_date = datetime(year, int(month), last_day, 23, 59, 59)
        
        date_mongo_expression = {
            "added_date": {
                "$gte": start_date,
                "$lt": end_date
            }
        }
        restrictions.append(date_mongo_expression)

    user = User.get(username)
    articles = exact_match(mongo.db.processed_arxiv_data, user.keywords, restrictions=restrictions)
    articles = sorted(articles, key=lambda x: x['added_date'], reverse=True)
    if user:
        return render_template('home.html', user=user, articles=articles[:20])
    else:
        return json.dumps({"code": 404, "msg": "User not found"})