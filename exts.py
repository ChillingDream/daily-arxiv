import yaml

from flask_pymongo import PyMongo
from jinja2 import Environment, FileSystemLoader
import openai

with open("config.yaml", "r") as fp:
    config = yaml.safe_load(fp)

mongo = PyMongo()
llm_client = openai.OpenAI(base_url=config["llm_client"]["url"], api_key=config["llm_client"]["api_key"])
llm_config = {
    "model": config["llm_client"]["model_name"],
    "max_tokens": 16384,
}
llm = {
    "client": llm_client,
    "config": llm_config,
}
jinja_env = Environment(
    loader=FileSystemLoader("prompts"),
    autoescape=False,
)