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


@user_blueprint.route("/users/read_papers", methods=["GET"])
def get_read_papers():
    username = request.args.get("username")
    user = User.get(username)
    if user:
        read_paper_ids = user.get_read_paper_ids()
        return jsonify({"arxiv_ids": read_paper_ids})
    return jsonify({"error": "User not found"}), 404


@user_blueprint.route("/users/read_papers", methods=["POST"])
def set_read_papers():
    username = request.json.get("username")
    read_paper_ids = request.json.get("arxiv_ids")
    user = User.get(username)
    if user:
        success = user.set_read_paper(read_paper_ids)
        return jsonify({"success": success})
    return jsonify({"error": "User not found"}), 404


@user_blueprint.route("/users/favorite_papers", methods=["GET"])
def get_favorite_papers():
    username = request.args.get("username")
    user = User.get(username)
    if user:
        favorite_paper_ids = user.get_favorite_paper_ids()
        return jsonify({"arxiv_ids": favorite_paper_ids})
    return jsonify({"error": "User not found"}), 404


@user_blueprint.route("/users/favorite_papers", methods=["POST"])
def set_favorite_papers():
    username = request.json.get("username")
    favorite_paper_ids = request.json.get("arxiv_ids")
    user = User.get(username)
    if user:
        success = user.set_favorite_paper(favorite_paper_ids)
        return jsonify({"success": success})
    return jsonify({"error": "User not found"}), 404

