from datetime import datetime
from flask import Blueprint, request, jsonify

from models import User
from algorithms import exact_match
from exts import mongo

query_blueprint = Blueprint("query_blueprint", __name__)


@query_blueprint.route("/query", methods=["POST"])
def em_query():
    """
    Args:
        query: list of keywords
        start_time: start timestamp of the query
        end_time: end timestamp of the query
        start_index: start index of the query in the search results
        end_index: end index of the query in the search_results
    """
    keywords = request.json.get("query")
    st_time = request.json.get("start_time")
    ed_time = request.json.get("end_time")
    st_index = request.json.get("start_index")
    ed_index = request.json.get("end_index")

    st_time = datetime.fromtimestamp(st_time)
    ed_time = datetime.fromtimestamp(ed_time)

    restrictions = []
    date_mongo_expression = {"added_date": {"$gte": st_time, "$lt": ed_time}}
    restrictions.append(date_mongo_expression)

    articles = exact_match(
        mongo.db.processed_arxiv_data, keywords, restrictions=restrictions
    )
    articles = sorted(articles, key=lambda x: x["added_date"], reverse=True)
    articles = articles[st_index : ed_index + 1]

    for x in articles:
        x["added_date"] = x["added_date"].timestamp()
        x["submitted_date"] = x["submitted_date"].timestamp()
        x.pop("_id")
        x.pop("category")

    return jsonify(articles)
