# display and manage keywords
from flask import Blueprint, request, jsonify

from models import User

kw_blueprint = Blueprint("kw_blueprint", __name__)


@kw_blueprint.route("/keywords", methods=["GET"])
def display_keywords():
    username = request.args.get("username")
    user = User.get(username)
    return jsonify({"keywords": user.get_keywords()})


@kw_blueprint.route("/keywords", methods=["POST"])
def set_keywords():
    username = request.json.get("username")
    keywords = request.json.get("keywords")
    user = User.get(username)
    success = user.set_keywords(keywords)
    return jsonify({"success": success})
