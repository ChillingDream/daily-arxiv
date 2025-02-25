import yaml
from flask import Flask

from exts import mongo
from routes import entrance, keywords

with open('config.yaml', 'r') as fp:
    config = yaml.safe_load(fp)

app = Flask(__name__)
app.config.update(config)
mongo.init_app(app)

app.register_blueprint(entrance)
app.register_blueprint(keywords)

if __name__ == "__main__":
    app.run(host='0.0.0.0')
