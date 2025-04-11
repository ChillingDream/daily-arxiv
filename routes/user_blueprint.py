### Entrance of the application. Prompt user to select account.

import json
from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from calendar import monthrange

from exts import mongo
from models import User
from algorithms import exact_match

user_blueprint = Blueprint("user_blueprint", __name__)


@user_blueprint.route("/users", methods=["GET"])
def index():
    users = User.get_all()
    usernames = [user.username for user in users]
    return jsonify({"usernames": usernames})
