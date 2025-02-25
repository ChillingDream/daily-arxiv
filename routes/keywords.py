# display and manage keywords
from flask import Blueprint, render_template, request, redirect, url_for

from models import User

keywords = Blueprint('keywords', __name__)


@keywords.route('/keywords', methods=['GET'])
def display_keywords():
    username = request.args.get('username')
    user = User.get(username)
    user_keywords = user.keywords
    return render_template('index.html')


@keywords.route('/keywords', methods=['POST'])
def set_keywords():
    username = request.form.get('username')
    keywords = request.form.get('keywords')
    user = User.get(username)
    user.set_keywords(keywords)
    return redirect(url_for('entrance.home', username=username))