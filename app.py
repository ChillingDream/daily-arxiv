import yaml
from flask import Flask
from flask_cors import CORS

from exts import mongo
from routes import kw_blueprint, query_blueprint, user_blueprint

with open("config.yaml", "r") as fp:
    config = yaml.safe_load(fp)

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
app.config.update(config)
mongo.init_app(app)

app.register_blueprint(user_blueprint)
app.register_blueprint(kw_blueprint)
app.register_blueprint(query_blueprint)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
