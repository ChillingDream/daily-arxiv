import yaml
from flask import Flask

from exts import mongo
from routes import user_blueprint, kw_blueprint, query_blueprint

with open('config.yaml', 'r') as fp:
    config = yaml.safe_load(fp)

app = Flask(__name__)
app.config.update(config)
mongo.init_app(app)

app.register_blueprint(user_blueprint)
app.register_blueprint(kw_blueprint)
app.register_blueprint(query_blueprint)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
