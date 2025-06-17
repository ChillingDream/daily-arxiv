import yaml
from flask import Flask
from flask_cors import CORS

from exts import mongo, config
from routes import kw_blueprint, query_blueprint, user_blueprint, analysis_blueprint

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
app.config.update(config)
mongo.init_app(app)

app.register_blueprint(user_blueprint)
app.register_blueprint(kw_blueprint)
app.register_blueprint(query_blueprint)
app.register_blueprint(analysis_blueprint)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
